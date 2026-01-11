# PRODUCTION DEPLOYMENT CHECKLIST

## Pre-Deployment Steps

1. **Environment Variables in Render Dashboard**:
   ```
   DEBUG=False
   SECRET_KEY=<generate-new-secret-key>
   ```

2. **Generate SECRET_KEY**:
   ```python
   import secrets
   print(secrets.token_urlsafe(50))
   ```

3. **Files Updated**:
   - requirements.txt (production packages)
   - build.sh (build script)
   - render.yaml (configuration)
   - URLs fixed (removed fix_users_temp)

## Deployment Steps

1. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Fix production deployment issues"
   git push origin main
   ```

2. **Set Environment Variables in Render**:
   - Go to Render Dashboard
   - Select Academia Carbon service
   - Go to Environment tab
   - Add: DEBUG=False
   - Add: SECRET_KEY=<your-generated-key>

3. **Trigger Deployment**:
   - Manual deploy or automatic on push

4. **Verify Deployment**:
   ```bash
   python debug_production.py
   ```

## Expected Results

- Site returns 200 OK (not 500 error)
- All pages load correctly
- Authentication works
- Database operations work

## If Still Getting 500 Error

1. Check Render logs for detailed error messages
2. Verify all environment variables are set
3. Check that build completed successfully
4. Ensure migrations ran without errors

---

**After successful deployment, run security verification:**
```bash
python verify_security_complete.py
```