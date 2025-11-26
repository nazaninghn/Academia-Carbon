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
