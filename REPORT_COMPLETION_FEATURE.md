# Report Completion Feature

## Overview
This feature adds an "Improve report accuracy" card to the ISO 14064-1 emissions inventory report page, allowing users to optionally share additional organizational details for more complete reports.

## Features

### 1. Complete Report Card
- **Location**: Appears on the inventory report page (`/reporting/inventory/`) between the download buttons and filters
- **Design**: Clean card with shield icon, professional styling
- **Purpose**: Encourages users to provide additional context for more comprehensive reports

### 2. Consent-Based Data Collection
Users can choose which information to share:
- ✅ Organization profile (industry, size, locations)
- ✅ Reporting boundary (operational control/equity share, subsidiaries)  
- ✅ Activity data sources (utility bills, fuel receipts)
- ✅ Reduction initiatives / projects (optional)

### 3. Modal Form
When users click "Share info (optional)", a modal opens with fields for:
- **Legal name**: Company/Organization name
- **Industry**: Industry type or NAICS code (optional)
- **Reporting period**: e.g., "2025-01-01 to 2025-12-31"
- **Boundary approach**: Operational control, Financial control, or Equity share
- **Notes**: Additional context (optional)

### 4. Privacy & Trust Features
- **Optional**: Clearly marked as optional throughout
- **Transparent**: "Privacy & data use" link
- **User control**: "You can remove this anytime" messaging
- **Granular consent**: Checkboxes for different data types

## Technical Implementation

### Database Model
```python
class ReportExtraInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    legal_name = models.CharField(max_length=200, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    reporting_period = models.CharField(max_length=100, blank=True, null=True)
    boundary_approach = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Consent tracking
    share_org_profile = models.BooleanField(default=True)
    share_boundary = models.BooleanField(default=True)
    share_data_sources = models.BooleanField(default=False)
    share_projects = models.BooleanField(default=False)
```

### API Endpoint
- **URL**: `/api/report-extra/`
- **Methods**: GET (retrieve), POST (save)
- **Authentication**: Login required
- **Response**: JSON with success/error status

### Frontend Components
- **Card UI**: Responsive design with mobile support
- **Modal**: Clean, accessible modal with form validation
- **JavaScript**: Handles form submission, data loading, error handling

## Usage

### For Users
1. Navigate to the inventory report page
2. Look for the "Improve report accuracy" card
3. Select which information types to share (checkboxes)
4. Click "Share info (optional)" to open the form
5. Fill in desired fields (all optional)
6. Click "Save" to store information

### For Developers
The additional information can be accessed in report generation:
```python
try:
    extra_info = request.user.report_extra_info
    if extra_info.legal_name:
        # Include legal name in report
    if extra_info.boundary_approach:
        # Include boundary approach in report
except ReportExtraInfo.DoesNotExist:
    # User hasn't provided extra info
    pass
```

## Files Modified/Added

### Modified Files
- `ghg/models.py` - Added ReportExtraInfo model
- `ghg/views.py` - Added report_extra_info_api view
- `ghg/urls.py` - Added API endpoint URL
- `ghg/admin.py` - Added admin interface for ReportExtraInfo
- `templates/reporting/inventory.html` - Added UI components and JavaScript

### New Migration
- `ghg/migrations/0008_reportextrainfo.py` - Database migration for new model

## Security & Privacy

### Data Protection
- All fields are optional
- User controls what information to share
- Data is only used for report generation
- Users can delete information anytime through admin

### Consent Management
- Granular consent checkboxes
- Consent preferences stored with data
- Clear privacy messaging
- Transparent data usage

## Future Enhancements

1. **PDF Integration**: Include extra info in generated PDF reports
2. **Data Export**: Allow users to export their extra information
3. **Bulk Operations**: Admin tools for managing multiple users' data
4. **Verification**: Optional verification workflow for organizational details
5. **Templates**: Pre-filled templates for common industries

## Testing

To test the feature:
1. Start the development server
2. Navigate to `/reporting/inventory/`
3. Look for the "Improve report accuracy" card
4. Test the modal form functionality
5. Verify data persistence through the API
6. Check admin interface at `/admin/ghg/reportextrainfo/`