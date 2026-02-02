"""
Emission Sources Management Models
Models for managing emission sources in admin panel
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class EmissionScope(models.Model):
    """
    Emission Scopes (1, 2, 3)
    """
    SCOPE_CHOICES = [
        ('1', 'Scope 1 - Direct Emissions'),
        ('2', 'Scope 2 - Indirect Emissions (Energy)'),
        ('3', 'Scope 3 - Other Indirect Emissions'),
    ]
    
    scope_number = models.CharField(
        max_length=1, 
        choices=SCOPE_CHOICES, 
        unique=True,
        verbose_name="Scope Number"
    )
    name_en = models.CharField(max_length=200, verbose_name="Name (English)")
    name_tr = models.CharField(max_length=200, blank=True, null=True, verbose_name="Name (Turkish)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Description (English)")
    description_tr = models.TextField(blank=True, null=True, verbose_name="Description (Turkish)")
    
    icon = models.CharField(max_length=50, default='🔥', verbose_name="Icon/Emoji")
    color = models.CharField(max_length=7, default='#3b82f6', verbose_name="Color (Hex)")
    
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    display_order = models.IntegerField(default=0, verbose_name="Display Order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_scopes')
    
    class Meta:
        ordering = ['scope_number']
        verbose_name = "Emission Scope"
        verbose_name_plural = "Emission Scopes"
    
    def __str__(self):
        return f"Scope {self.scope_number} - {self.name_en}"


class EmissionCategory(models.Model):
    """
    Main emission categories
    e.g., Stationary Combustion, Mobile Combustion, Electricity
    """
    scope = models.ForeignKey(
        EmissionScope, 
        on_delete=models.CASCADE, 
        related_name='categories',
        verbose_name="Scope"
    )
    
    code = models.CharField(max_length=50, unique=True, verbose_name="Category Code")
    name_en = models.CharField(max_length=200, verbose_name="Name (English)")
    name_tr = models.CharField(max_length=200, blank=True, null=True, verbose_name="Name (Turkish)")
    
    description_en = models.TextField(blank=True, null=True, verbose_name="Description (English)")
    description_tr = models.TextField(blank=True, null=True, verbose_name="Description (Turkish)")
    
    icon = models.CharField(max_length=50, default='📊', verbose_name="Icon/Emoji")
    
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    display_order = models.IntegerField(default=0, verbose_name="Display Order")
    
    # Metadata
    methodology_notes = models.TextField(blank=True, null=True, verbose_name="Methodology Notes")
    reference_standard = models.CharField(max_length=200, blank=True, null=True, verbose_name="Reference Standard")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_categories')
    
    class Meta:
        ordering = ['scope', 'display_order', 'name_en']
        verbose_name = "Emission Category"
        verbose_name_plural = "Emission Categories"
        unique_together = ['scope', 'code']
    
    def __str__(self):
        return f"{self.scope.scope_number}.{self.code} - {self.name_en}"


class EmissionSource(models.Model):
    """
    Emission sources (subcategories)
    e.g., Natural Gas, Diesel, Petrol, Coal
    """
    category = models.ForeignKey(
        EmissionCategory, 
        on_delete=models.CASCADE, 
        related_name='sources',
        verbose_name="Category"
    )
    
    code = models.CharField(max_length=50, verbose_name="Source Code")
    name_en = models.CharField(max_length=200, verbose_name="Name (English)")
    name_tr = models.CharField(max_length=200, blank=True, null=True, verbose_name="Name (Turkish)")
    
    description_en = models.TextField(blank=True, null=True, verbose_name="Description (English)")
    description_tr = models.TextField(blank=True, null=True, verbose_name="Description (Turkish)")
    
    # Unit information
    default_unit = models.CharField(max_length=50, verbose_name="Default Unit", help_text="e.g., liters, kWh, kg")
    alternative_units = models.JSONField(
        default=list, 
        blank=True,
        verbose_name="Alternative Units",
        help_text="JSON array of alternative units"
    )
    
    icon = models.CharField(max_length=50, default='⚡', verbose_name="Icon/Emoji")
    
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    display_order = models.IntegerField(default=0, verbose_name="Display Order")
    
    # Additional fields
    requires_industry_type = models.BooleanField(default=False, verbose_name="Requires Industry Type")
    requires_fuel_name = models.BooleanField(default=False, verbose_name="Requires Fuel Name")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_sources')
    
    class Meta:
        ordering = ['category', 'display_order', 'name_en']
        verbose_name = "Emission Source"
        verbose_name_plural = "Emission Sources"
        unique_together = ['category', 'code']
    
    def __str__(self):
        return f"{self.category.code}.{self.code} - {self.name_en}"
    
    def get_scope(self):
        return self.category.scope


class EmissionFactorData(models.Model):
    """
    Emission factors for each source
    Can have multiple factors for different countries
    """
    source = models.ForeignKey(
        EmissionSource, 
        on_delete=models.CASCADE, 
        related_name='emission_factors',
        verbose_name="Emission Source"
    )
    
    # Country/Region specific
    country_code = models.CharField(
        max_length=10, 
        default='global',
        verbose_name="Country Code",
        help_text="ISO country code or 'global'"
    )
    country_name = models.CharField(max_length=100, default='Global', verbose_name="Country Name")
    
    # Emission factor value
    factor_value = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name="Emission Factor",
        help_text="kg CO2e per unit"
    )
    unit = models.CharField(max_length=50, verbose_name="Unit")
    
    # GHG breakdown (optional)
    co2_factor = models.FloatField(null=True, blank=True, verbose_name="CO2 Factor")
    ch4_factor = models.FloatField(null=True, blank=True, verbose_name="CH4 Factor")
    n2o_factor = models.FloatField(null=True, blank=True, verbose_name="N2O Factor")
    
    # Metadata
    reference_source = models.CharField(
        max_length=500, 
        blank=True, 
        null=True,
        verbose_name="Reference Source",
        help_text="e.g., IPCC 2006, DESNZ 2024"
    )
    reference_year = models.IntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(2000), MaxValueValidator(2100)],
        verbose_name="Reference Year"
    )
    methodology = models.TextField(blank=True, null=True, verbose_name="Methodology")
    
    # Validity period
    valid_from = models.DateField(null=True, blank=True, verbose_name="Valid From")
    valid_to = models.DateField(null=True, blank=True, verbose_name="Valid To")
    
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    is_default = models.BooleanField(default=False, verbose_name="Is Default Factor")
    
    # Quality indicators
    uncertainty_percentage = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Uncertainty %"
    )
    data_quality_rating = models.CharField(
        max_length=20,
        choices=[
            ('high', 'High Quality'),
            ('medium', 'Medium Quality'),
            ('low', 'Low Quality'),
            ('estimated', 'Estimated'),
        ],
        default='medium',
        verbose_name="Data Quality"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_factors')
    
    class Meta:
        ordering = ['source', 'country_code', '-reference_year']
        verbose_name = "Emission Factor Data"
        verbose_name_plural = "Emission Factor Data"
        indexes = [
            models.Index(fields=['source', 'country_code', 'is_active']),
            models.Index(fields=['is_default', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.source.name_en} ({self.country_name}): {self.factor_value} kg CO2e/{self.unit}"
    
    def save(self, *args, **kwargs):
        # If this is set as default, unset other defaults for same source/country
        if self.is_default:
            EmissionFactorData.objects.filter(
                source=self.source,
                country_code=self.country_code,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        
        super().save(*args, **kwargs)


class EmissionCalculationLog(models.Model):
    """
    Emission calculation logs - for tracking and audit
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calculation_logs')
    
    source = models.ForeignKey(EmissionSource, on_delete=models.SET_NULL, null=True)
    factor_used = models.ForeignKey(EmissionFactorData, on_delete=models.SET_NULL, null=True)
    
    activity_data = models.FloatField(verbose_name="Activity Data")
    unit = models.CharField(max_length=50, verbose_name="Unit")
    
    calculated_emissions_kg = models.FloatField(verbose_name="Emissions (kg CO2e)")
    
    calculation_method = models.CharField(max_length=100, default='direct', verbose_name="Calculation Method")
    
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Calculation Log"
        verbose_name_plural = "Calculation Logs"
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['source', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.source} - {self.created_at.strftime('%Y-%m-%d')}"
