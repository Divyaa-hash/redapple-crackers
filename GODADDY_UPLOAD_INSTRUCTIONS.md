# GoDaddy Upload Instructions - Image Fix

## Files to Upload to GoDaddy

### 1. Database File (CRITICAL)
- **Source:** `C:\Users\Divya\OneDrive\Desktop\crackers\db.sqlite3`
- **Destination:** `/home/gs26214tgb0g/redapple-crackers/db.sqlite3`
- **Action:** Replace the existing file with the updated database

### 2. New Template Tag Directory
- **Create directory:** `/home/gs26214tgb0g/redapple-crackers/products/templatetags/`
- **Upload files:**
  - `__init__.py`
  - `product_images.py`

### 3. Updated Template Files
Replace these files in `/home/gs26214tgb0g/redapple-crackers/templates/`:
- `home.html`
- `shop.html`
- `product_detail.html`
- `cart.html`
- `checkout.html`
- `wishlist.html`
- `home_new.html`

## Upload Steps using cPanel File Manager

### Step 1: Access cPanel
1. Log in to your GoDaddy cPanel
2. Go to **File Manager**

### Step 2: Upload Database
1. Navigate to: `/home/gs26214tgb0g/redapple-crackers/`
2. **BACKUP** the existing `db.sqlite3` file (rename it to `db.sqlite3.backup`)
3. Upload the new `db.sqlite3` from your local computer
4. Set permissions to 644

### Step 3: Create Template Tag Directory
1. Navigate to: `/home/gs26214tgb0g/redapple-crackers/products/`
2. Click **"Folder"** to create a new folder named `templatetags`
3. Navigate into the new `templatetags` folder
4. Upload `__init__.py` and `product_images.py`

### Step 4: Update Template Files
1. Navigate to: `/home/gs26214tgb0g/redapple-crackers/templates/`
2. Replace each of the 7 template files with the updated versions from your local computer

### Step 5: Restart Passenger (if needed)
1. In cPanel, go to **Software > Setup Python App**
2. Find your redapple-crackers application
3. Click **"Restart"**

## Verification
After uploading, visit: http://redapplecrackers.com/shop/
The images should now match what you see on localhost.
