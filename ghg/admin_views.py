"""
Admin Views for User Management and Activity Monitoring
پنل مدیریت کاربران و نظارت بر فعالیت‌ها
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
import json
import csv

from .models import (
    EmissionRecord, Supplier, CustomEmissionFactor, 
    MaterialRequest, ReportExtraInfo, IndustryRequest
)
from .security import get_client_ip, log_security_event


def is_admin_user(user):
    """Check if user is admin"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(is_admin_user)
def admin_dashboard(request):
    """پنل اصلی مدیریت"""
    
    # آمار کلی کاربران
    total_users = User.objects.count()
    active_users = User.objects.filter(last_login__gte=timezone.now() - timedelta(days=30)).count()
    new_users_today = User.objects.filter(date_joined__date=timezone.now().date()).count()
    new_users_week = User.objects.filter(date_joined__gte=timezone.now() - timedelta(days=7)).count()
    
    # آمار فعالیت‌ها
    total_emissions = EmissionRecord.objects.count()
    emissions_today = EmissionRecord.objects.filter(created_at__date=timezone.now().date()).count()
    total_suppliers = Supplier.objects.count()
    total_custom_factors = CustomEmissionFactor.objects.count()
    pending_requests = MaterialRequest.objects.filter(status='pending').count()
    
    # کاربران فعال امروز
    today_active_users = User.objects.filter(
        Q(last_login__date=timezone.now().date()) |
        Q(emission_records__created_at__date=timezone.now().date())
    ).distinct().count()
    
    # آمار انتشار کربن
    total_co2_kg = EmissionRecord.objects.aggregate(total=Sum('emissions_kg'))['total'] or 0
    total_co2_tons = total_co2_kg / 1000
    
    # کاربران برتر (بیشترین فعالیت)
    top_users = User.objects.annotate(
        emission_count=Count('emission_records'),
        total_emissions=Sum('emission_records__emissions_kg')
    ).filter(emission_count__gt=0).order_by('-emission_count')[:10]
    
    # فعالیت‌های اخیر
    recent_activities = EmissionRecord.objects.select_related('user').order_by('-created_at')[:20]
    
    # درخواست‌های در انتظار
    pending_material_requests = MaterialRequest.objects.filter(status='pending').select_related('user')[:10]
    pending_industry_requests = IndustryRequest.objects.filter(status='pending').select_related('user')[:10]
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'new_users_today': new_users_today,
        'new_users_week': new_users_week,
        'today_active_users': today_active_users,
        'total_emissions': total_emissions,
        'emissions_today': emissions_today,
        'total_suppliers': total_suppliers,
        'total_custom_factors': total_custom_factors,
        'pending_requests': pending_requests,
        'total_co2_tons': round(total_co2_tons, 2),
        'top_users': top_users,
        'recent_activities': recent_activities,
        'pending_material_requests': pending_material_requests,
        'pending_industry_requests': pending_industry_requests,
    }
    
    return render(request, 'admin/dashboard.html', context)


@user_passes_test(is_admin_user)
def user_list(request):
    """لیست کاربران با جزئیات کامل"""
    
    # فیلترها
    search = request.GET.get('search', '')
    status = request.GET.get('status', 'all')  # all, active, inactive, new
    sort_by = request.GET.get('sort', '-date_joined')
    
    # کوئری اصلی
    users = User.objects.annotate(
        emission_count=Count('emission_records'),
        total_emissions_kg=Sum('emission_records__emissions_kg'),
        supplier_count=Count('suppliers'),
        custom_factor_count=Count('custom_factors'),
        material_request_count=Count('material_requests')
    )
    
    # اعمال فیلترها
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    if status == 'active':
        users = users.filter(last_login__gte=timezone.now() - timedelta(days=30))
    elif status == 'inactive':
        users = users.filter(
            Q(last_login__lt=timezone.now() - timedelta(days=30)) |
            Q(last_login__isnull=True)
        )
    elif status == 'new':
        users = users.filter(date_joined__gte=timezone.now() - timedelta(days=7))
    
    # مرتب‌سازی
    users = users.order_by(sort_by)
    
    # صفحه‌بندی
    paginator = Paginator(users, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
        'sort_by': sort_by,
        'total_users': users.count(),
    }
    
    return render(request, 'admin/user_list.html', context)


