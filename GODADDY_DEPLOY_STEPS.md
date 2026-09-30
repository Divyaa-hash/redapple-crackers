# GoDaddy Deployment Instructions - Logo & Product Images Update

## Files to Upload to GoDaddy (Updated)

### Critical Files to Upload:

1. **Database File** (MUST BACKUP FIRST)
   - Source: `C:\Users\Divya\OneDrive\Desktop\crackers\db.sqlite3`
   - Destination: `/home/gs26214tgb0g/redapple-crackers/db.sqlite3`
   - **ACTION**: Backup existing file first, then replace

2. **Logo Files**
   - Source: `C:\Users\Divya\OneDrive\Desktop\crackers\logo.jpg`
   - Destination: `/home/gs26214tgb0g/redapple-crackers/logo.jpg`

   - Source: `C:\Users\Divya\OneDrive\Desktop\crackers\static\images\crackers\logo.jpg`
   - Destination: `/home/gs26214tgb0g/redapple-crackers/static/images/crackers/logo.jpg`

   - Source: `C:\Users\Divya\OneDrive\Desktop\crackers\staticfiles\images\crackers\logo.jpg`
   - Destination: `/home/gs26214tgb0g/redapple-crackers/staticfiles/images/crackers/logo.jpg`

3. **Static Files** (Update entire directories)
   - Source: `C:\Users\Divya\OneDrive\Desktop\crackers\static\css\`
   - Destination: `/home/gs26214tgb0g/redapple-crackers/static/css/`

   - Source: `C:\Users\Divya\OneDrive\Desktop\crackers\static\js\`
   - Destination: `/home/gs26214tgb0g/redapple-crackers/static/js/`

   - Source: `C:\Users\Divya\OneDrive\Desktop\crackers\static\images\crackers\`
   - Destination: `/home/gs26214tgb0g/redapple-crackers/static/images/crackers/`

4. **Staticfiles** (Collected static)
   - Source: `C:\Users\Divya\OneDrive\Desktop\crackers\staticfiles\css\`
   - Destination: `/home/gs26214tgb0g/redapple-crackers/staticfiles/css/`

   - Source: `C:\Users\Divya\OneDrive\Desktop\crackers\staticfiles\js\`
   - Destination: `/home/gs26214tgb0g/redapple-crackers/staticfiles/js/`

   - Source: `C:\Users\Divya\OneDrive\Desktop\crackers\staticfiles\images\crackers\`
   - Destination: `/home/gs26214tgb0g/redapple-crackers/staticfiles/images/crackers/`

## Step-by-Step Instructions (cPanel File Manager)

### Step 1: Access cPanel
1. Log in to your GoDaddy account
2. Go to **My Products**
3. Click on your hosting plan
4. Click **cPanel Admin**

### Step 2: Open File Manager
1. In cPanel, find and click **File Manager**
2. Navigate to: `/home/gs26214tgb0g/redapple-crackers/`

### Step 3: Backup Database (CRITICAL)
1. Find `db.sqlite3` in the root directory
2. Right-click and select **Rename**
3. Rename it to `db.sqlite3.backup` with today's date
4. This ensures you can revert if something goes wrong

### Step 4: Upload Database
1. Click **Upload** in the File Manager toolbar
2. Select `db.sqlite3` from your local computer
3. Wait for upload to complete
4. Set file permissions to 644 (right-click > Change Permissions)

### Step 5: Upload Logo Files
1. Navigate to `/home/gs26214tgb0g/redapple-crackers/`
2. Upload `logo.jpg` from your local computer

3. Navigate to `/home/gs26214tgb0g/redapple-crackers/static/images/crackers/`
4. Upload `logo.jpg` (replace existing)

5. Navigate to `/home/gs26214tgb0g/redapple-crackers/staticfiles/images/crackers/`
6. Upload `logo.jpg` (replace existing)

### Step 6: Upload Static Files
1. Navigate to `/home/gs26214tgb0g/redapple-crackers/static/`
2. For each subdirectory (css, js, images):
   - Enter the directory
   - Upload all files from the corresponding local directory
   - Overwrite existing files when prompted

### Step 7: Upload Staticfiles
1. Navigate to `/home/gs26214tgb0g/redapple-crackers/staticfiles/`
2. For each subdirectory (css, js, images):
   - Enter the directory
   - Upload all files from the corresponding local directory
   - Overwrite existing files when prompted

### Step 8: Restart Passenger Application
1. In cPanel, go to **Software > Setup Python App**
2. Find your `redapple-crackers` application
3. Click **Restart**
4. Wait for the restart to complete

### Step 9: Verify Deployment
1. Open your browser
2. Visit: `http://redapplecrackers.com/`
3. Check that:
   - The new logo is displayed (THE CELEBRATION COLLECTION with red apple)
   - Product images are showing the logo for the 19 updated products
   - The site loads without errors

## Alternative: Use SFTP Client (FileZilla)

If you prefer using an FTP client instead of cPanel File Manager:

1. **Download FileZilla**: https://filezilla-project.org/
2. **Configure connection**:
   - Host: `redapplecrackers.com`
   - Username: `gs26214tgb0g`
   - Password: Your GoDaddy password
   - Port: 22 (SFTP)

3. **Connect and upload files** following the same file paths above

## Troubleshooting

### If images don't appear:
1. Clear your browser cache (Ctrl+F5)
2. Check file permissions (should be 644 for files, 755 for directories)
3. Restart Passenger again in cPanel
4. Check browser console for 404 errors

### If site doesn't load:
1. Restore the database backup
2. Check Python error logs in cPanel
3. Verify Django settings in config/settings.py

### If SSH connection fails:
- Use cPanel File Manager (recommended for GoDaddy)
- Or use FileZilla SFTP client
- SSH may require additional setup on GoDaddy

## Summary of Changes Made

- ✅ Updated logo to "THE CELEBRATION COLLECTION" with red apple
- ✅ Updated 19 products to use logo image:
  - Colour Rocket
  - 10k Wala Spl, 5k Wala Spl, 2k Wala Spl, 1k Wala Spl
  - 10k Wala, 5k Wala, 2k Wala, 1k Wala, 1H Wala
  - Avatar 2
  - Jolly Bobby Asok Brand
  - Smiley Mushroom
  - Sword
  - Kickerzzz (2 variants)
  - Little Dove
  - Mini Peacock
  - Binge Pop

## Contact Support

If you encounter issues:
1. Check GoDaddy documentation: https://www.godaddy.com/help/cpanel-26378
2. Contact GoDaddy support via chat or phone
3. Consider switching to Render (already configured and working)
