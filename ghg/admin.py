from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from datetime import datetime, timedelta
import csv
import json

from .models import (
    Country, EmissionData, EmissionRecord, Supplier, CustomEmissionFactor, 
    MaterialRequest, ReportExtraInfo, IndustryType, IndustryRequest
)
import logging

logger = logging.getLogger(__name__)

# Global Admin Settings
admin.site.site_header = "🌱 Academia Carbon - Admin Panel"
admin.site.site_title = "Academia Carbon Admin"
admin.site.index_title = "Carbon Management System"

# Custom User Admin with Complete Details
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'full_name', 'user_stats', 'activity_status', 
        'last_login_formatted', 'date_joined_formatted', 'user_actions'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('📊 User Statistics', {
            'fields': ('user_statistics',),
            'classes': ('wide',)
        }),
    )
    
    readonly_fields = BaseUserAdmin.readonly_fields + ('user_statistics',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related().prefetch_related(
            'emission_records', 'suppliers', 'custom_factors', 'material_requests'
        )
    
    def full_name(self, obj):
        return obj.get_full_name() or obj.username
    full_name.short_description = 'Full Name'
    
    def user_stats(self, obj):
        emissions_count = getattr(obj, '_emissions_count', obj.emission_records.count())
        total_co2 = getattr(obj, '_total_co2', 
                           obj.emission_records.aggregate(total=Sum('emissions_kg'))['total'] or 0)
        suppliers_count = getattr(obj, '_suppliers_count', obj.suppliers.count())
        
        return format_html(
            '<div style="font-size: 11px;">'
            '🔥 <strong>{}</strong> calculations<br>'
            '🌍 <strong>{}</strong> kg CO2<br>'
            '🏢 <strong>{}</strong> suppliers'
            '</div>',
            emissions_count, f"{total_co2:.1f}", suppliers_count
        )
    user_stats.short_description = '📊 Statistics'
    
    def activity_status(self, obj):
        if not obj.last_login:
            return format_html('<span style="color: #dc2626;">❌ Never logged in</span>')
        
        days_ago = (timezone.now() - obj.last_login).days
        if days_ago == 0:
            color, status = '#059669', '🟢 Active today'
        elif days_ago <= 7:
            color, status = '#0891b2', f'🔵 {days_ago} days ago'
        elif days_ago <= 30:
            color, status = '#ea580c', f'🟡 {days_ago} days ago'
        else:
            color, status = '#dc2626', f'🔴 {days_ago} days ago'
        
        return format_html('<span style="color: {};">{}</span>', color, status)
    activity_status.short_description = '🔄 Activity Status'
    
    def last_login_formatted(self, obj):
        if obj.last_login:
            return obj.last_login.strftime('%Y/%m/%d - %H:%M')
        return '❌ Never'
    last_login_formatted.short_description = '🕐 Last Login'
    
    def date_joined_formatted(self, obj):
        return obj.date_joined.strftime('%Y/%m/%d - %H:%M')
    date_joined_formatted.short_description = '📅 Date Joined'
    
    def user_actions(self, obj):
        return format_html(
            '<a href="{}" style="background: #3b82f6; color: white; padding: 4px 8px; '
            'border-radius: 4px; text-decoration: none; font-size: 11px;">👁️ Details</a>',
            reverse('admin:auth_user_change', args=[obj.pk])
        )
    user_actions.short_description = '⚡ Actions'
    
    def user_statistics(self, obj):
        """Display complete user statistics"""
        if not obj.pk:
            return "User not saved yet"
        
        # Calculate statistics
        emissions = obj.emission_records.all()
        total_emissions = emissions.aggregate(total=Sum('emissions_kg'))['total'] or 0
        
        # Statistics by Scope
        scope_stats = {}
        for scope in ['1', '2', '3']:
            scope_data = emissions.filter(scope=scope).aggregate(
                count=Count('id'), total=Sum('emissions_kg')
            )
            scope_stats[scope] = {
                'count': scope_data['count'] or 0,
                'total': scope_data['total'] or 0
            }
        
        # Monthly activity
        last_month = timezone.now() - timedelta(days=30)
        recent_activity = emissions.filter(created_at__gte=last_month).count()
        
        # Uploaded files
        uploaded_files = emissions.filter(proof_document__isnull=False).count()
        uploaded_files += obj.custom_factors.filter(certificate_file__isnull=False).count()
        
        return format_html(
            '<div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin: 10px 0;">'
            '<h3 style="margin: 0 0 10px 0; color: #1f2937;">📊 Complete User Statistics</h3>'
            
            '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px;">'
            '<div style="background: white; padding: 10px; border-radius: 6px; text-align: center; border-left: 3px solid #ef4444;">'
            '<div style="font-size: 18px; font-weight: bold; color: #ef4444;">{}</div>'
            '<div style="font-size: 11px; color: #6b7280;">Scope 1</div>'
            '<div style="font-size: 10px; color: #9ca3af;">{} kg CO2</div>'
            '</div>'
            '<div style="background: white; padding: 10px; border-radius: 6px; text-align: center; border-left: 3px solid #f59e0b;">'
            '<div style="font-size: 18px; font-weight: bold; color: #f59e0b;">{}</div>'
            '<div style="font-size: 11px; color: #6b7280;">Scope 2</div>'
            '<div style="font-size: 10px; color: #9ca3af;">{} kg CO2</div>'
            '</div>'
            '<div style="background: white; padding: 10px; border-radius: 6px; text-align: center; border-left: 3px solid #3b82f6;">'
            '<div style="font-size: 18px; font-weight: bold; color: #3b82f6;">{}</div>'
            '<div style="font-size: 11px; color: #6b7280;">Scope 3</div>'
            '<div style="font-size: 10px; color: #9ca3af;">{} kg CO2</div>'
            '</div>'
            '</div>'
            
            '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">'
            '<div style="background: white; padding: 8px; border-radius: 6px; text-align: center;">'
            '<div style="font-size: 16px; font-weight: bold; color: #059669;">{}</div>'
            '<div style="font-size: 10px; color: #6b7280;">Total Calculations</div>'
            '</div>'
            '<div style="background: white; padding: 8px; border-radius: 6px; text-align: center;">'
            '<div style="font-size: 16px; font-weight: bold; color: #0891b2;">{}</div>'
            '<div style="font-size: 10px; color: #6b7280;">Tons CO2 Total</div>'
            '</div>'
            '<div style="background: white; padding: 8px; border-radius: 6px; text-align: center;">'
            '<div style="font-size: 16px; font-weight: bold; color: #7c3aed;">{}</div>'
            '<div style="font-size: 10px; color: #6b7280;">Monthly Activity</div>'
            '</div>'
            '<div style="background: white; padding: 8px; border-radius: 6px; text-align: center;">'
            '<div style="font-size: 16px; font-weight: bold; color: #dc2626;">{}</div>'
            '<div style="font-size: 10px; color: #6b7280;">Files Uploaded</div>'
            '</div>'
            '</div>'
            
            '<div style="margin-top: 10px; font-size: 11px; color: #6b7280;">'
            '🏢 Suppliers: <strong>{}</strong> | '
            '🔧 Custom Factors: <strong>{}</strong> | '
            '📋 Requests: <strong>{}</strong>'
            '</div>'
            '</div>',
            
            scope_stats['1']['count'], f"{scope_stats['1']['total']:.1f}",
            scope_stats['2']['count'], f"{scope_stats['2']['total']:.1f}", 
            scope_stats['3']['count'], f"{scope_stats['3']['total']:.1f}",
            
            emissions.count(),
            f"{total_emissions / 1000:.1f}",
            recent_activity,
            uploaded_files,
            
            obj.suppliers.count(),
            obj.custom_factors.count(),
            obj.material_requests.count()
        )
    user_statistics.short_description = '📊 Complete Statistics'
    
    actions = ['export_users_csv', 'deactivate_users', 'activate_users']
    
    def export_users_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Username', 'Email', 'Full Name', 'Date Joined', 'Last Login',
            'Is Active', 'Total Emissions (kg)', 'Emissions Count', 'Suppliers Count'
        ])
        
        for user in queryset:
            total_emissions = user.emission_records.aggregate(total=Sum('emissions_kg'))['total'] or 0
            writer.writerow([
                user.username, user.email, user.get_full_name(),
                user.date_joined, user.last_login, user.is_active,
                total_emissions, user.emission_records.count(), user.suppliers.count()
            ])
        
        return response
    export_users_csv.short_description = "📊 Export Users to CSV"
    
    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} users deactivated.')
    deactivate_users.short_description = "🔒 Deactivate Users"
    
    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} users activated.')
    activate_users.short_description = "✅ Activate Users"

