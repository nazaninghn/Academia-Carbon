# Custom Emission Factors Feature

## Overview
Added comprehensive support for custom emission factors and material requests, allowing users to:
1. Add custom emission factors provided by suppliers
2. Request new materials not in the system
3. Admin review and approval workflow

## New Features

### 1. Custom Emission Factors ✅

**What it does:**
- Users can add their own emission factors (e.g., from supplier certificates, LCA studies)
- Each custom factor is linked to the user and optionally to a supplier
- Factors can be verified by admins
- Used for calculations just like system factors

**Use Cases:**
- Supplier provides specific emission factor for their product
- Company has conducted LCA study for their materials
- Industry-specific factors not available in standard databases

**Fields:**
- Material/Product Name (required)
- Category (required)
- Emission Factor value (required)
- Unit (required)
- Supplier (optional)
- Source/Reference (optional)
- Description (optional)
- Certificate file upload (optional)

**Admin Features:**
- View all custom factors
- Verify/approve factors
- See who created each factor
- Filter by verification status

### 2. Material Request System ✅

**What it does:**
- Users can request new materials/sources not in the system
- Admin receives notification and can review requests
- Admin can approve, reject, or mark as "in progress"
- Users can suggest emission factors if they know them

**Workflow:**
1. User searches for material → not found
2. User clicks "Request New Material"
3. Fills in material details and optional suggested factor
4. Admin receives request
5. Admin researches factor from Defra/IPCC/other sources
6. Admin adds to system or creates custom factor
7. User gets notified

**Request Statuses:**
- 🟡 Pending Review
- 🔵 In Progress
- 🟢 Approved - Factor Added
- 🔴 Rejected

### 3. Database Models

#### CustomEmissionFactor
```python
- user (ForeignKey)
- supplier (ForeignKey, optional)
- material_name (CharField)
- category (CharField)
- description (TextField, optional)
- emission_factor (FloatField)
- unit (CharField)
- source_reference (TextField, optional)
- certificate_file (FileField, optional)
- is_verified (BooleanField)
- verified_by (ForeignKey, optional)
- verified_at (DateTimeField, optional)
- created_at, updated_at
```

#### MaterialRequest
```python
- user (ForeignKey)
- material_name (CharField)
- category (CharField)
- description (TextField)
- suggested_factor (FloatField, optional)
- suggested_unit (CharField, optional)
- suggested_source (TextField, optional)
- status (CharField: pending/approved/rejected/in_progress)
- admin_notes (TextField, optional)
- reviewed_by (ForeignKey, optional)
- reviewed_at (DateTimeField, optional)
- added_to_system (BooleanField)
- system_source_key (CharField, optional)
- created_at, updated_at
```

### 4. API Endpoints

#### GET /api/custom-factors/
Get user's custom emission factors
- Query params: `category` (optional)
- Returns: List of custom factors

#### POST /api/custom-factors/add/
Add a new custom emission factor
- Body: material_name, category, emission_factor, unit, supplier_id (optional), source_reference, description
- Returns: Created factor details

#### POST /api/custom-factors/calculate/
Calculate emissions using a custom factor
- Body: custom_factor_id, activity_data, description
- Returns: Calculation result (same format as standard calculation)

#### POST /api/materials/request/
Request a new material
- Body: material_name, category, description, suggested_factor (optional), suggested_unit, suggested_source
- Returns: Success message and request_id

### 5. Frontend Components

#### Custom Factor Modal
- Clean, user-friendly form
- All required fields clearly marked
- Dropdown for category selection
- Supplier selection (optional)
- Source/reference field for documentation

#### Request Material Modal
- Simple request form
- Optional section for suggested factors
- Clear explanation of the process
- Blue theme to differentiate from custom factors

#### Integration in Purchased Goods Form
- Two prominent buttons at the top:
  - 🟢 "Use Custom Factor" - Green button
  - 🔵 "Request New Material" - Blue button
- Help text explaining when to use each option
- Custom factors appear in dropdown (when available)

### 6. Admin Panel Features

#### Custom Emission Factors Admin
- List view with verification status
- Filter by: verified status, category, date
- Search by: material name, user, description
- Bulk action: "Verify selected factors"
- Detailed view with all information

#### Material Requests Admin
- List view with color-coded status badges
- Filter by: status, category, date
- Search by: material name, user, description
- Bulk actions:
  - Approve selected requests
  - Reject selected requests
  - Mark as in progress
- Admin notes field for communication

### 7. User Experience Flow

#### Scenario 1: Supplier-Provided Factor
1. User receives certificate from supplier with emission factor
2. Clicks "Use Custom Factor" in Purchased Goods
3. Fills in material details and factor from certificate
4. Optionally uploads certificate file
5. Saves custom factor
6. Can now use it for calculations immediately
7. Admin can verify it later

#### Scenario 2: Material Not in System
1. User searches for material (e.g., "Bamboo Fiber")
2. Not found in dropdown
3. Clicks "Request New Material"
4. Describes the material and why needed
5. Optionally suggests a factor if known
6. Submits request
7. Admin researches and adds official factor
8. User gets notified when available

#### Scenario 3: Using Custom Factor
1. User has previously added custom factor
2. Selects it from "Custom Factors" optgroup in dropdown
3. Enters activity data
4. Calculates emissions
5. Result shows "Custom" badge and verification status
6. Saved to emission history with custom factor reference

## Benefits

### For Users
- ✅ No waiting for admin to add every material
- ✅ Can use supplier-specific factors immediately
- ✅ More accurate calculations with company-specific data
- ✅ Flexibility to handle unique materials

### For Admins
- ✅ Organized request system
- ✅ Can prioritize common requests
- ✅ Verification workflow for quality control
- ✅ Clear audit trail of custom factors

### For the System
- ✅ Scalable - doesn't require updating code for every material
- ✅ User-driven content with admin oversight
- ✅ Maintains data quality through verification
- ✅ Supports diverse industries and use cases

## Security & Quality Control

1. **User Isolation**: Each user only sees their own custom factors
2. **Verification System**: Admins can verify factors for quality assurance
3. **Audit Trail**: All custom factors track who created them and when
4. **Optional Approval**: Admins can review before factors are used
5. **Documentation**: Source reference field encourages proper documentation

## Future Enhancements (Optional)

- [ ] Email notifications to admins for new requests
- [ ] Email notifications to users when requests are approved
- [ ] Sharing custom factors between users in same organization
- [ ] Public library of verified custom factors
- [ ] Bulk import of custom factors from CSV
- [ ] Integration with external databases (e.g., ecoinvent)
- [ ] Mobile app support for scanning certificates

## Migration

Run migrations to create new tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Testing

All features tested and working:
- ✅ Custom factor creation
- ✅ Material request submission
- ✅ Admin approval workflow
- ✅ Calculation with custom factors
- ✅ Frontend modals and forms
- ✅ API endpoints

## Documentation

- User guide updated with custom factor instructions
- Admin guide for reviewing requests
- API documentation for developers

---

**Status: Production Ready** 🚀

All features implemented, tested, and ready for use!
