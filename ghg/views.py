from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Country, EmissionData
from django.db.models import Sum, Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import EmailLoginForm, EmailSignupForm

def index(request):
    # Redirect to login if not authenticated
    if not request.user.is_authenticated:
        return redirect('ghg:admin_login')
    
    countries = Country.objects.all().order_by('name')
    latest_year = EmissionData.objects.order_by('-year').first()
    total_emissions = EmissionData.objects.filter(
        year=latest_year.year if latest_year else 2023
    ).aggregate(Sum('total_ghg'))['total_ghg__sum'] or 0
    
    data_points = EmissionData.objects.count()
    
    context = {
        'countries': countries,
        'total_emissions': round(total_emissions, 2),
        'latest_year': latest_year.year if latest_year else 2023,
        'data_points': data_points,
    }
    return render(request, 'index.html', context)

@login_required
def data_entry(request):
    return render(request, 'data_entry.html')

@login_required
def calculate_emission(request):
    if request.method == 'POST':
        import json
        from .emission_factors import calculate_emissions
        from .models import EmissionRecord, Supplier
        
        data = json.loads(request.body)
        category = data.get('category')
        source = data.get('source')
        activity_data = float(data.get('activity_data', 0))
        country = data.get('country', 'global')
        description = data.get('description', '')
        industry_type = data.get('industry_type', '')
        fuel_name = data.get('fuel_name', '')
        supplier_id = data.get('supplier_id', None)
        save_record = data.get('save', True)  # Option to save or not
        
        result = calculate_emissions(category, source, activity_data, country)
        
        if 'error' not in result and save_record:
            # Determine scope based on category
            scope = '1'  # Default
            if category in ['electricity', 'steam-heat']:
                scope = '2'
            elif category in ['travel', 'waste', 'water', 'purchased-goods', 'capital-goods', 
                             'fuel-energy', 'upstream-transport', 'commuting', 'upstream-leased',
                             'downstream-transport', 'end-of-life', 'franchises', 'investments']:
                scope = '3'
            
            # Get supplier object if provided
            supplier_obj = None
            if supplier_id:
                try:
                    supplier_obj = Supplier.objects.get(id=supplier_id, user=request.user)
                except Supplier.DoesNotExist:
                    pass
            
            # Save to database
            record = EmissionRecord.objects.create(
                user=request.user,
                scope=scope,
                category=category,
                source=source,
                source_name=result['source_name'],
                activity_data=activity_data,
                unit=result['unit'],
                emission_factor=result['factor'],
                emissions_kg=result['emissions_kg'],
                emissions_tons=result['emissions_tons'],
                country=country,
                reference=result.get('reference', ''),
                description=description,
                industry_type=industry_type or None,
                fuel_name=fuel_name or None,
                supplier=supplier_obj
            )
            
            result['record_id'] = record.id
            result['saved'] = True
        
        return JsonResponse(result)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_country_data(request, country_code):
    try:
        country = Country.objects.get(code=country_code)
        emissions = EmissionData.objects.filter(country=country).order_by('year')
        
        data = {
            'country': country.name,
            'years': [e.year for e in emissions],
            'co2': [e.co2_emissions for e in emissions],
            'methane': [e.methane_emissions or 0 for e in emissions],
            'nitrous_oxide': [e.nitrous_oxide or 0 for e in emissions],
            'total': [e.total_ghg for e in emissions],
        }
        return JsonResponse(data)
    except Country.DoesNotExist:
        return JsonResponse({'error': 'Country not found'}, status=404)

@login_required
def get_global_data(request):
    years = EmissionData.objects.values_list('year', flat=True).distinct().order_by('year')
    
    data = {
        'years': list(years),
        'emissions': []
    }
    
    for year in years:
        total = EmissionData.objects.filter(year=year).aggregate(Sum('total_ghg'))['total_ghg__sum'] or 0
        data['emissions'].append(round(total, 2))
    
    return JsonResponse(data)

@login_required
def get_top_emitters(request):
    # Get latest year
    latest_year = EmissionData.objects.order_by('-year').first()
    year = latest_year.year if latest_year else 2023
    
    # Get top 10 emitters for that year
    top_emitters = EmissionData.objects.filter(year=year).select_related('country').order_by('-total_ghg')[:10]
    
    data = {
        'countries': [e.country.name for e in top_emitters],
        'emissions': [round(e.total_ghg, 2) for e in top_emitters]
    }
    
    return JsonResponse(data)

