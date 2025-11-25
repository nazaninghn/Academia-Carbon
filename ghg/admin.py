from django.contrib import admin
from .models import Country, EmissionData, EmissionRecord, Supplier

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
            'fields': ('description', 'supplier')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'supplier_type', 'email', 'phone', 'created_at']
    list_filter = ['supplier_type', 'created_at', 'user']
    search_fields = ['name', 'email', 'contact_person']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'supplier_type')
        }),
        ('Contact Details', {
            'fields': ('contact_person', 'email', 'phone', 'address')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
