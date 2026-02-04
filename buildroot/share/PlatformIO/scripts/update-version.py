#!/usr/bin/env python
"""
Update firmware version with timestamp before build
"""
Import("env")
import os
import re
from datetime import datetime

def update_version(source, target, env):
    # Path to Version.h (correct location)
    version_file = os.path.join("Marlin", "src", "inc", "Version.h")
    
    if not os.path.exists(version_file):
        print(f"⚠️  Version.h not found at {version_file}")
        return
    
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
    else:
        print(f"⚠️  Failed to update version (pattern not matched)")

# Register the callback to run before build
env.AddPreAction("buildprog", update_version)
