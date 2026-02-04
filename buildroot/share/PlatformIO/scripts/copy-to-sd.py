#!/usr/bin/env python
"""
Copy firmware.bin to SD card with a unique timestamped name
"""
Import("env")
import os
import shutil
from datetime import datetime

def copy_to_sd(source, target, env):
    # Path to the built firmware
    firmware_path = str(target[0])
    
    # SD card drive letter (change this to your SD card drive)
    sd_drive = "E:\\"  # Change to your SD card drive letter
    
    # Check if SD card is accessible
    if not os.path.exists(sd_drive):
        print(f"⚠️  SD card not found at {sd_drive}")
        print("   Update SD_DRIVE in buildroot/share/PlatformIO/scripts/copy-to-sd.py")
        return
    
    # Delete all files in SD card root directory
    print("🗑️  Cleaning SD card...")
    deleted_count = 0
    for item in os.listdir(sd_drive):
        item_path = os.path.join(sd_drive, item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                deleted_count += 1
                print(f"   Deleted: {item}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                deleted_count += 1
                print(f"   Deleted folder: {item}")
        except Exception as e:
            print(f"   ⚠️  Could not delete {item}: {e}")
    
    if deleted_count > 0:
        print(f"✅ Cleaned {deleted_count} item(s) from SD card")
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_name = f"firmware_{timestamp}.bin"
    destination = os.path.join(sd_drive, new_name)
    
    # Copy the file
    try:
        shutil.copy2(firmware_path, destination)
        print(f"✅ Firmware copied to SD card: {new_name}")
    except Exception as e:
        print(f"❌ Failed to copy firmware: {e}")

# Register the callback
env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", copy_to_sd)
