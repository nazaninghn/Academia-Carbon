from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    class Meta:
        verbose_name_plural = "Countries"
    
    def __str__(self):
        return self.name

class EmissionData(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    year = models.IntegerField()
    co2_emissions = models.FloatField(help_text="CO2 emissions in million tonnes")
    methane_emissions = models.FloatField(help_text="CH4 emissions in million tonnes", null=True, blank=True)
    nitrous_oxide = models.FloatField(help_text="N2O emissions in million tonnes", null=True, blank=True)
    total_ghg = models.FloatField(help_text="Total GHG emissions in CO2 equivalent")
    
    class Meta:
        ordering = ['-year']
        unique_together = ['country', 'year']
    
    def __str__(self):
        return f"{self.country.name} - {self.year}"


class Supplier(models.Model):
    """Supplier/Vendor management for emission tracking"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suppliers')
    name = models.CharField(max_length=200, help_text="Supplier/Vendor name")
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    supplier_type = models.CharField(max_length=100, blank=True, null=True, 
                                     help_text="e.g., Energy, Fuel, Transportation")
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        unique_together = ['user', 'name']
    
    def __str__(self):
        return self.name


class EmissionRecord(models.Model):
    """Store user emission calculations"""
    SCOPE_CHOICES = [
        ('1', 'Scope 1 - Direct Emissions'),
        ('2', 'Scope 2 - Indirect Emissions (Energy)'),
        ('3', 'Scope 3 - Other Indirect Emissions'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emission_records')
    scope = models.CharField(max_length=1, choices=SCOPE_CHOICES)
    category = models.CharField(max_length=50, help_text="e.g., stationary, mobile, electricity")
    source = models.CharField(max_length=100, help_text="e.g., diesel, natural-gas")
    source_name = models.CharField(max_length=200, help_text="Display name of source")
    
    activity_data = models.FloatField(help_text="Amount of activity")
    unit = models.CharField(max_length=20, help_text="Unit of measurement")
    
    emission_factor = models.FloatField(help_text="Emission factor used")
    emissions_kg = models.FloatField(help_text="Total emissions in kg CO2e")
    emissions_tons = models.FloatField(help_text="Total emissions in tons CO2e")
    
    country = models.CharField(max_length=50, default='global', help_text="Country for emission factors")
    reference = models.TextField(blank=True, null=True, help_text="Reference source for emission factor")
    
    description = models.TextField(blank=True, null=True, help_text="Optional description")
    supplier_old = models.CharField(max_length=200, blank=True, null=True, help_text="Supplier name (deprecated)")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, 
                                 related_name='emission_records', help_text="Supplier/Vendor")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Emission Record"
        verbose_name_plural = "Emission Records"
    
    def __str__(self):
        return f"{self.user.username} - {self.source_name} - {self.emissions_kg} kg CO2e"
    
    def get_scope_display_short(self):
        return f"Scope {self.scope}"
