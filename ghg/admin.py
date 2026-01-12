from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Country, EmissionData, EmissionRecord, Supplier, CustomEmissionFactor, MaterialRequest, ReportExtraInfo, IndustryType, IndustryRequest
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
    list_display = ['name', 'user', 'factor_value', 'unit', 'category', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'category', 'created_at']
    search_fields = ['name', 'user__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Material Information', {
            'fields': ('user', 'name', 'category', 'description')
        }),
        ('Emission Factor', {
            'fields': ('factor_value', 'unit', 'reference_source', 'certificate_file')
        }),
        ('Verification', {
            'fields': ('is_verified',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['verify_factors']
    
    def verify_factors(self, request, queryset):
        queryset.update(is_verified=True)
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
