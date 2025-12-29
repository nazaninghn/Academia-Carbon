from django.contrib import admin
from django.utils.html import format_html
from .models import Country, EmissionData, EmissionRecord, Supplier, CustomEmissionFactor, MaterialRequest, ReportExtraInfo
import logging

logger = logging.getLogger(__name__)

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
    list_display = ['user', 'scope', 'source_name', 'emissions_kg', 'country', 'created_at']
    list_filter = ['scope', 'country', 'created_at', 'user']
    search_fields = ['user__username', 'source_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'scope')
        }),
        ('Emission Details', {
            'fields': ('category', 'source', 'source_name', 'activity_data', 'unit')
        }),
        ('Calculation Results', {
            'fields': ('emission_factor', 'emissions_kg', 'emissions_tons', 'country', 'reference')
        }),
        ('Additional Information', {
            'fields': ('description', 'industry_type', 'fuel_name', 'supplier')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'supplier_type', 'country', 'city', 'email', 'phone', 'created_at']
    list_filter = ['supplier_type', 'country', 'created_at', 'user']
    search_fields = ['name', 'email', 'contact_person', 'city', 'tax_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'supplier_type')
        }),
        ('Contact Details', {
            'fields': ('contact_person', 'email', 'phone', 'website')
        }),
        ('Location', {
            'fields': ('country', 'city', 'address')
        }),
        ('Business Information', {
            'fields': ('tax_number', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CustomEmissionFactor)
class CustomEmissionFactorAdmin(admin.ModelAdmin):
    list_display = ['material_name', 'user', 'emission_factor', 'unit', 'category', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'category', 'created_at']
    search_fields = ['material_name', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at', 'verified_at', 'verified_by']
    
    fieldsets = (
        ('Material Information', {
            'fields': ('user', 'supplier', 'material_name', 'category', 'description')
        }),
        ('Emission Factor', {
            'fields': ('emission_factor', 'unit', 'source_reference', 'certificate_file')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verified_by', 'verified_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['verify_factors']
    
    def verify_factors(self, request, queryset):
        for factor in queryset:
            factor.verify(request.user)
        self.message_user(request, f"{queryset.count()} custom factors verified successfully.")
    verify_factors.short_description = "Verify selected custom factors"


@admin.register(MaterialRequest)
class MaterialRequestAdmin(admin.ModelAdmin):
    list_display = ['material_name', 'user', 'category', 'status_badge', 'created_at', 'reviewed_by']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['material_name', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at', 'reviewed_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'material_name', 'category', 'description')
        }),
        ('User Suggestions', {
            'fields': ('suggested_factor', 'suggested_unit', 'suggested_source')
        }),
        ('Admin Review', {
            'fields': ('status', 'admin_notes', 'reviewed_by', 'reviewed_at')
        }),
        ('System Integration', {
            'fields': ('added_to_system', 'system_source_key')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_requests', 'reject_requests', 'mark_in_progress']
    
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