# Register Custom User Admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(EmissionData)
class EmissionDataAdmin(admin.ModelAdmin):
    list_display = ['country', 'year', 'co2_emissions', 'total_ghg']
    list_filter = ['year', 'country']
    search_fields = ['country__name']

@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = [
        'record_info', 'user_link', 'scope_badge', 'emissions_display', 
        'activity_info', 'country_flag', 'file_status', 'created_at_formatted', 'record_actions'
    ]
    list_filter = [
        'scope', 'category', 'country', 'created_at', 'user', 
        ('proof_document', admin.EmptyFieldListFilter),
        ('supplier', admin.EmptyFieldListFilter)
    ]
    search_fields = [
        'user__username', 'user__email', 'source_name', 'description', 
        'supplier__name', 'industry_type', 'fuel_name'
    ]
    readonly_fields = ['created_at', 'updated_at', 'record_details']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('👤 User Information', {
            'fields': ('user', 'scope')
        }),
        ('🔥 Emission Details', {
            'fields': ('category', 'source', 'source_name', 'activity_data', 'unit'),
            'classes': ('wide',)
        }),
        ('📊 Calculation Results', {
            'fields': ('emission_factor', 'emissions_kg', 'emissions_tons', 'country', 'reference'),
            'classes': ('wide',)
        }),
        ('ℹ️ Additional Information', {
            'fields': ('description', 'industry_type', 'fuel_name', 'supplier', 'proof_document'),
            'classes': ('collapse',)
        }),
        ('📋 Complete Details', {
            'fields': ('record_details',),
            'classes': ('wide',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'supplier').prefetch_related()
    
    def record_info(self, obj):
        return format_html(
            '<div style="font-weight: bold; color: #1f2937;">{}</div>'
            '<div style="font-size: 11px; color: #6b7280;">{}</div>',
            obj.source_name[:30] + ('...' if len(obj.source_name) > 30 else ''),
            obj.category.replace('-', ' ').title()
        )
    record_info.short_description = '🔥 Emission Source'
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.pk])
        return format_html(
            '<a href="{}" style="color: #3b82f6; text-decoration: none;">'
            '<strong>{}</strong></a><br>'
            '<span style="font-size: 10px; color: #6b7280;">{}</span>',
            url, obj.user.username, obj.user.email
        )
    user_link.short_description = '👤 User'
    
    def scope_badge(self, obj):
        colors = {'1': '#ef4444', '2': '#f59e0b', '3': '#3b82f6'}
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">'
            'Scope {}</span>',
            colors.get(obj.scope, '#6b7280'), obj.scope
        )
    scope_badge.short_description = '📊 Scope'
    
    def emissions_display(self, obj):
        return format_html(
            '<div style="text-align: center;">'
            '<div style="font-size: 14px; font-weight: bold; color: #059669;">{}</div>'
            '<div style="font-size: 10px; color: #6b7280;">kg CO2e</div>'
            '<div style="font-size: 12px; color: #0891b2;">{} tons</div>'
            '</div>',
            f"{obj.emissions_kg:,.1f}", f"{obj.emissions_tons:.3f}"
        )
    emissions_display.short_description = '🌍 Emissions'
    
    def activity_info(self, obj):
        return format_html(
            '<div style="font-size: 12px;">'
            '<strong>{}</strong> {}<br>'
            '<span style="color: #6b7280;">Factor: {}</span>'
            '</div>',
            f"{obj.activity_data:,.1f}", obj.unit, obj.emission_factor
        )
    activity_info.short_description = '📈 Activity Data'
    
    def country_flag(self, obj):
        country_flags = {
            'iran': '🇮🇷', 'usa': '🇺🇸', 'uk': '🇬🇧', 'germany': '🇩🇪',
            'france': '🇫🇷', 'global': '🌍', 'turkey': '🇹🇷'
        }
        flag = country_flags.get(obj.country.lower(), '🌍')
        return format_html('{} {}', flag, obj.country.title())
    country_flag.short_description = '🌍 Country'
    
    def file_status(self, obj):
        if obj.proof_document:
            return format_html(
                '<a href="{}" target="_blank" style="color: #059669;">'
                '📄 Has File</a>',
                obj.proof_document.url
            )
        return format_html('<span style="color: #dc2626;">❌ No File</span>')
    file_status.short_description = '📁 File'
    
    def created_at_formatted(self, obj):
        return format_html(
            '<div style="font-size: 11px;">'
            '<div>{}</div>'
            '<div style="color: #6b7280;">{}</div>'
            '</div>',
            obj.created_at.strftime('%Y/%m/%d'),
            obj.created_at.strftime('%H:%M')
        )
    created_at_formatted.short_description = '🕐 Created Date'
    
    def record_actions(self, obj):
        return format_html(
            '<div style="display: flex; gap: 4px;">'
            '<a href="{}" style="background: #3b82f6; color: white; padding: 2px 6px; '
            'border-radius: 3px; text-decoration: none; font-size: 10px;">✏️</a>'
            '</div>',
            reverse('admin:ghg_emissionrecord_change', args=[obj.pk])
        )
    record_actions.short_description = '⚡ Actions'
    
    def record_details(self, obj):
        """Display complete record details"""
        if not obj.pk:
            return "Record not saved yet"
        
        # Calculate percentage of user's total emissions
        user_total = obj.user.emission_records.aggregate(total=Sum('emissions_kg'))['total'] or 0
        percentage = (obj.emissions_kg / user_total * 100) if user_total > 0 else 0
        
        return format_html(
            '<div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin: 10px 0;">'
            '<h3 style="margin: 0 0 15px 0; color: #1f2937;">📋 Complete Record Details</h3>'
            
            '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 15px;">'
            
            '<div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #3b82f6;">'
            '<h4 style="margin: 0 0 8px 0; color: #3b82f6; font-size: 12px;">🔥 Emission Information</h4>'
            '<div style="font-size: 11px; line-height: 1.4;">'
            '<strong>Source:</strong> {}<br>'
            '<strong>Category:</strong> {}<br>'
            '<strong>Scope:</strong> {}<br>'
            '<strong>Share of Total:</strong> {}%'
            '</div>'
            '</div>'
            
            '<div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #059669;">'
            '<h4 style="margin: 0 0 8px 0; color: #059669; font-size: 12px;">📊 Calculations</h4>'
            '<div style="font-size: 11px; line-height: 1.4;">'
            '<strong>Activity Data:</strong> {} {}<br>'
            '<strong>Emission Factor:</strong> {}<br>'
            '<strong>Emissions:</strong> {} kg<br>'
            '<strong>Equivalent:</strong> {} tons CO2e'
            '</div>'
            '</div>'
            
            '<div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #f59e0b;">'
            '<h4 style="margin: 0 0 8px 0; color: #f59e0b; font-size: 12px;">ℹ️ Additional Information</h4>'
            '<div style="font-size: 11px; line-height: 1.4;">'
            '<strong>Country:</strong> {}<br>'
            '<strong>Supplier:</strong> {}<br>'
            '<strong>Industry:</strong> {}<br>'
            '<strong>File:</strong> {}'
            '</div>'
            '</div>'
            
            '</div>'
            
            '{}'
            
            '<div style="margin-top: 15px; padding: 10px; background: #e0f2fe; border-radius: 6px;">'
            '<div style="font-size: 11px; color: #0277bd;">'
            '<strong>📚 Reference:</strong> {}'
            '</div>'
            '</div>'
            '</div>',
            
            obj.source_name,
            obj.category.replace('-', ' ').title(),
            f"Scope {obj.scope}",
            f"{percentage:.1f}",
            
            f"{obj.activity_data:,.1f}", obj.unit,
            obj.emission_factor,
            f"{obj.emissions_kg:,.1f}",
            f"{obj.emissions_tons:.3f}",
            
            obj.country.title(),
            obj.supplier.name if obj.supplier else 'None',
            obj.industry_type or 'Unspecified',
            '✅ Has File' if obj.proof_document else '❌ No File',
            
            f'<div style="margin: 10px 0; padding: 8px; background: #fef3c7; border-radius: 4px; font-size: 11px;"><strong>💬 Description:</strong> {obj.description}</div>' if obj.description else '',
            
            obj.reference or 'No reference specified'
        )
    record_details.short_description = '📋 Complete Details'
    
    actions = ['export_records_csv', 'bulk_verify', 'calculate_totals']
    
    def export_records_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="emission_records.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'User', 'Date', 'Scope', 'Source', 'Activity Data', 'Unit',
            'Emissions (kg)', 'Emissions (tons)', 'Country', 'Supplier', 'Description'
        ])
        
        for record in queryset:
            writer.writerow([
                record.user.username, record.created_at.strftime('%Y-%m-%d'),
                f'Scope {record.scope}', record.source_name, record.activity_data,
                record.unit, record.emissions_kg, record.emissions_tons,
                record.country, record.supplier.name if record.supplier else '',
                record.description or ''
            ])
        
        return response
    export_records_csv.short_description = "📊 Export Records to CSV"
    
    def calculate_totals(self, request, queryset):
        total_kg = queryset.aggregate(total=Sum('emissions_kg'))['total'] or 0
        total_tons = total_kg / 1000
        count = queryset.count()
        
        self.message_user(
            request, 
            f'📊 Selected Statistics: {count} records | {total_kg:,.1f} kg CO2e | {total_tons:.3f} tons CO2e'
        )
    calculate_totals.short_description = "📊 Calculate Total Emissions"

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = [
        'supplier_info', 'user_link', 'contact_details', 'location_info', 
        'business_info', 'usage_stats', 'created_at_formatted', 'supplier_actions'
    ]
    list_filter = [
        'supplier_type', 'country', 'city', 'created_at', 'user'
    ]
    search_fields = [
        'name', 'email', 'contact_person', 'city', 'tax_number', 
        'user__username', 'user__email', 'website'
    ]
    readonly_fields = ['created_at', 'updated_at', 'supplier_analytics']
    list_per_page = 25
    
    fieldsets = (
        ('👤 User Information', {
            'fields': ('user',)
        }),
        ('🏢 Basic Information', {
            'fields': ('name', 'supplier_type'),
            'classes': ('wide',)
        }),
        ('📞 Contact Information', {
            'fields': ('contact_person', 'email', 'phone', 'website'),
            'classes': ('wide',)
        }),
        ('📍 Location', {
            'fields': ('country', 'city', 'address'),
            'classes': ('wide',)
        }),
        ('💼 Business Information', {
            'fields': ('tax_number', 'notes'),
            'classes': ('collapse',)
        }),
        ('📊 Performance Analysis', {
            'fields': ('supplier_analytics',),
            'classes': ('wide',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('emission_records')
    
    def supplier_info(self, obj):
        return format_html(
            '<div style="font-weight: bold; color: #1f2937; font-size: 13px;">{}</div>'
            '<div style="font-size: 11px; color: #6b7280; margin-top: 2px;">'
            '🏷️ {}</div>',
            obj.name[:35] + ('...' if len(obj.name) > 35 else ''),
            obj.supplier_type or 'Type unspecified'
        )
    supplier_info.short_description = '🏢 Supplier'
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.pk])
        return format_html(
            '<a href="{}" style="color: #3b82f6; text-decoration: none;">'
            '<strong>{}</strong></a><br>'
            '<span style="font-size: 10px; color: #6b7280;">{}</span>',
            url, obj.user.username, obj.user.email
        )
    user_link.short_description = '👤 User'
    
    def contact_details(self, obj):
        contact_html = '<div style="font-size: 11px; line-height: 1.3;">'
        
        if obj.contact_person:
            contact_html += f'👤 <strong>{obj.contact_person}</strong><br>'
        
        if obj.email:
            contact_html += f'📧 <a href="mailto:{obj.email}" style="color: #3b82f6;">{obj.email}</a><br>'
        
        if obj.phone:
            contact_html += f'📞 {obj.phone}<br>'
        
        if obj.website:
            contact_html += f'🌐 <a href="{obj.website}" target="_blank" style="color: #059669;">Website</a>'
        
        contact_html += '</div>'
        
        return format_html(contact_html) if any([obj.contact_person, obj.email, obj.phone, obj.website]) else format_html('<span style="color: #dc2626;">❌ Incomplete information</span>')
    contact_details.short_description = '📞 Contact'
    
    def location_info(self, obj):
        location_parts = []
        if obj.city:
            location_parts.append(obj.city)
        if obj.country:
            location_parts.append(obj.country)
        
        if location_parts:
            return format_html(
                '<div style="font-size: 11px;">'
                '📍 {}<br>'
                '{}'
                '</div>',
                ' - '.join(location_parts),
                f'<span style="color: #6b7280;">Full address available</span>' if obj.address else '<span style="color: #f59e0b;">No full address</span>'
            )
        return format_html('<span style="color: #dc2626;">❌ Location unspecified</span>')
    location_info.short_description = '📍 Location'
    
    def business_info(self, obj):
        return format_html(
            '<div style="font-size: 11px;">'
            '🏛️ {}<br>'
            '📝 {}'
            '</div>',
            obj.tax_number if obj.tax_number else '<span style="color: #f59e0b;">No tax ID</span>',
            'Has notes' if obj.notes else '<span style="color: #6b7280;">No notes</span>'
        )
    business_info.short_description = '💼 Business'
    
    def usage_stats(self, obj):
        emissions_count = obj.emission_records.count()
        if emissions_count > 0:
            total_emissions = obj.emission_records.aggregate(total=Sum('emissions_kg'))['total'] or 0
            return format_html(
                '<div style="text-align: center; font-size: 11px;">'
                '<div style="font-weight: bold; color: #059669;">{}</div>'
                '<div style="color: #6b7280;">calculations</div>'
                '<div style="font-size: 10px; color: #0891b2;">{} kg CO2</div>'
                '</div>',
                emissions_count, f"{total_emissions:.1f}"
            )
        return format_html('<span style="color: #6b7280; font-size: 11px;">🔄 Not used</span>')
    usage_stats.short_description = '📊 Usage'
    
    def created_at_formatted(self, obj):
        return format_html(
            '<div style="font-size: 11px;">'
            '<div>{}</div>'
            '<div style="color: #6b7280;">{}</div>'
            '</div>',
            obj.created_at.strftime('%Y/%m/%d'),
            obj.created_at.strftime('%H:%M')
        )
    created_at_formatted.short_description = '🕐 Created Date'
    
    def supplier_actions(self, obj):
        return format_html(
            '<div style="display: flex; gap: 4px;">'
            '<a href="{}" style="background: #3b82f6; color: white; padding: 2px 6px; '
            'border-radius: 3px; text-decoration: none; font-size: 10px;">✏️</a>'
            '</div>',
            reverse('admin:ghg_supplier_change', args=[obj.pk])
        )
    supplier_actions.short_description = '⚡ Actions'
    
    def supplier_analytics(self, obj):
        """Complete supplier performance analysis"""
        if not obj.pk:
            return "Supplier not saved yet"
        
        emissions = obj.emission_records.all()
        total_emissions = emissions.aggregate(total=Sum('emissions_kg'))['total'] or 0
        
        # Monthly statistics
        last_month = timezone.now() - timedelta(days=30)
        recent_usage = emissions.filter(created_at__gte=last_month).count()
        
        # Statistics by Scope
        scope_stats = {}
        for scope in ['1', '2', '3']:
            scope_data = emissions.filter(scope=scope).aggregate(
                count=Count('id'), total=Sum('emissions_kg')
            )
            scope_stats[scope] = {
                'count': scope_data['count'] or 0,
                'total': scope_data['total'] or 0
            }
        
        return format_html(
            '<div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin: 10px 0;">'
            '<h3 style="margin: 0 0 15px 0; color: #1f2937;">📊 Supplier Performance Analysis</h3>'
            
            '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 15px;">'
            '<div style="background: white; padding: 10px; border-radius: 6px; text-align: center; border-left: 3px solid #059669;">'
            '<div style="font-size: 18px; font-weight: bold; color: #059669;">{}</div>'
            '<div style="font-size: 11px; color: #6b7280;">Total Usage</div>'
            '</div>'
            '<div style="background: white; padding: 10px; border-radius: 6px; text-align: center; border-left: 3px solid #0891b2;">'
            '<div style="font-size: 18px; font-weight: bold; color: #0891b2;">{}</div>'
            '<div style="font-size: 11px; color: #6b7280;">Tons CO2 Total</div>'
            '</div>'
            '<div style="background: white; padding: 10px; border-radius: 6px; text-align: center; border-left: 3px solid #7c3aed;">'
            '<div style="font-size: 18px; font-weight: bold; color: #7c3aed;">{}</div>'
            '<div style="font-size: 11px; color: #6b7280;">Monthly Usage</div>'
            '</div>'
            '<div style="background: white; padding: 10px; border-radius: 6px; text-align: center; border-left: 3px solid #f59e0b;">'
            '<div style="font-size: 18px; font-weight: bold; color: #f59e0b;">{}</div>'
            '<div style="font-size: 11px; color: #6b7280;">Share of Total</div>'
            '</div>'
            '</div>'
            
            '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">'
            '<div style="background: white; padding: 8px; border-radius: 6px; text-align: center; border-left: 3px solid #ef4444;">'
            '<div style="font-size: 14px; font-weight: bold; color: #ef4444;">{}</div>'
            '<div style="font-size: 10px; color: #6b7280;">Scope 1</div>'
            '</div>'
            '<div style="background: white; padding: 8px; border-radius: 6px; text-align: center; border-left: 3px solid #f59e0b;">'
            '<div style="font-size: 14px; font-weight: bold; color: #f59e0b;">{}</div>'
            '<div style="font-size: 10px; color: #6b7280;">Scope 2</div>'
            '</div>'
            '<div style="background: white; padding: 8px; border-radius: 6px; text-align: center; border-left: 3px solid #3b82f6;">'
            '<div style="font-size: 14px; font-weight: bold; color: #3b82f6;">{}</div>'
            '<div style="font-size: 10px; color: #6b7280;">Scope 3</div>'
            '</div>'
            '</div>'
            '</div>',
            
            emissions.count(),
            f"{total_emissions / 1000:.1f}",
            recent_usage,
            f"{(total_emissions / obj.user.emission_records.aggregate(total=Sum('emissions_kg'))['total'] * 100) if obj.user.emission_records.aggregate(total=Sum('emissions_kg'))['total'] else 0:.1f}",
            
            scope_stats['1']['count'],
            scope_stats['2']['count'],
            scope_stats['3']['count']
        )
    supplier_analytics.short_description = '📊 Performance Analysis'
    
    actions = ['export_suppliers_csv', 'send_contact_email']
    
    def export_suppliers_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="suppliers_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Type', 'Contact Person', 'Email', 'Phone', 'Country', 
            'City', 'Tax Number', 'Usage Count', 'Total Emissions (kg)', 'User'
        ])
        
        for supplier in queryset:
            usage_count = supplier.emission_records.count()
            total_emissions = supplier.emission_records.aggregate(total=Sum('emissions_kg'))['total'] or 0
            
            writer.writerow([
                supplier.name, supplier.supplier_type, supplier.contact_person,
                supplier.email, supplier.phone, supplier.country, supplier.city,
                supplier.tax_number, usage_count, total_emissions, supplier.user.username
            ])
        
        return response
    export_suppliers_csv.short_description = "📊 Export Suppliers to CSV"


