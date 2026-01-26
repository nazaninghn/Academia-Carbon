# Request New Material Feature

## Overview
A floating action button (FAB) that allows users to request new materials/emission factors that are not currently in the system.

## Features
- ✅ Floating button in bottom-right corner (always visible)
- ✅ Simple modal with required fields
- ✅ Connected to backend API
- ✅ Stores requests in MaterialRequest model
- ✅ Admin can review and approve requests

## User Interface

### Floating Action Button
- **Location**: Bottom-right corner of the page
- **Style**: Blue circular button with paper plane icon
- **Behavior**: Hover animation (scales up)
- **Always visible**: Fixed position, stays on screen while scrolling

### Modal Form
**Required Fields:**
- Material Name (نام ماده)
- Category (دسته‌بندی)
- Description (توضیحات)

**Optional Fields:**
- Suggested Emission Factor (ضریب انتشار پیشنهادی)
- Unit (واحد)
- Source (منبع)

## Backend

### API Endpoint
- **URL**: `/api/materials/request/`
- **Method**: POST
- **View**: `request_new_material` in `ghg/views.py`
- **Authentication**: Required (login_required)
- **Rate Limit**: Standard rate limiting applied

### Database Model
**Model**: `MaterialRequest` in `ghg/models.py`

**Fields:**
- `user`: ForeignKey to User
- `request_type`: CharField (default: 'material')
- `name`: CharField (max 200)
- `description`: TextField
- `additional_info`: TextField (stores category, factor, unit, source)
- `status`: CharField (pending/approved/rejected)
- `admin_notes`: TextField (optional)
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

### Request Data Format
```json
{
    "material_name": "Bamboo Fiber",
    "category": "purchased-goods",
    "description": "Need emission factor for bamboo fiber",
    "suggested_factor": 1.5,
    "suggested_unit": "kg",
    "suggested_source": "Supplier certificate"
}
```

### Response Format
**Success:**
```json
{
    "success": true,
    "message": "Your request has been submitted. Admin will review it soon.",
    "request_id": 123
}
```

**Error:**
```json
{
    "error": "Missing required fields"
}
```

## Admin Panel
Admins can view and manage material requests in Django admin:
- Navigate to: `/admin/ghg/materialrequest/`
- Filter by status (pending/approved/rejected)
- Add admin notes
- Change status

## Files Modified
1. `templates/data_entry.html` - Added floating button and modal
2. `ghg/views.py` - `request_new_material` view
3. `ghg/models.py` - `MaterialRequest` model
4. `ghg/urls.py` - API endpoint routing

## How to Use

### For Users:
1. Navigate to Data Entry page
2. Click the blue floating button in bottom-right corner
3. Fill in the form (required fields marked with *)
4. Click "ارسال درخواست" (Submit Request)
5. Wait for admin approval

### For Admins:
1. Go to Django admin panel
2. Navigate to "Material Requests"
3. Review pending requests
4. Add emission factor to system if approved
5. Update request status and add notes

## Categories Available
- `stationary` - Stationary Combustion
- `mobile` - Mobile Combustion
- `purchased-goods` - Purchased Goods & Services
- `waste` - Waste
- `other` - Other

## Security Features
- ✅ CSRF protection
- ✅ Login required
- ✅ Input validation
- ✅ Field length limits
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Rate limiting

## Testing
```bash
# Run server
python manage.py runserver

# Navigate to
http://127.0.0.1:8000/data-entry/

# Look for blue floating button in bottom-right corner
# Click and test the form
```

## Future Enhancements
- Email notifications to admins on new requests
- User dashboard to track request status
- Bulk import of approved materials
- Integration with external emission factor databases
