"""
GoDaddy FTP/SFTP Deployment Script
This script deploys the crackers website to GoDaddy using FTP/SFTP
"""

import os
import sys
from pathlib import Path
from ftplib import FTP

# Configuration
FTP_HOST = "redapplecrackers.com"
FTP_USER = "gs26214tgb0g"
FTP_PASSWORD = input("Enter your GoDaddy FTP/SSH password: ")
REMOTE_PATH = "/home/gs26214tgb0g/redapple-crackers"
LOCAL_PATH = r"C:\Users\Divya\OneDrive\Desktop\crackers"

def upload_file(ftp, local_file, remote_file):
    """Upload a single file via FTP"""
    print(f"Uploading: {local_file} -> {remote_file}")
    try:
        with open(local_file, 'rb') as f:
            ftp.storbinary(f'STOR {remote_file}', f)
        print(f"Success: {local_file}")
        return True
    except Exception as e:
        print(f"Error uploading {local_file}: {e}")
        return False

def upload_directory(ftp, local_dir, remote_dir):
    """Upload a directory recursively via FTP"""
    print(f"Uploading directory: {local_dir} -> {remote_dir}")
    try:
        # Create remote directory if it doesn't exist
        try:
            ftp.mkd(remote_dir)
        except:
            pass  # Directory might already exist

        # Upload files in directory
        for item in os.listdir(local_dir):
            local_path = os.path.join(local_dir, item)
            remote_path = f"{remote_dir}/{item}"

            if os.path.isfile(local_path):
                upload_file(ftp, local_path, remote_path)
            elif os.path.isdir(local_path):
                upload_directory(ftp, local_path, remote_path)

        return True
    except Exception as e:
        print(f"Error uploading directory {local_dir}: {e}")
        return False

def main():
    print("=" * 50)
    print("GoDaddy FTP/SFTP Deployment Script")
    print("=" * 50)
    print(f"Host: {FTP_HOST}")
    print(f"User: {FTP_USER}")
    print(f"Remote Path: {REMOTE_PATH}")
    print("=" * 50)

    try:
        # Connect to FTP
        print("\nConnecting to FTP server...")
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASSWORD)
        print("Connected successfully!")

        # Step 1: Backup existing database
        print("\nStep 1: Backing up existing database...")
        try:
            ftp.rename(f"{REMOTE_PATH}/db.sqlite3", f"{REMOTE_PATH}/db.sqlite3.backup")
            print("Database backed up successfully")
        except:
            print("Database backup skipped (file may not exist)")

        # Step 2: Upload database
        print("\nStep 2: Uploading database file...")
        if not upload_file(ftp, f"{LOCAL_PATH}\\db.sqlite3", f"{REMOTE_PATH}/db.sqlite3"):
            print("Database upload failed. Aborting.")
            ftp.quit()
            sys.exit(1)

        # Step 3: Upload logo files
        print("\nStep 3: Uploading logo files...")
        upload_file(ftp, f"{LOCAL_PATH}\\logo.jpg", f"{REMOTE_PATH}/logo.jpg")
        upload_file(ftp, f"{LOCAL_PATH}\\static\\images\\crackers\\logo.jpg", f"{REMOTE_PATH}/static/images/crackers/logo.jpg")
        upload_file(ftp, f"{LOCAL_PATH}\\staticfiles\\images\\crackers\\logo.jpg", f"{REMOTE_PATH}/staticfiles/images/crackers/logo.jpg")

        # Step 4: Upload static files
        print("\nStep 4: Uploading static files...")
        upload_directory(ftp, f"{LOCAL_PATH}\\static\\css", f"{REMOTE_PATH}/static/css")
        upload_directory(ftp, f"{LOCAL_PATH}\\static\\js", f"{REMOTE_PATH}/static/js")
        upload_directory(ftp, f"{LOCAL_PATH}\\static\\images", f"{REMOTE_PATH}/static/images")

        # Step 5: Upload staticfiles
        print("\nStep 5: Uploading staticfiles...")
        upload_directory(ftp, f"{LOCAL_PATH}\\staticfiles\\css", f"{REMOTE_PATH}/staticfiles/css")
        upload_directory(ftp, f"{LOCAL_PATH}\\staticfiles\\js", f"{REMOTE_PATH}/staticfiles/js")
        upload_directory(ftp, f"{LOCAL_PATH}\\staticfiles\\images", f"{REMOTE_PATH}/staticfiles/images")

        # Close connection
        ftp.quit()

        print("\n" + "=" * 50)
        print("Deployment completed successfully!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Visit http://redapplecrackers.com/ to verify")
        print("2. Check that the logo is updated")
        print("3. Check that product images are displaying correctly")
        print("4. You may need to restart Passenger in cPanel if changes don't appear")
        print()

    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Verify your FTP credentials are correct")
        print("2. Check that FTP is enabled in your GoDaddy cPanel")
        print("3. Try using File Manager in cPanel instead")
        sys.exit(1)

if __name__ == "__main__":
    main()
