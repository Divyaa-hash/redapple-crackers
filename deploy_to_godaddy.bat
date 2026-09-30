@echo off
REM GoDaddy SSH Deployment Script for Windows
REM This script deploys the crackers website to GoDaddy via SSH

set SSH_HOST=redapplecrackers.com
set SSH_USER=gs26214tgb0g
set REMOTE_PATH=/home/gs26214tgb0g/redapple-crackers
set LOCAL_PATH=C:\Users\Divya\OneDrive\Desktop\crackers

echo ==========================================
echo GoDaddy SSH Deployment Script
echo ==========================================
echo Host: %SSH_HOST%
echo User: %SSH_USER%
echo Remote Path: %REMOTE_PATH%
echo ==========================================
echo.

REM Step 1: Backup existing database on remote server
echo Step 1: Backing up existing database on GoDaddy...
ssh %SSH_USER%@%SSH_HOST% "cd %REMOTE_PATH% && cp db.sqlite3 db.sqlite3.backup.%%date:~10,4%%%%date:~4,2%%%%date:~7,2%%_%%time:~0,2%%%%time:~3,2%"
if %errorlevel% neq 0 (
    echo X Database backup failed
    pause
    exit /b 1
)
echo Database backup completed
echo.

REM Step 2: Upload database
echo Step 2: Uploading database file...
scp "%LOCAL_PATH%\db.sqlite3" %SSH_USER%@%SSH_HOST%:%REMOTE_PATH%/
if %errorlevel% neq 0 (
    echo X Database upload failed
    pause
    exit /b 1
)
echo Database uploaded successfully
echo.

REM Step 3: Upload logo files
echo Step 3: Uploading logo files...
scp "%LOCAL_PATH%\logo.jpg" %SSH_USER%@%SSH_HOST%:%REMOTE_PATH%/
scp "%LOCAL_PATH%\static\images\crackers\logo.jpg" %SSH_USER%@%SSH_HOST%:%REMOTE_PATH%/static/images/crackers/
scp "%LOCAL_PATH%\staticfiles\images\crackers\logo.jpg" %SSH_USER%@%SSH_HOST%:%REMOTE_PATH%/staticfiles/images/crackers/
if %errorlevel% neq 0 (
    echo X Logo files upload failed
    pause
    exit /b 1
)
echo Logo files uploaded successfully
echo.

REM Step 4: Upload static files (using scp for key files)
echo Step 4: Uploading static files...
scp -r "%LOCAL_PATH%\static\css" %SSH_USER%@%SSH_HOST%:%REMOTE_PATH%/static/
scp -r "%LOCAL_PATH%\static\js" %SSH_USER%@%SSH_HOST%:%REMOTE_PATH%/static/
scp -r "%LOCAL_PATH%\static\images" %SSH_USER%@%SSH_HOST%:%REMOTE_PATH%/static/
if %errorlevel% neq 0 (
    echo X Static files upload failed
    pause
    exit /b 1
)
echo Static files uploaded successfully
echo.

REM Step 5: Upload staticfiles (collected static)
echo Step 5: Uploading collected static files...
scp -r "%LOCAL_PATH%\staticfiles\css" %SSH_USER%@%SSH_HOST%:%REMOTE_PATH%/staticfiles/
scp -r "%LOCAL_PATH%\staticfiles\js" %SSH_USER%@%SSH_HOST%:%REMOTE_PATH%/staticfiles/
scp -r "%LOCAL_PATH%\staticfiles\images" %SSH_USER%@%SSH_HOST%:%REMOTE_PATH%/staticfiles/
if %errorlevel% neq 0 (
    echo X Collected static files upload failed
    pause
    exit /b 1
)
echo Collected static files uploaded successfully
echo.

REM Step 6: Restart Passenger application
echo Step 6: Restarting Passenger application...
ssh %SSH_USER%@%SSH_HOST% "cd %REMOTE_PATH% && touch passenger_wsgi.py"
if %errorlevel% neq 0 (
    echo X Passenger restart failed
    pause
    exit /b 1
)
echo Passenger restart triggered
echo.

echo ==========================================
echo Deployment completed successfully!
echo ==========================================
echo.
echo Next steps:
echo 1. Visit http://redapplecrackers.com/ to verify
echo 2. Check that the logo is updated
echo 3. Check that product images are displaying correctly
echo.

pause