@admin.register(CustomEmissionFactor)
class CustomEmissionFactorAdmin(admin.ModelAdmin):
    list_display = [
        'factor_info', 'user_link', 'factor_details', 'verification_status', 
        'usage_stats', 'file_status', 'created_at_formatted', 'factor_actions'
    ]
    list_filter = [
        'is_verified', 'category', 'created_at', 'user',
        ('certificate_file', admin.EmptyFieldListFilter)
    ]
    search_fields = [
        'name', 'user__username', 'description', 'category', 'reference_source'
    ]
    readonly_fields = ['created_at', 'updated_at', 'factor_analytics']
    list_per_page = 25
    
    fieldsets = (
        ('👤 User Information', {
            'fields': ('user',)
        }),
        ('🔧 Factor Information', {
            'fields': ('name', 'category', 'description'),
            'classes': ('wide',)
        }),
        ('📊 Emission Factor', {
            'fields': ('factor_value', 'unit', 'reference_source', 'certificate_file'),
            'classes': ('wide',)
        }),
        ('✅ Verification', {
            'fields': ('is_verified',),
            'classes': ('wide',)
        }),
        ('📈 Usage Analysis', {
            'fields': ('factor_analytics',),
            'classes': ('wide',)
        }),
        ('🕐 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def factor_info(self, obj):
        return format_html(
            '<div style="font-weight: bold; color: #1f2937; font-size: 13px;">{}</div>'
            '<div style="font-size: 11px; color: #6b7280; margin-top: 2px;">'
            '🏷️ {}</div>',
            obj.name[:40] + ('...' if len(obj.name) > 40 else ''),
            obj.category.replace('-', ' ').title()
        )
    factor_info.short_description = '🔧 Factor'
    
    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.pk])
        return format_html(
            '<a href="{}" style="color: #3b82f6; text-decoration: none;">'
            '<strong>{}</strong></a><br>'
            '<span style="font-size: 10px; color: #6b7280;">{}</span>',
            url, obj.user.username, obj.user.email
        )
    user_link.short_description = '👤 User'
    
    def factor_details(self, obj):
        return format_html(
            '<div style="text-align: center; font-size: 12px;">'
            '<div style="font-size: 14px; font-weight: bold; color: #059669;">{}</div>'
            '<div style="color: #6b7280; font-size: 10px;">{}</div>'
            '<div style="color: #0891b2; font-size: 11px; margin-top: 2px;">kg CO2e per {}</div>'
            '</div>',
            obj.factor_value, obj.unit, obj.unit
        )
    factor_details.short_description = '📊 Value'
    
    def verification_status(self, obj):
        if obj.is_verified:
            return format_html(
                '<span style="background: #059669; color: white; padding: 4px 8px; '
                'border-radius: 12px; font-size: 11px; font-weight: bold;">'
                '✅ Verified</span>'
            )
        return format_html(
            '<span style="background: #f59e0b; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">'
            '⏳ Pending</span>'
        )
    verification_status.short_description = '✅ Status'
    
    def usage_stats(self, obj):
        # Assume relationship with EmissionRecord exists
        # usage_count = obj.emission_records.count() if hasattr(obj, 'emission_records') else 0
        usage_count = 0  # Temporarily zero
        
        if usage_count > 0:
            return format_html(
                '<div style="text-align: center; font-size: 11px;">'
                '<div style="font-weight: bold; color: #059669;">{}</div>'
                '<div style="color: #6b7280;">usage</div>'
                '</div>',
                usage_count
            )
        return format_html('<span style="color: #6b7280; font-size: 11px;">🔄 Not used</span>')
    usage_stats.short_description = '📈 Usage'
    
    def file_status(self, obj):
        if obj.certificate_file:
            return format_html(
                '<a href="{}" target="_blank" style="color: #059669;">'
                '📄 Certificate</a>',
                obj.certificate_file.url
            )
        return format_html('<span style="color: #dc2626;">❌ No Certificate</span>')
    file_status.short_description = '📁 File'
    
    def created_at_formatted(self, obj):
        return format_html(
            '<div style="font-size: 11px;">'
            '<div>{}</div>'
            '<div style="color: #6b7280;">{}</div>'
            '</div>',
            obj.created_at.strftime('%Y/%m/%d'),
            obj.created_at.strftime('%H:%M')
        )
    created_at_formatted.short_description = '🕐 Created Date'
    
    def factor_actions(self, obj):
        verify_style = 'background: #059669;' if not obj.is_verified else 'background: #6b7280;'
        return format_html(
            '<div style="display: flex; gap: 4px;">'
            '<a href="{}" style="background: #3b82f6; color: white; padding: 2px 6px; '
            'border-radius: 3px; text-decoration: none; font-size: 10px;">✏️</a>'
            '</div>',
            reverse('admin:ghg_customemissionfactor_change', args=[obj.pk])
        )
    factor_actions.short_description = '⚡ Actions'
    
    def factor_analytics(self, obj):
        """Complete custom factor analysis"""
        if not obj.pk:
            return "Factor not saved yet"
        
        return format_html(
            '<div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin: 10px 0;">'
            '<h3 style="margin: 0 0 15px 0; color: #1f2937;">📊 Custom Factor Analysis</h3>'
            
            '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">'
            
            '<div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #3b82f6;">'
            '<h4 style="margin: 0 0 8px 0; color: #3b82f6; font-size: 12px;">🔧 Technical Specifications</h4>'
            '<div style="font-size: 11px; line-height: 1.4;">'
            '<strong>Name:</strong> {}<br>'
            '<strong>Category:</strong> {}<br>'
            '<strong>Value:</strong> {} {}<br>'
            '<strong>Status:</strong> {}'
            '</div>'
            '</div>'
            
            '<div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #059669;">'
            '<h4 style="margin: 0 0 8px 0; color: #059669; font-size: 12px;">📚 Documentation</h4>'
            '<div style="font-size: 11px; line-height: 1.4;">'
            '<strong>Reference:</strong> {}<br>'
            '<strong>Certificate:</strong> {}<br>'
            '<strong>Description:</strong> {}'
            '</div>'
            '</div>'
            
            '<div style="background: white; padding: 12px; border-radius: 6px; border-left: 4px solid #f59e0b;">'
            '<h4 style="margin: 0 0 8px 0; color: #f59e0b; font-size: 12px;">📈 Usage Statistics</h4>'
            '<div style="font-size: 11px; line-height: 1.4;">'
            '<strong>Usage Count:</strong> 0<br>'
            '<strong>Last Used:</strong> Never<br>'
            '<strong>Popularity:</strong> New'
            '</div>'
            '</div>'
            
            '</div>'
            '</div>',
            
            obj.name,
            obj.category.replace('-', ' ').title(),
            obj.factor_value, obj.unit,
            'Verified' if obj.is_verified else 'Pending Verification',
            
            obj.reference_source[:50] + '...' if obj.reference_source and len(obj.reference_source) > 50 else obj.reference_source or 'Unspecified',
            'Available' if obj.certificate_file else 'Not Available',
            obj.description[:50] + '...' if obj.description and len(obj.description) > 50 else obj.description or 'Not Available'
        )
    factor_analytics.short_description = '📊 Complete Analysis'
    
    actions = ['verify_factors', 'export_factors_csv']
    
    def verify_factors(self, request, queryset):
        count = queryset.update(is_verified=True)
        self.message_user(request, f"✅ {count} custom factors verified.")
    verify_factors.short_description = "✅ Verify Selected Factors"
    
    def export_factors_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="custom_factors_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Category', 'Factor Value', 'Unit', 'Is Verified', 
            'Reference Source', 'User', 'Created Date'
        ])
        
        for factor in queryset:
            writer.writerow([
                factor.name, factor.category, factor.factor_value, factor.unit,
                'Yes' if factor.is_verified else 'No', factor.reference_source or '',
                factor.user.username, factor.created_at.strftime('%Y-%m-%d')
            ])
        
        return response
    export_factors_csv.short_description = "📊 Export Factors to CSV"


