# Mobile Logo Display Issue - Solution Guide

## Problem Description
In mobile view on the landing page, the logo appears as a **small green square** instead of the full logo image. In desktop view, the logo displays correctly.

## Root Cause
The current `logo.png` file has the following issues:
1. **White Background**: The PNG file has a white background instead of a transparent background
2. **Large File Size**: 128KB (too large for a logo, should be under 20KB)
3. **Mobile Display**: When scaled down to 70px in mobile view, only the green portion is visible

## Current File Information
- **File**: `Academia-Carbon/static/images/logo.png`
- **Size**: 128,394 bytes (128KB)
- **Format**: PNG
- **Issue**: White background, not transparent

## Solution Options

### Option 1: Replace with Transparent PNG (Recommended)
1. Open your logo in an image editor (Photoshop, GIMP, Photopea, etc.)
2. Remove the white background
3. Export as PNG with **transparent background**
4. Optimize the file size (should be under 20KB)
5. Replace the file at: `Academia-Carbon/static/images/logo.png`

### Option 2: Use SVG Format (Best Quality)
1. Convert your logo to SVG format
2. SVG files are:
   - Vector-based (perfect quality at any size)
   - Much smaller file size
   - Support transparent backgrounds natively
3. Save as: `Academia-Carbon/static/images/logo.svg`
4. Update the template to use `.svg` instead of `.png`

### Option 3: Use Online Tools
You can use free online tools to remove the background:
- **remove.bg** - https://www.remove.bg/
- **Photopea** - https://www.photopea.com/ (free Photoshop alternative)
- **GIMP** - https://www.gimp.org/ (free desktop software)

## Steps to Fix

### If Using PNG:
1. Remove white background from logo
2. Export as PNG with transparency
3. Optimize file size (use tools like TinyPNG.com)
4. Replace file: `Academia-Carbon/static/images/logo.png`
5. Test in mobile view

### If Using SVG:
1. Convert logo to SVG format
2. Save as: `Academia-Carbon/static/images/logo.svg`
3. Update line 1537 in `Academia-Carbon/templates/landing.html`:
   ```html
   <!-- Change from: -->
   <img src="{% static 'images/logo.png' %}" alt="Academia Carbon" class="logo-icon" loading="eager">
   
   <!-- To: -->
   <img src="{% static 'images/logo.svg' %}" alt="Academia Carbon" class="logo-icon" loading="eager">
   ```
4. Test in mobile view

## Current CSS Configuration
The mobile logo styles are correctly configured:
- Width: 70px (mobile)
- Height: 70px (mobile)
- Object-fit: contain
- Background: transparent
- Display: block

The CSS is working correctly. The issue is with the image file itself.

## Testing After Fix
1. Clear browser cache
2. Run: `python manage.py collectstatic --noinput`
3. Test on mobile device or mobile view in browser
4. Logo should display fully, not as a green square

## Additional Notes
- Desktop logo size: 100px × 100px
- Mobile logo size: 70px × 70px
- The logo loads slowly because of the 128KB file size
- After fixing, the logo should load instantly and display correctly on all devices
