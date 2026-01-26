# Git Commands to Push Changes

## Step 1: Check Status
```bash
cd Academia-Carbon
git status
```

## Step 2: Add All Changes
```bash
git add .
```

## Step 3: Commit Changes
```bash
git commit -m "feat: Add Request New Material floating button feature

- Added floating action button (FAB) in bottom-right corner
- Created simple modal for material requests
- Connected to MaterialRequest backend API
- Removed old non-functional button implementations
- Added comprehensive documentation

Features:
- Always visible floating button
- Simple form with required/optional fields
- Backend validation and security
- Admin panel integration
- English UI/UX"
```

## Step 4: Push to GitHub
```bash
git push origin main
```

Or if your branch is different:
```bash
git push origin master
```

## If You Need to Set Remote (First Time)
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## Files Changed Summary
**Added:**
- Floating action button in data_entry.html
- Simple modal with English UI
- JavaScript functions for modal control
- REQUEST_MATERIAL_FEATURE.md documentation

**Modified:**
- templates/data_entry.html (added FAB and modal)
- ghg/views.py (cleaned up test code)
- ghg/urls.py (removed test URL)

**Removed:**
- test_button.html
- DEBUG_INSTRUCTIONS.md
- TESTING_CHECKLIST.md
- TEMPLATE_FIX_SUMMARY.md
- FINAL_TEST_GUIDE.md
- BUTTON_VISIBILITY_FIX.md

## Verify Before Push
```bash
# Make sure migrations are applied
python manage.py migrate

# Run tests if you have any
python manage.py test

# Check for any issues
python manage.py check --deploy
```

## After Push
1. Go to your GitHub repository
2. Verify the changes are there
3. Check the commit message
4. Update README.md if needed
