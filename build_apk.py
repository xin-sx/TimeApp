#!/usr/bin/env python3
import os
import shutil
import zipfile
import subprocess
import glob

def build_apk():
    print("Building APK manually...")
    
    # Create output directories
    os.makedirs('app/build/outputs/apk/debug', exist_ok=True)
    
    # Build directory structure for APK
    apk_dir = 'app/build/outputs/apk/debug/tmp_apk'
    os.makedirs(apk_dir, exist_ok=True)
    
    # Copy manifest
    shutil.copy('app/src/main/AndroidManifest.xml', apk_dir)
    
    # Copy resources
    for res_dir in ['layout', 'values', 'xml']:
        src = f'app/src/main/res/{res_dir}'
        dst = os.path.join(apk_dir, 'res', res_dir)
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(src):
            shutil.copy(os.path.join(src, f), dst)
    
    # Copy drawables
    for mipmap in glob.glob('app/src/main/res/mipmap-*'):
        dst = os.path.join(apk_dir, 'res', os.path.basename(mipmap))
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(mipmap):
            shutil.copy(os.path.join(mipmap, f), dst)
    
    # Compile Java to dex
    print("Compiling Java...")
    subprocess.run([
        'javac',
        '-d', '/tmp/timeapp_classes',
        '-cp', 'libs/android.jar',
        'app/src/main/java/com/example/timeapp/MainActivity.java'
    ], check=True)
    
    # Convert to dex
    print("Converting to dex...")
    subprocess.run([
        'd8',
        '--output', os.path.join(apk_dir, 'classes.dex'),
        '/tmp/timeapp_classes/com/example/timeapp/MainActivity.class'
    ], check=True)
    
    # Add empty META-INF directory
    os.makedirs(os.path.join(apk_dir, 'META-INF'), exist_ok=True)
    
    # Create APK zip
    apk_path = 'app/build/outputs/apk/debug/app-debug.apk'
    print(f"Creating APK: {apk_path}")
    
    with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(apk_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, apk_dir)
                z.write(full_path, rel_path)
    
    # Sign APK
    print("Signing APK...")
    subprocess.run([
        'apksigner',
        'sign',
        '--ks', '/tmp/debug.keystore',
        '--ks-pass', 'pass:android',
        '--key-pass', 'pass:android',
        apk_path
    ], check=True)
    
    print(f"APK built successfully: {apk_path}")

if __name__ == '__main__':
    build_apk()