@admin.register(MaterialRequest)
class MaterialRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'request_type', 'status_badge', 'created_at']
    list_filter = ['status', 'request_type', 'created_at']
    search_fields = ['name', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'request_type', 'name', 'description')
        }),
        ('Additional Information', {
            'fields': ('additional_info',)
        }),
        ('Admin Review', {
            'fields': ('status', 'admin_notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_requests', 'reject_requests']
    
    def status_badge(self, obj):
        colors = {
            'pending': '#fbbf24',
            'approved': '#22c55e',
            'rejected': '#ef4444',
            'in_progress': '#3b82f6',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def approve_requests(self, request, queryset):
        from .notifications import send_material_request_status_notification
        for req in queryset:
            req.approve(request.user, 'Approved via admin action')
            # Send notification to user
            try:
                send_material_request_status_notification(req)
            except Exception as e:
                logger.error(f"Failed to send notification: {str(e)}")
        self.message_user(request, f"{queryset.count()} requests approved.")
    approve_requests.short_description = "Approve selected requests"
    
    def reject_requests(self, request, queryset):
        from .notifications import send_material_request_status_notification
        for req in queryset:
            req.reject(request.user, 'Rejected via admin action')
            # Send notification to user
            try:
                send_material_request_status_notification(req)
            except Exception as e:
                logger.error(f"Failed to send notification: {str(e)}")
        self.message_user(request, f"{queryset.count()} requests rejected.")
    reject_requests.short_description = "Reject selected requests"
    
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, f"{queryset.count()} requests marked as in progress.")
    mark_in_progress.short_description = "Mark as in progress"


@admin.register(ReportExtraInfo)
class ReportExtraInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'legal_name', 'industry', 'boundary_approach', 'has_consent', 'created_at']
    list_filter = ['boundary_approach', 'share_org_profile', 'share_boundary', 'created_at']
    search_fields = ['user__username', 'legal_name', 'industry']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Organization Details', {
            'fields': ('legal_name', 'industry')
        }),
        ('Reporting Information', {
            'fields': ('reporting_period', 'boundary_approach', 'notes')
        }),
        ('Consent Settings', {
            'fields': ('share_org_profile', 'share_boundary', 'share_data_sources', 'share_projects')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_consent(self, obj):
        """Show if user has given any consent"""
        return obj.share_org_profile or obj.share_boundary or obj.share_data_sources or obj.share_projects
    has_consent.boolean = True
    has_consent.short_description = 'Has Consent'


@admin.register(IndustryType)
class IndustryTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'requested_by', 'created_at']
    list_filter = ['is_active', 'created_at', 'requested_by']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Industry Information', {
            'fields': ('name', 'code', 'description', 'is_active')
        }),
        ('Request Information', {
            'fields': ('requested_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(IndustryRequest)
class IndustryRequestAdmin(admin.ModelAdmin):
    list_display = ['industry_name', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['industry_name', 'user__email', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Request Details', {
            'fields': ('user', 'industry_name', 'industry_code', 'description', 'business_context')
        }),
        ('Admin Review', {
            'fields': ('status', 'admin_notes', 'approved_industry')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        """Approve selected industry requests"""
        approved_count = 0
        for industry_request in queryset.filter(status='pending'):
            # Create the industry type
            industry_type, created = IndustryType.objects.get_or_create(
                name=industry_request.industry_name,
                defaults={
                    'code': industry_request.industry_code,
                    'description': industry_request.description,
                    'requested_by': industry_request.user,
                    'is_active': True,
                }
            )
            
            # Update the request
            industry_request.status = 'approved'
            industry_request.approved_industry = industry_type
            industry_request.admin_notes = f'Approved via bulk action on {timezone.now().strftime("%Y-%m-%d")}'
            industry_request.save()
            
            # Send notification to user
            try:
                from .notifications import send_industry_status_notification
                send_industry_status_notification(industry_request)
            except Exception as e:
                logger.error(f"Failed to send approval notification: {str(e)}")
            
            approved_count += 1
        
        self.message_user(request, f"Successfully approved {approved_count} industry requests.")
    approve_requests.short_description = "✅ Approve selected industry requests"
    
    def reject_requests(self, request, queryset):
        """Reject selected industry requests"""
        rejected_count = 0
        for industry_request in queryset.filter(status='pending'):
            industry_request.status = 'rejected'
            industry_request.admin_notes = f'Rejected via bulk action on {timezone.now().strftime("%Y-%m-%d")} - Please review and resubmit with more details.'
            industry_request.save()
            
            # Send notification to user
            try:
                from .notifications import send_industry_status_notification
                send_industry_status_notification(industry_request)
            except Exception as e:
                logger.error(f"Failed to send rejection notification: {str(e)}")
            
            rejected_count += 1
        
        self.message_user(request, f"Successfully rejected {rejected_count} industry requests.")
    reject_requests.short_description = "❌ Reject selected industry requests"
    def has_consent(self, obj):
        consent_count = sum([
            obj.share_org_profile,
            obj.share_boundary,
            obj.share_data_sources,
            obj.share_projects
        ])
        return format_html(
            '<span style="color: {};">{}/4 consents</span>',
            '#22c55e' if consent_count >= 2 else '#f59e0b',
            consent_count
        )
    has_consent.short_description = 'Consent Status'
