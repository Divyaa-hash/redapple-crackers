# GoDaddy Shared Hosting (cPanel) Deployment Guide

## ⚠️ IMPORTANT NOTES

GoDaddy Shared Hosting has significant limitations for Django:
- No shell access (limited SSH if available)
- Limited Python versions (usually Python 3.6-3.9)
- No process management (no Gunicorn/uWSGI)
- Requires Passenger WSGI for Django
- Limited memory and CPU
- PostgreSQL may not be available (use SQLite)
- **NOT RECOMMENDED FOR PRODUCTION DJANGO APPS**

## BETTER ALTERNATIVES

1. **Render** (Free tier available) - Already configured, working
2. **DigitalOcean** ($4/month VPS) - Easy Django deployment
3. **Heroku** (Free tier) - Excellent Django support
4. **PythonAnywhere** (Free tier) - Designed for Django

---

## IF YOU STILL WANT TO PROCEED WITH GODADDY

### Step 1: Check Python Support in cPanel

1. Log in to your GoDaddy cPanel
2. Look for **"Setup Python App"** or **"Select Python Version"**
3. If you don't see this, your hosting doesn't support Python
4. Contact GoDaddy support to enable Python

### Step 2: Create a Python App in cPanel

1. In cPanel, click **"Setup Python App"**
2. Click **"Create Application"**
3. Configure:
   - **Python version:** 3.9 or higher (if available)
   - **Application root:** `/home/username/public_html/crackers`
   - **Application URL:** Leave blank or specify `/crackers`
   - **Application startup file:** `passenger_wsgi.py`
   - **Application entry point:** `passenger_wsgi.py`
4. Click **"Create"**

### Step 3: Upload Files

1. Compress your project (exclude `__pycache__`, `.git`, `venv`)
2. In cPanel File Manager:
   - Go to `/home/username/public_html/`
   - Upload the compressed file
   - Extract it to `crackers/` folder

### Step 4: Create passenger_wsgi.py

Create `passenger_wsgi.py` in the project root:

```python
import sys
import os

# Add project to Python path
sys.path.insert(0, '/home/username/public_html/crackers')
sys.path.insert(0, '/home/username/public_html/crackers/config')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django and application
import django
django.setup()

from config.wsgi import application
```

### Step 5: Install Dependencies

1. In cPanel Python App setup:
   - Click **"Run pip install"**
   - Add your requirements:
     ```
     Django==6.0.7
     djangorestframework==3.15.2
     python-decouple==3.8
     dj-database-url==2.2.0
     pillow==10.4.0
     ```
   - Click **"Install"**

### Step 6: Configure Django Settings

Update `config/settings.py` for GoDaddy:

```python
# Add your GoDaddy domain to ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'yourdomain.ipage.com'
]

# Use SQLite for shared hosting (no PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = '/home/username/public_html/crackers/staticfiles'
```

### Step 7: Run Migrations

1. In cPanel Terminal (if available) or SSH:
   ```bash
   cd /home/username/public_html/crackers
   python manage.py migrate
   ```

### Step 8: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 9: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 10: Restart Application

1. In cPanel Python App setup
2. Click **"Restart"**

---

## LIMITATIONS YOU WILL FACE

1. **Performance:** Shared hosting is slow for Django
2. **Python Version:** May be stuck on older Python
3. **Database:** No PostgreSQL, only SQLite
4. **Process Management:** No Gunicorn, limited performance
5. **Scalability:** Cannot handle high traffic
6. **Debugging:** Limited error logging and debugging tools

---

## RECOMMENDED SWITCH TO RENDER

You already have a working Render deployment:
- **Free tier available**
- **PostgreSQL database included**
- **Automatic HTTPS**
- **Automatic scaling**
- **Better performance**
- **Easier deployment**

Your current Render deployment:
- https://redapple-crackers.onrender.com/
- Already configured and working
- Just need to trigger deployment after changes

---

## IF YOU WANT TO CANCEL GODADDY

1. Contact GoDaddy support
2. Request cancellation within refund period
3. Continue using Render (free tier)
4. Or switch to DigitalOcean ($4/month)

---

## CONTACT

If you need help with Render deployment:
- Check RENDER_DEPLOYMENT.md in your project
- Your current deployment is already working
- Just trigger manual deploy after code changes
