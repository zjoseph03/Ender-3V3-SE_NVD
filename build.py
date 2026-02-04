#!/usr/bin/env python
"""
Build script that updates version and then builds firmware
Usage: python build.py
"""
import os
import re
import subprocess
import sys
from datetime import datetime

def update_version():
    """Update the firmware version with timestamp"""
    version_file = os.path.join("Marlin", "src", "inc", "Version.h")
    
    if not os.path.exists(version_file):
        print(f"❌ Version.h not found at {version_file}")
        return False
    
    # Generate version string with timestamp (includes seconds for uniqueness)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_version = f"NVD_{timestamp}"
    
    # Read the file
    with open(version_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the version line inside the HIGH_SPEED_1 condition
    pattern = r'(#if ENABLED\(HIGH_SPEED_1\)\s+#define SHORT_BUILD_VERSION\s+")[^"]*(")'
    replacement = rf'\g<1>{new_version}\g<2>'
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Write back if changed
    if new_content != content:
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Updated firmware version to: {new_version}")
        return True
    else:
        print(f"⚠️  Failed to update version (pattern not matched)")
        return False

def build_firmware():
    """Run PlatformIO build command"""
    print("\n🔨 Building firmware...")
    result = subprocess.run(
        ["platformio", "run", "--silent", "-e", "STM32F103RET6_creality"],
        cwd=os.getcwd()
    )
    return result.returncode == 0

if __name__ == "__main__":
    print("=" * 60)
    print("Marlin Firmware Build Script")
    print("=" * 60)
    
    # Step 1: Update version
    if not update_version():
        print("\n⚠️  Version update failed, but continuing with build...")
    
    # Step 2: Build firmware
    if build_firmware():
        print("\n✅ Build completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Build failed!")
        sys.exit(1)
