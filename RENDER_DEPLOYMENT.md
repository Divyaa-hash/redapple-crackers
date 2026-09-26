# Render Deployment Guide for RedApple Crackers

## Current Status
- ✅ Code is pushed to GitHub: https://github.com/Divyaa-hash/redapple-crackers.git
- ✅ Latest commit: dbca6c8 (Enhance admin dashboard with improved order display and WhatsApp features)
- ✅ All migrations applied locally
- ✅ Database cleaned (no test data)
- ✅ Server ready for production

## Deploy to Render

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up or log in
3. Connect your GitHub account

### Step 2: Create PostgreSQL Database
1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Name: `redapple-crackers-db`
4. Database: `crackers`
5. User: `postgres`
6. Region: Choose nearest region
7. Click "Create Database"
8. Wait for database to be ready
9. Copy the database connection URL

### Step 3: Set Environment Variables
After database is created, add these environment variables in Render:

1. **SECRET_KEY**: Generate a strong secret key
   ```
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **DEBUG**: `False`

3. **ALLOWED_HOSTS**: `.onrender.com,your-app-name.onrender.com`

4. **DATABASE_URL**: (From Render PostgreSQL database - Render will auto-set this)

5. **RAZORPAY_KEY_ID**: Your Razorpay key ID

6. **RAZORPAY_KEY_SECRET**: Your Razorpay key secret

7. **WHATSAPP_ADMIN_NUMBER**: `9345980679`

### Step 4: Create Web Service
1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Connect GitHub repository: `Divyaa-hash/redapple-crackers`
4. Branch: `main`
5. Name: `redapple-crackers`
6. Region: Same as database
7. Build Command:
   ```
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```

8. Start Command:
   ```
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
   ```

9. Click "Create Web Service"

### Step 5: Configure Web Service
After deployment starts:

1. Go to your web service settings
2. Add environment variables from Step 3
3. Connect to the PostgreSQL database created in Step 2
4. Wait for deployment to complete

### Step 6: Verify Deployment
1. Once deployed, click the URL provided by Render
2. Test the website:
   - Home page: https://your-app-name.onrender.com/
   - Shop: https://your-app-name.onrender.com/shop/
   - Admin: https://your-app-name.onrender.com/admin/
   - Dashboard: https://your-app-name.onrender.com/siteadmin/dashboard/

### Step 7: Create Superuser
SSH into your Render web service or use Render's shell:

```bash
python manage.py createsuperuser
```

Use the same credentials:
- Username: saran_admin
- Email: saran450j@gmail.com
- Password: Admin@123

## Production Checklist

- [x] Code pushed to GitHub
- [x] Latest migrations committed
- [x] Database migrations included
- [x] Static files configured with WhiteNoise
- [x] Procfile configured for gunicorn
- [x] Requirements.txt up to date
- [x] ALLOWED_HOSTS configured for Render
- [x] DEBUG=False in production
- [x] PostgreSQL configured
- [x] Environment variables documented
- [ ] Create Render PostgreSQL database
- [ ] Create Render web service
- [ ] Set environment variables in Render
- [ ] Create superuser in production
- [ ] Test all functionality
- [ ] Configure custom domain (optional)

## Important Notes

1. **Database**: Render uses PostgreSQL, which is already configured in requirements.txt
2. **Static Files**: WhiteNoise is configured to serve static files
3. **Media Files**: Consider using Cloudinary for media file storage in production
4. **WhatsApp**: Current implementation generates messages but requires API integration
5. **Payments**: Razorpay integration requires production keys

## Troubleshooting

### Deployment Fails
- Check build logs in Render
- Verify requirements.txt has all dependencies
- Check Python version compatibility

### Database Connection Error
- Verify DATABASE_URL is set correctly
- Check database is in same region as web service
- Verify database credentials

### Static Files Not Loading
- Check `python manage.py collectstatic` ran successfully
- Verify WhiteNoise is in INSTALLED_APPS
- Check STATIC_URL and STATIC_ROOT settings

### Admin Panel Not Accessible
- Create superuser in production database
- Verify ALLOWED_HOSTS includes your Render domain
- Check DEBUG is False for security

## Links

- Render Dashboard: https://dashboard.render.com
- GitHub Repository: https://github.com/Divyaa-hash/redapple-crackers.git
- Django Docs: https://docs.djangoproject.com/
- Render Django Guide: https://render.com/docs/deploy-django
