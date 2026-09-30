"""
GoDaddy SSH Deployment Script for Windows
This script deploys the crackers website to GoDaddy via SSH
"""

import os
import sys
import subprocess
from pathlib import Path

# Configuration
SSH_HOST = "redapplecrackers.com"
SSH_USER = "gs26214tgb0g"
REMOTE_PATH = "/home/gs26214tgb0g/redapple-crackers"
LOCAL_PATH = r"C:\Users\Divya\OneDrive\Desktop\crackers"

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"Success: {description}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {description}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("=" * 50)
    print("GoDaddy SSH Deployment Script")
    print("=" * 50)
    print(f"Host: {SSH_HOST}")
    print(f"User: {SSH_USER}")
    print(f"Remote Path: {REMOTE_PATH}")
    print("=" * 50)

    # Step 1: Backup existing database on remote server
    backup_cmd = f'ssh {SSH_USER}@{SSH_HOST} "cd {REMOTE_PATH} && cp db.sqlite3 db.sqlite3.backup"'
    if not run_command(backup_cmd, "Backing up existing database on GoDaddy"):
        print("Database backup failed. Aborting.")
        sys.exit(1)

    # Step 2: Upload database
    db_upload_cmd = f'scp "{LOCAL_PATH}\\db.sqlite3" {SSH_USER}@{SSH_HOST}:{REMOTE_PATH}/'
    if not run_command(db_upload_cmd, "Uploading database file"):
        print("Database upload failed. Aborting.")
        sys.exit(1)

    # Step 3: Upload logo files
    logo_upload_cmd1 = f'scp "{LOCAL_PATH}\\logo.jpg" {SSH_USER}@{SSH_HOST}:{REMOTE_PATH}/'
    logo_upload_cmd2 = f'scp "{LOCAL_PATH}\\static\\images\\crackers\\logo.jpg" {SSH_USER}@{SSH_HOST}:{REMOTE_PATH}/static/images/crackers/'
    logo_upload_cmd3 = f'scp "{LOCAL_PATH}\\staticfiles\\images\\crackers\\logo.jpg" {SSH_USER}@{SSH_HOST}:{REMOTE_PATH}/staticfiles/images/crackers/'

    if not run_command(logo_upload_cmd1, "Uploading root logo"):
        print("Root logo upload failed. Aborting.")
        sys.exit(1)

    if not run_command(logo_upload_cmd2, "Uploading static logo"):
        print("Static logo upload failed. Aborting.")
        sys.exit(1)

    if not run_command(logo_upload_cmd3, "Uploading staticfiles logo"):
        print("Staticfiles logo upload failed. Aborting.")
        sys.exit(1)

    # Step 4: Upload static files
    static_css_cmd = f'scp -r "{LOCAL_PATH}\\static\\css" {SSH_USER}@{SSH_HOST}:{REMOTE_PATH}/static/'
    static_js_cmd = f'scp -r "{LOCAL_PATH}\\static\\js" {SSH_USER}@{SSH_HOST}:{REMOTE_PATH}/static/'
    static_images_cmd = f'scp -r "{LOCAL_PATH}\\static\\images" {SSH_USER}@{SSH_HOST}:{REMOTE_PATH}/static/'

    if not run_command(static_css_cmd, "Uploading static CSS files"):
        print("Static CSS upload failed. Aborting.")
        sys.exit(1)

    if not run_command(static_js_cmd, "Uploading static JS files"):
        print("Static JS upload failed. Aborting.")
        sys.exit(1)

    if not run_command(static_images_cmd, "Uploading static images"):
        print("Static images upload failed. Aborting.")
        sys.exit(1)

    # Step 5: Upload staticfiles (collected static)
    staticfiles_css_cmd = f'scp -r "{LOCAL_PATH}\\staticfiles\\css" {SSH_USER}@{SSH_HOST}:{REMOTE_PATH}/staticfiles/'
    staticfiles_js_cmd = f'scp -r "{LOCAL_PATH}\\staticfiles\\js" {SSH_USER}@{SSH_HOST}:{REMOTE_PATH}/staticfiles/'
    staticfiles_images_cmd = f'scp -r "{LOCAL_PATH}\\staticfiles\\images" {SSH_USER}@{SSH_HOST}:{REMOTE_PATH}/staticfiles/'

    if not run_command(staticfiles_css_cmd, "Uploading staticfiles CSS"):
        print("Staticfiles CSS upload failed. Aborting.")
        sys.exit(1)

    if not run_command(staticfiles_js_cmd, "Uploading staticfiles JS"):
        print("Staticfiles JS upload failed. Aborting.")
        sys.exit(1)

    if not run_command(staticfiles_images_cmd, "Uploading staticfiles images"):
        print("Staticfiles images upload failed. Aborting.")
        sys.exit(1)

    # Step 6: Restart Passenger application
    restart_cmd = f'ssh {SSH_USER}@{SSH_HOST} "cd {REMOTE_PATH} && touch passenger_wsgi.py"'
    if not run_command(restart_cmd, "Restarting Passenger application"):
        print("Passenger restart failed. Aborting.")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Deployment completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Visit http://redapplecrackers.com/ to verify")
    print("2. Check that the logo is updated")
    print("3. Check that product images are displaying correctly")
    print()

if __name__ == "__main__":
    main()