@user_passes_test(is_admin_user)
def user_detail(request, user_id):
    """جزئیات کامل یک کاربر"""
    
    user = get_object_or_404(User, id=user_id)
    
    # آمار کلی کاربر
    emission_records = user.emission_records.all()
    total_emissions_kg = emission_records.aggregate(total=Sum('emissions_kg'))['total'] or 0
    total_emissions_tons = total_emissions_kg / 1000
    
    # آمار بر اساس Scope
    scope_stats = []
    for scope in ['1', '2', '3']:
        scope_records = emission_records.filter(scope=scope)
        scope_kg = scope_records.aggregate(total=Sum('emissions_kg'))['total'] or 0
        scope_stats.append({
            'scope': scope,
            'count': scope_records.count(),
            'emissions_kg': scope_kg,
            'emissions_tons': round(scope_kg / 1000, 3)
        })
    
    # فعالیت‌های اخیر
    recent_emissions = emission_records.order_by('-created_at')[:20]
    
    # تامین‌کنندگان
    suppliers = user.suppliers.all()
    
    # فاکتورهای سفارشی
    custom_factors = user.custom_factors.all()
    
    # درخواست‌ها
    material_requests = user.material_requests.all()
    
    # اطلاعات اضافی گزارش
    try:
        report_extra = user.report_extra_info
    except ReportExtraInfo.DoesNotExist:
        report_extra = None
    
    # آمار فعالیت ماهانه (6 ماه اخیر)
    monthly_activity = []
    for i in range(6):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=31)
        month_emissions = emission_records.filter(
            created_at__gte=month_start,
            created_at__lt=month_end
        ).aggregate(total=Sum('emissions_kg'))['total'] or 0
        
        monthly_activity.append({
            'month': month_start.strftime('%Y-%m'),
            'emissions_kg': month_emissions,
            'emissions_tons': round(month_emissions / 1000, 3)
        })
    
    monthly_activity.reverse()
    
    # فایل‌های آپلود شده
    uploaded_files = []
    for record in emission_records.filter(proof_document__isnull=False):
        if record.proof_document:
            uploaded_files.append({
                'record': record,
                'file': record.proof_document,
                'size': record.proof_document.size if record.proof_document else 0
            })
    
    for factor in custom_factors.filter(certificate_file__isnull=False):
        if factor.certificate_file:
            uploaded_files.append({
                'factor': factor,
                'file': factor.certificate_file,
                'size': factor.certificate_file.size if factor.certificate_file else 0
            })
    
    context = {
        'user_obj': user,  # تغییر نام برای جلوگیری از تداخل با request.user
        'total_emissions_kg': total_emissions_kg,
        'total_emissions_tons': round(total_emissions_tons, 3),
        'scope_stats': scope_stats,
        'recent_emissions': recent_emissions,
        'suppliers': suppliers,
        'custom_factors': custom_factors,
        'material_requests': material_requests,
        'report_extra': report_extra,
        'monthly_activity': monthly_activity,
        'uploaded_files': uploaded_files,
        'emission_count': emission_records.count(),
        'supplier_count': suppliers.count(),
        'custom_factor_count': custom_factors.count(),
        'request_count': material_requests.count(),
    }
    
    return render(request, 'admin/user_detail.html', context)


@user_passes_test(is_admin_user)
def activity_monitor(request):
    """نظارت بر فعالیت‌های زنده"""
    
    # فعالیت‌های امروز
    today = timezone.now().date()
    today_activities = EmissionRecord.objects.filter(
        created_at__date=today
    ).select_related('user').order_by('-created_at')
    
    # کاربران آنلاین (فعالیت در 15 دقیقه اخیر)
    online_threshold = timezone.now() - timedelta(minutes=15)
    online_users = User.objects.filter(
        Q(last_login__gte=online_threshold) |
        Q(emission_records__created_at__gte=online_threshold)
    ).distinct()
    
    # آمار ساعتی امروز
    hourly_stats = []
    for hour in range(24):
        hour_start = today_activities.filter(created_at__hour=hour)
        hourly_stats.append({
            'hour': f"{hour:02d}:00",
            'count': hour_start.count(),
            'users': hour_start.values('user').distinct().count()
        })
    
    # درخواست‌های اخیر
    recent_requests = MaterialRequest.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).select_related('user').order_by('-created_at')
    
    context = {
        'today_activities': today_activities[:50],
        'online_users': online_users,
        'hourly_stats': hourly_stats,
        'recent_requests': recent_requests,
        'online_count': online_users.count(),
        'today_activity_count': today_activities.count(),
    }
    
    return render(request, 'admin/activity_monitor.html', context)


@user_passes_test(is_admin_user)
def file_manager(request):
    """مدیریت فایل‌های آپلود شده"""
    
    # فایل‌های EmissionRecord
    emission_files = EmissionRecord.objects.filter(
        proof_document__isnull=False
    ).select_related('user').order_by('-created_at')
    
    # فایل‌های CustomEmissionFactor
    factor_files = CustomEmissionFactor.objects.filter(
        certificate_file__isnull=False
    ).select_related('user').order_by('-created_at')
    
    # آمار فایل‌ها
    total_emission_files = emission_files.count()
    total_factor_files = factor_files.count()
    
    # محاسبه حجم کل (تقریبی)
    total_size = 0
    for record in emission_files:
        if record.proof_document:
            try:
                total_size += record.proof_document.size
            except:
                pass
    
    for factor in factor_files:
        if factor.certificate_file:
            try:
                total_size += factor.certificate_file.size
            except:
                pass
    
    # تبدیل به MB
    total_size_mb = round(total_size / (1024 * 1024), 2)
    
    context = {
        'emission_files': emission_files[:100],
        'factor_files': factor_files[:100],
        'total_emission_files': total_emission_files,
        'total_factor_files': total_factor_files,
        'total_files': total_emission_files + total_factor_files,
        'total_size_mb': total_size_mb,
    }
    
    return render(request, 'admin/file_manager.html', context)