@login_required
def emission_history(request):
    """View to display user's emission calculation history"""
    from .models import EmissionRecord
    
    records = EmissionRecord.objects.filter(user=request.user).order_by('-created_at')[:50]
    
    # Calculate totals by scope
    scope1_total = EmissionRecord.objects.filter(user=request.user, scope='1').aggregate(
        total=Sum('emissions_kg'))['total'] or 0
    scope2_total = EmissionRecord.objects.filter(user=request.user, scope='2').aggregate(
        total=Sum('emissions_kg'))['total'] or 0
    scope3_total = EmissionRecord.objects.filter(user=request.user, scope='3').aggregate(
        total=Sum('emissions_kg'))['total'] or 0
    
    total_emissions = scope1_total + scope2_total + scope3_total
    
    context = {
        'records': records,
        'scope1_total': round(scope1_total / 1000, 2),  # Convert to tons
        'scope2_total': round(scope2_total / 1000, 2),
        'scope3_total': round(scope3_total / 1000, 2),
        'total_emissions': round(total_emissions / 1000, 2),
        'record_count': records.count()
    }
    
    return render(request, 'emission_history.html', context)

@login_required
def get_user_emissions_summary(request):
    """API endpoint for user's emission summary"""
    from .models import EmissionRecord
    from django.db.models import Sum
    from datetime import datetime, timedelta
    
    # Get date range (last 12 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    records = EmissionRecord.objects.filter(
        user=request.user,
        created_at__gte=start_date
    )
    
    # Group by scope
    scope_data = records.values('scope').annotate(
        total=Sum('emissions_kg')
    ).order_by('scope')
    
    # Group by month
    monthly_data = records.extra(
        select={'month': "strftime('%%Y-%%m', created_at)"}
    ).values('month').annotate(
        total=Sum('emissions_kg')
    ).order_by('month')
    
    # Top categories
    category_data = records.values('category', 'source_name').annotate(
        total=Sum('emissions_kg')
    ).order_by('-total')[:10]
    
    data = {
        'scope_totals': {
            'scope1': round(sum(s['total'] for s in scope_data if s['scope'] == '1') / 1000, 2),
            'scope2': round(sum(s['total'] for s in scope_data if s['scope'] == '2') / 1000, 2),
            'scope3': round(sum(s['total'] for s in scope_data if s['scope'] == '3') / 1000, 2),
        },
        'monthly': [
            {
                'month': m['month'],
                'emissions': round(m['total'] / 1000, 2)
            } for m in monthly_data
        ],
        'top_categories': [
            {
                'name': c['source_name'],
                'emissions': round(c['total'] / 1000, 2)
            } for c in category_data
        ],
        'total_records': records.count()
    }
    
    return JsonResponse(data)

@login_required
def user_guide(request):
    """Display user guide page"""
    return render(request, 'user_guide.html')


def email_login_view(request):
    """Login view using email"""
    if request.user.is_authenticated:
        return redirect('ghg:index')
    
    if request.method == 'POST':
        email = request.POST.get('username')  # Field name is 'username' but contains email
        password = request.POST.get('password')
        
        # Authenticate using email
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.email}!')
            return redirect('ghg:index')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            form = EmailLoginForm()
    else:
        form = EmailLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def email_signup_view(request):
    """Signup view using email"""
    if request.user.is_authenticated:
        return redirect('ghg:index')
    
    if request.method == 'POST':
        form = EmailSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='ghg.backends.EmailBackend')
            messages.success(request, 'Account created successfully! Welcome to Academia Carbon.')
            return redirect('ghg:index')
    else:
        form = EmailSignupForm()
    
    return render(request, 'auth/signup.html', {'form': form})


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully')
    return redirect('ghg:email_login')


@login_required
def get_suppliers(request):
    """API endpoint to get user's suppliers"""
    from .models import Supplier
    
    suppliers = Supplier.objects.filter(user=request.user).values('id', 'name', 'supplier_type')
    return JsonResponse({'suppliers': list(suppliers)})


