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
    contact_person = models.CharField(max_length=100, blank=True, null=True, help_text="Primary contact name")
    email = models.EmailField(blank=True, null=True, help_text="Primary contact email")
    phone = models.CharField(max_length=50, blank=True, null=True, help_text="Phone number with country code")
    supplier_type = models.CharField(max_length=100, blank=True, null=True, 
                                     help_text="Activity/Type: Energy, Fuel, Transportation, etc.")
    country = models.CharField(max_length=100, blank=True, null=True, help_text="Country")
    city = models.CharField(max_length=100, blank=True, null=True, help_text="City")
    tax_number = models.CharField(max_length=100, blank=True, null=True, help_text="Tax/VAT number")
    website = models.URLField(blank=True, null=True, help_text="Company website")
    address = models.TextField(blank=True, null=True, help_text="Full address")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes")
    
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
    industry_type = models.CharField(max_length=100, blank=True, null=True, help_text="Industry type (for specific sources)")
    fuel_name = models.CharField(max_length=100, blank=True, null=True, help_text="Fuel name (for Off-Road)")
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


class CustomEmissionFactor(models.Model):
    """Custom emission factors provided by suppliers or calculated by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_factors')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True, 
                                 related_name='custom_factors', help_text="Supplier who provided this factor")
    
    # Material/Source information
    material_name = models.CharField(max_length=200, help_text="Name of material/product")
    category = models.CharField(max_length=50, help_text="Category (e.g., purchased-goods, stationary)")
    description = models.TextField(blank=True, null=True, help_text="Detailed description")
    
    # Emission factor details
    emission_factor = models.FloatField(help_text="Emission factor value (kg CO2e per unit)")
    unit = models.CharField(max_length=20, help_text="Unit of measurement (kg, liters, m3, etc.)")
    
    # Source/Reference
    source_reference = models.TextField(blank=True, null=True, 
                                       help_text="Reference/source of this emission factor (e.g., supplier certificate, LCA study)")
    certificate_file = models.FileField(upload_to='emission_certificates/', blank=True, null=True,
                                       help_text="Upload certificate or documentation")
    
    # Verification status
    is_verified = models.BooleanField(default=False, help_text="Verified by admin")
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='verified_factors', help_text="Admin who verified")
    verified_at = models.DateTimeField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Custom Emission Factor"
        verbose_name_plural = "Custom Emission Factors"
    
    def __str__(self):
        return f"{self.material_name} - {self.emission_factor} kg CO2e/{self.unit}"
    
    def verify(self, admin_user):
        """Verify this custom factor"""
        self.is_verified = True
        self.verified_by = admin_user
        self.verified_at = timezone.now()
        self.save()


class MaterialRequest(models.Model):
    """Requests for new materials/sources not in the system"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved - Factor Added'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='material_requests')
    
    # Material information
    material_name = models.CharField(max_length=200, help_text="Name of requested material/source")
    category = models.CharField(max_length=50, help_text="Category (e.g., purchased-goods, stationary)")
    description = models.TextField(help_text="Description of the material and why it's needed")
    
    # User's information (if they have it)
    suggested_factor = models.FloatField(blank=True, null=True, 
                                        help_text="User's suggested emission factor (if known)")
    suggested_unit = models.CharField(max_length=20, blank=True, null=True,
                                     help_text="Suggested unit")
    suggested_source = models.TextField(blank=True, null=True,
                                       help_text="Source of suggested factor")
    
    # Admin response
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True, help_text="Admin notes/response")
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='reviewed_requests')
    reviewed_at = models.DateTimeField(blank=True, null=True)
    
    # If approved, link to the added factor
    added_to_system = models.BooleanField(default=False)
    system_source_key = models.CharField(max_length=100, blank=True, null=True,
                                        help_text="Key in emission_factors.py if added to system")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Material Request"
        verbose_name_plural = "Material Requests"
    
    def __str__(self):
        return f"{self.material_name} - {self.get_status_display()}"
    
    def approve(self, admin_user, notes=''):
        """Approve this request"""
        self.status = 'approved'
        self.reviewed_by = admin_user
        self.reviewed_at = timezone.now()
        self.admin_notes = notes
        self.save()
    
    def reject(self, admin_user, notes=''):
        """Reject this request"""
        self.status = 'rejected'
        self.reviewed_by = admin_user
        self.reviewed_at = timezone.now()
        self.admin_notes = notes
        self.save()


class ReportExtraInfo(models.Model):
    """Store additional organizational details for more complete ISO 14064-1 reports"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='report_extra_info')
    
    # Organization details
    legal_name = models.CharField(max_length=200, blank=True, null=True, 
                                 help_text="Legal name of organization")
    industry = models.CharField(max_length=100, blank=True, null=True,
                               help_text="Industry type or NAICS code")
    
    # Reporting boundary
    reporting_period = models.CharField(max_length=100, blank=True, null=True,
                                       help_text="Reporting period (e.g., 2025-01-01 to 2025-12-31)")
    boundary_approach = models.CharField(max_length=50, blank=True, null=True,
                                        choices=[
                                            ('operational_control', 'Operational Control'),
                                            ('financial_control', 'Financial Control'),
                                            ('equity_share', 'Equity Share'),
                                        ],
                                        help_text="Consolidation approach")
    
    # Additional context
    notes = models.TextField(blank=True, null=True, 
                            help_text="Additional context for the report")
    
    # Consent tracking
    share_org_profile = models.BooleanField(default=True, 
                                           help_text="User consented to share organization profile")
    share_boundary = models.BooleanField(default=True,
                                        help_text="User consented to share reporting boundary")
    share_data_sources = models.BooleanField(default=False,
                                            help_text="User consented to share data sources info")
    share_projects = models.BooleanField(default=False,
                                        help_text="User consented to share projects/initiatives")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Report Extra Information"
        verbose_name_plural = "Report Extra Information"
    
    def __str__(self):
        return f"{self.user.username} - Report Extra Info"


class IndustryType(models.Model):
    """Industry types for better emission factor categorization"""
    name = models.CharField(max_length=200, unique=True, help_text="Industry name")
    code = models.CharField(max_length=20, blank=True, null=True, help_text="Industry code (e.g., NAICS)")
    description = models.TextField(blank=True, null=True, help_text="Industry description")
    is_active = models.BooleanField(default=True, help_text="Is this industry type active?")
    
    # User who requested this industry (if it was user-requested)
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   help_text="User who requested this industry type")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Industry Type"
        verbose_name_plural = "Industry Types"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name


class IndustryRequest(models.Model):
    """User requests for new industry types"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    industry_name = models.CharField(max_length=200, help_text="Requested industry name")
    industry_code = models.CharField(max_length=20, blank=True, null=True, help_text="Industry code if known")
    description = models.TextField(help_text="Description of the industry")
    business_context = models.TextField(blank=True, null=True, help_text="How this industry relates to their business")
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True, help_text="Admin notes about this request")
    
    # If approved, link to the created industry
    approved_industry = models.ForeignKey(IndustryType, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Industry Request"
        verbose_name_plural = "Industry Requests"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.industry_name} - {self.get_status_display()}"