@user_passes_test(is_admin_user)
def export_user_data(request, user_id):
    """صادرات داده‌های کاربر به CSV"""
    
    user = get_object_or_404(User, id=user_id)
    
    # ایجاد response برای CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="user_{user.username}_data.csv"'
    
    writer = csv.writer(response)
    
    # هدر CSV
    writer.writerow([
        'Date', 'Scope', 'Category', 'Source', 'Activity Data', 
        'Unit', 'Emissions (kg CO2e)', 'Emissions (tons CO2e)', 
        'Country', 'Description', 'Supplier'
    ])
    
    # داده‌های انتشار
    for record in user.emission_records.all():
        writer.writerow([
            record.created_at.strftime('%Y-%m-%d %H:%M'),
            f"Scope {record.scope}",
            record.category,
            record.source_name,
            record.activity_data,
            record.unit,
            record.emissions_kg,
            record.emissions_tons,
            record.country,
            record.description or '',
            record.supplier.name if record.supplier else record.supplier_old or ''
        ])
    
    return response


@user_passes_test(is_admin_user)
def user_statistics_api(request):
    """API برای آمار کاربران (برای چارت‌ها)"""
    
    # آمار ثبت‌نام در 30 روز اخیر
    signup_stats = []
    for i in range(30):
        date = timezone.now().date() - timedelta(days=i)
        count = User.objects.filter(date_joined__date=date).count()
        signup_stats.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    signup_stats.reverse()
    
    # آمار فعالیت در 7 روز اخیر
    activity_stats = []
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        emission_count = EmissionRecord.objects.filter(created_at__date=date).count()
        active_users = User.objects.filter(
            Q(last_login__date=date) |
            Q(emission_records__created_at__date=date)
        ).distinct().count()
        
        activity_stats.append({
            'date': date.strftime('%Y-%m-%d'),
            'emissions': emission_count,
            'active_users': active_users
        })
    
    activity_stats.reverse()
    
    return JsonResponse({
        'signup_stats': signup_stats,
        'activity_stats': activity_stats
    })


@user_passes_test(is_admin_user)
def toggle_user_status(request, user_id):
    """فعال/غیرفعال کردن کاربر"""
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        
        # تغییر وضعیت
        user.is_active = not user.is_active
        user.save()
        
        # لاگ امنیتی
        action = 'activated' if user.is_active else 'deactivated'
        log_security_event(
            f'user_{action}',
            user.email,
            f'Admin {request.user.email} {action} user {user.email}'
        )
        
        status = 'فعال' if user.is_active else 'غیرفعال'
        messages.success(request, f'کاربر {user.username} {status} شد.')
        
        return JsonResponse({
            'success': True,
            'is_active': user.is_active,
            'message': f'کاربر {status} شد.'
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@user_passes_test(is_admin_user)
def delete_user_data(request, user_id):
    """حذف داده‌های کاربر (GDPR compliance)"""
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        
        # شمارش داده‌ها قبل از حذف
        emission_count = user.emission_records.count()
        supplier_count = user.suppliers.count()
        factor_count = user.custom_factors.count()
        request_count = user.material_requests.count()
        
        # حذف داده‌ها
        user.emission_records.all().delete()
        user.suppliers.all().delete()
        user.custom_factors.all().delete()
        user.material_requests.all().delete()
        
        # حذف اطلاعات اضافی
        try:
            user.report_extra_info.delete()
        except ReportExtraInfo.DoesNotExist:
            pass
        
        # لاگ امنیتی
        log_security_event(
            'user_data_deleted',
            user.email,
            f'Admin {request.user.email} deleted all data for user {user.email}'
        )
        
        messages.success(
            request, 
            f'تمام داده‌های کاربر {user.username} حذف شد: '
            f'{emission_count} رکورد انتشار، {supplier_count} تامین‌کننده، '
            f'{factor_count} فاکتور سفارشی، {request_count} درخواست'
        )
        
        return JsonResponse({
            'success': True,
            'deleted_counts': {
                'emissions': emission_count,
                'suppliers': supplier_count,
                'factors': factor_count,
                'requests': request_count
            }
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@user_passes_test(is_admin_user)
def security_logs(request):
    """نمایش لاگ‌های امنیتی"""
    
    # خواندن فایل لاگ امنیتی
    import os
    from django.conf import settings
    
    log_file_path = os.path.join(settings.BASE_DIR, 'logs', 'security.log')
    
    logs = []
    if os.path.exists(log_file_path):
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # آخرین 1000 خط
                for line in lines[-1000:]:
                    if line.strip():
                        logs.append(line.strip())
        except Exception as e:
            logs = [f"Error reading log file: {str(e)}"]
    else:
        logs = ["Security log file not found"]
    
    logs.reverse()  # جدیدترین‌ها اول
    
    # صفحه‌بندی
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_logs': len(logs),
    }
    
    return render(request, 'admin/security_logs.html', context)


def custom_admin_login(request):
    """صفحه لاگین ادمین سفارشی"""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('ghg:admin_dashboard')
    
    return redirect('ghg:email_login')