@login_required
def add_supplier(request):
    """API endpoint to add a new supplier"""
    from .models import Supplier
    import json
    
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        
        if not name:
            return JsonResponse({'error': 'Supplier name is required'}, status=400)
        
        # Check if supplier already exists
        if Supplier.objects.filter(user=request.user, name=name).exists():
            return JsonResponse({'error': 'Supplier with this name already exists'}, status=400)
        
        # Combine phone code and number
        phone_code = data.get('phone_code', '')
        phone_number = data.get('phone', '')
        full_phone = f"{phone_code} {phone_number}".strip() if phone_code and phone_number else phone_number
        
        supplier = Supplier.objects.create(
            user=request.user,
            name=name,
            supplier_type=data.get('supplier_type') or None,
            contact_person=data.get('contact_person') or None,
            email=data.get('email') or None,
            phone=full_phone or None,
            country=data.get('country') or None,
            city=data.get('city') or None,
            tax_number=data.get('tax_number') or None,
            website=data.get('website') or None,
            address=data.get('address') or None,
            notes=data.get('notes') or None
        )
        
        return JsonResponse({
            'success': True,
            'supplier': {
                'id': supplier.id,
                'name': supplier.name,
                'supplier_type': supplier.supplier_type
            }
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)



@login_required
def get_custom_factors(request):
    """API endpoint to get user's custom emission factors"""
    from .models import CustomEmissionFactor
    
    category = request.GET.get('category', None)
    
    factors = CustomEmissionFactor.objects.filter(user=request.user)
    if category:
        factors = factors.filter(category=category)
    
    data = {
        'factors': [
            {
                'id': f.id,
                'material_name': f.material_name,
                'emission_factor': f.emission_factor,
                'unit': f.unit,
                'category': f.category,
                'is_verified': f.is_verified,
                'supplier_name': f.supplier.name if f.supplier else None,
            }
            for f in factors
        ]
    }
    
    return JsonResponse(data)


@login_required
def add_custom_factor(request):
    """API endpoint to add a custom emission factor"""
    from .models import CustomEmissionFactor, Supplier
    from .notifications import send_custom_factor_notification
    import json
    import logging
    
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        material_name = data.get('material_name', '').strip()
        emission_factor = data.get('emission_factor')
        unit = data.get('unit', '').strip()
        category = data.get('category', '').strip()
        
        if not all([material_name, emission_factor, unit, category]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            emission_factor = float(emission_factor)
        except ValueError:
            return JsonResponse({'error': 'Invalid emission factor value'}, status=400)
        
        # Get supplier if provided
        supplier_id = data.get('supplier_id')
        supplier_obj = None
        if supplier_id:
            try:
                supplier_obj = Supplier.objects.get(id=supplier_id, user=request.user)
            except Supplier.DoesNotExist:
                pass
        
        # Create custom factor
        custom_factor = CustomEmissionFactor.objects.create(
            user=request.user,
            supplier=supplier_obj,
            material_name=material_name,
            category=category,
            description=data.get('description', ''),
            emission_factor=emission_factor,
            unit=unit,
            source_reference=data.get('source_reference', '')
        )
        
        # Optional: notify admins about the new custom factor
        try:
            notification_sent = send_custom_factor_notification(custom_factor)
            if notification_sent:
                logger.info(f"Notification sent for custom factor: {material_name}")
            else:
                logger.warning(f"Notification not sent for custom factor: {material_name}")
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            # Don't fail the request if notification fails
        
        return JsonResponse({
            'success': True,
            'factor': {
                'id': custom_factor.id,
                'material_name': custom_factor.material_name,
                'emission_factor': custom_factor.emission_factor,
                'unit': custom_factor.unit,
                'category': custom_factor.category,
            }
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def request_new_material(request):
    """API endpoint to request a new material/source"""
    from .models import MaterialRequest
    from .notifications import send_material_request_notification
    import json
    import logging
    
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        material_name = data.get('material_name', '').strip()
        category = data.get('category', '').strip()
        description = data.get('description', '').strip()
        
        if not all([material_name, category, description]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Create material request
        material_request = MaterialRequest.objects.create(
            user=request.user,
            material_name=material_name,
            category=category,
            description=description,
            suggested_factor=data.get('suggested_factor'),
            suggested_unit=data.get('suggested_unit'),
            suggested_source=data.get('suggested_source', '')
        )
        
        # Send notification to admin
        try:
            notification_sent = send_material_request_notification(material_request)
            if notification_sent:
                logger.info(f"Notification sent for material request: {material_name}")
            else:
                logger.warning(f"Notification not sent for material request: {material_name}")
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
            # Don't fail the request if notification fails
        
        return JsonResponse({
            'success': True,
            'message': 'Your request has been submitted. Admin will review it soon.',
            'request_id': material_request.id
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def calculate_with_custom_factor(request):
    """Calculate emissions using a custom emission factor"""
    import json
    from .models import EmissionRecord, CustomEmissionFactor
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        custom_factor_id = data.get('custom_factor_id')
        activity_data = float(data.get('activity_data', 0))
        description = data.get('description', '')
        
        if not custom_factor_id or activity_data <= 0:
            return JsonResponse({'error': 'Invalid data'}, status=400)
        
        try:
            custom_factor = CustomEmissionFactor.objects.get(id=custom_factor_id, user=request.user)
        except CustomEmissionFactor.DoesNotExist:
            return JsonResponse({'error': 'Custom factor not found'}, status=404)
        
        # Calculate emissions
        emissions_kg = activity_data * custom_factor.emission_factor
        emissions_tons = emissions_kg / 1000.0
        
        # Determine scope based on category
        scope = '3'  # Default to Scope 3
        if custom_factor.category in ['stationary', 'mobile', 'fugitive']:
            scope = '1'
        elif custom_factor.category in ['electricity', 'steam-heat']:
            scope = '2'
        
        # Save to database
        record = EmissionRecord.objects.create(
            user=request.user,
            scope=scope,
            category=custom_factor.category,
            source='custom-' + str(custom_factor.id),
            source_name=custom_factor.material_name,
            activity_data=activity_data,
            unit=custom_factor.unit,
            emission_factor=custom_factor.emission_factor,
            emissions_kg=emissions_kg,
            emissions_tons=emissions_tons,
            country='custom',
            reference=f'Custom factor: {custom_factor.source_reference}' if custom_factor.source_reference else 'Custom emission factor',
            description=description,
            supplier=custom_factor.supplier
        )
        
        result = {
            'emissions_kg': round(emissions_kg, 4),
            'emissions_tons': round(emissions_tons, 6),
            'factor': custom_factor.emission_factor,
            'unit': custom_factor.unit,
            'source_name': custom_factor.material_name,
            'activity_data': activity_data,
            'country': 'custom',
            'category': custom_factor.category,
            'source_key': 'custom-' + str(custom_factor.id),
            'reference': custom_factor.source_reference or 'Custom emission factor',
            'record_id': record.id,
            'saved': True,
            'is_custom': True,
            'is_verified': custom_factor.is_verified
        }
        
        return JsonResponse(result)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_emission_record(request, record_id):
    """API endpoint to get a single emission record"""
    from .models import EmissionRecord
    
    try:
        record = EmissionRecord.objects.get(id=record_id, user=request.user)
        
        return JsonResponse({
            'id': record.id,
            'activity_data': record.activity_data,
            'unit': record.unit,
            'description': record.description or '',
            'source_name': record.source_name,
            'emissions_kg': record.emissions_kg,
            'emissions_tons': record.emissions_tons,
            'created_at': record.created_at.isoformat()
        })
        
    except EmissionRecord.DoesNotExist:
        return JsonResponse({'error': 'Record not found'}, status=404)


@login_required
def update_emission_record(request, record_id):
    """API endpoint to update an emission record"""
    from .models import EmissionRecord
    import json
    
    if request.method == 'PUT':
        try:
            record = EmissionRecord.objects.get(id=record_id, user=request.user)
            data = json.loads(request.body)
            
            # Get new activity data
            new_activity_data = float(data.get('activity_data', record.activity_data))
            new_description = data.get('description', record.description or '')
            
            if new_activity_data <= 0:
                return JsonResponse({'error': 'Activity data must be greater than 0'}, status=400)
            
            # Recalculate emissions if activity data changed
            if new_activity_data != record.activity_data:
                record.activity_data = new_activity_data
                record.emissions_kg = new_activity_data * record.emission_factor
                record.emissions_tons = record.emissions_kg / 1000.0
            
            # Update description
            record.description = new_description
            record.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Record updated successfully',
                'record': {
                    'id': record.id,
                    'activity_data': record.activity_data,
                    'emissions_kg': record.emissions_kg,
                    'emissions_tons': record.emissions_tons,
                    'description': record.description
                }
            })
            
        except EmissionRecord.DoesNotExist:
            return JsonResponse({'error': 'Record not found'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid activity data'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def delete_emission_record(request, record_id):
    """API endpoint to delete an emission record"""
    from .models import EmissionRecord
    
    if request.method == 'DELETE':
        try:
            record = EmissionRecord.objects.get(id=record_id, user=request.user)
            record.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Record deleted successfully'
            })
            
        except EmissionRecord.DoesNotExist:
            return JsonResponse({'error': 'Record not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def export_emission_report(request, scope):
    """API endpoint to export emission records as Excel report"""
    from .models import EmissionRecord
    from django.http import HttpResponse
    import io
    from datetime import datetime
    
    try:
        # Try to import openpyxl for Excel export
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
    except ImportError:
        return JsonResponse({'error': 'Excel export not available. Please install openpyxl.'}, status=500)
    
    # Filter records based on scope
    records = EmissionRecord.objects.filter(user=request.user).order_by('-created_at')
    
    if scope != 'all':
        scope_number = scope.replace('scope', '')
        records = records.filter(scope=int(scope_number))
    
    # Create workbook and worksheet
    wb = Workbook()
    ws = wb.active
    
    # Set worksheet title based on scope (max 31 chars for Excel)
    scope_titles = {
        'all': 'All Scopes Report',
        'scope1': 'Scope 1 Direct',
        'scope2': 'Scope 2 Electricity', 
        'scope3': 'Scope 3 Indirect'
    }
    ws.title = scope_titles.get(scope, 'Emission Report')
    
    # Define styles
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2D7A5F", end_color="2D7A5F", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Add title
    ws.merge_cells('A1:H1')
    title_cell = ws['A1']
    title_cell.value = f"Academia Carbon - {scope_titles.get(scope, 'Emission Report')}"
    title_cell.font = Font(bold=True, size=16, color="2D7A5F")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Add generation info
    ws.merge_cells('A2:H2')
    info_cell = ws['A2']
    info_cell.value = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | User: {request.user.email}"
    info_cell.font = Font(size=10, color="666666")
    info_cell.alignment = Alignment(horizontal="center")
    
    # Add summary statistics
    total_records = records.count()
    total_emissions_kg = sum(record.emissions_kg for record in records)
    total_emissions_tons = total_emissions_kg / 1000.0
    
    ws.merge_cells('A4:H4')
    summary_cell = ws['A4']
    summary_cell.value = f"Summary: {total_records} records | Total Emissions: {total_emissions_kg:.2f} kg CO2e ({total_emissions_tons:.3f} tons CO2e)"
    summary_cell.font = Font(bold=True, size=12, color="2D7A5F")
    summary_cell.alignment = Alignment(horizontal="center")
    
    # Headers
    headers = ['Date', 'Time', 'Scope', 'Source', 'Activity Data', 'Unit', 'Emissions (kg CO2e)', 'Emissions (tons CO2e)', 'Country', 'Description']
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=6, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border
    
    # Data rows
    for row, record in enumerate(records, 7):
        data = [
            record.created_at.strftime('%Y-%m-%d'),
            record.created_at.strftime('%H:%M:%S'),
            f"Scope {record.scope}",
            record.source_name,
            record.activity_data,
            record.unit,
            round(record.emissions_kg, 3),
            round(record.emissions_tons, 6),
            'Turkey' if record.country == 'turkey' else 'Global',
            record.description or ''
        ]
        
        for col, value in enumerate(data, 1):
            cell = ws.cell(row=row, column=col)
            cell.value = value
            cell.border = border
            
            # Color code by scope
            if col == 3:  # Scope column
                if record.scope == 1:
                    cell.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
                elif record.scope == 2:
                    cell.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
                elif record.scope == 3:
                    cell.fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
    
    # Auto-adjust column widths
    for col in range(1, len(headers) + 1):
        column_letter = get_column_letter(col)
        max_length = 0
        for row in ws[column_letter]:
            try:
                if len(str(row.value)) > max_length:
                    max_length = len(str(row.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Save to memory
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    # Create response
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    # Set filename
    scope_names = {
        'all': 'All_Scopes',
        'scope1': 'Scope_1_Direct_Emissions',
        'scope2': 'Scope_2_Electricity',
        'scope3': 'Scope_3_Indirect_Emissions'
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{scope_names.get(scope, 'Emission')}_Report_{today}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response