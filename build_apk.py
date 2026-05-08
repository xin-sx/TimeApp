#!/usr/bin/env python3
"""
Android APK 自动构建脚本
在有网络的电脑上运行此脚本即可构建APK
"""

import os
import subprocess
import sys
import zipfile
import shutil

PROJECT_DIR = "/workspace/TimeApp"

def check_environment():
    """检查环境"""
    print("检查构建环境...")
    
    # 检查Java
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        print(f"✓ Java 已安装: {result.stderr.split()[2]}")
    except:
        print("✗ Java 未安装，请先安装 JDK 8 或更高版本")
        return False
    
    # 检查Gradle或Android SDK
    has_gradle = shutil.which('gradle') is not None
    has_android = os.path.exists(os.path.expanduser('~/Android/Sdk')) or os.environ.get('ANDROID_HOME')
    
    if has_gradle or has_android:
        print("✓ Android 构建工具已就绪")
        return True
    else:
        print("✗ 未检测到 Gradle 或 Android SDK")
        print("  请安装 Android Studio 或 Android SDK")
        return False

def download_android_studio():
    """下载 Android Studio"""
    print("\n建议安装 Android Studio:")
    print("1. 访问 https://developer.android.com/studio")
    print("2. 下载并安装 Android Studio")
    print("3. 安装完成后，打开此项目并构建 APK")

def build_with_gradle():
    """使用 Gradle 构建"""
    print("\n正在使用 Gradle 构建...")
    
    os.chdir(PROJECT_DIR)
    
    # 尝试使用 gradlew
    gradlew = os.path.join(PROJECT_DIR, 'gradlew')
    if os.path.exists(gradlew):
        os.chmod(gradlew, 0o755)
        cmd = [gradlew, 'assembleRelease']
    else:
        cmd = ['gradle', 'assembleRelease']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            print("✓ 构建成功!")
            apk_path = os.path.join(PROJECT_DIR, 'app/build/outputs/apk/release/app-release.apk')
            if os.path.exists(apk_path):
                print(f"\nAPK 文件位置: {apk_path}")
                print(f"文件大小: {os.path.getsize(apk_path) / 1024 / 1024:.2f} MB")
            return True
        else:
            print(f"✗ 构建失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ 构建出错: {e}")
        return False

def create_package_zip():
    """创建项目压缩包"""
    print("\n正在创建项目压缩包...")
    
    zip_path = '/workspace/TimeApp.zip'
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('/workspace/TimeApp'):
            # 排除构建目录
            if 'build' in dirs:
                dirs.remove('build')
            for file in files:
                if file.endswith('.gradle') or file.endswith('.xml') or file.endswith('.properties') or file.endswith('.java') or file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, '/workspace')
                    zipf.write(file_path, arcname)
    
    print(f"✓ 项目压缩包已创建: {zip_path}")
    return zip_path

def main():
    print("=" * 50)
    print("TimeApp Android APK 构建工具")
    print("=" * 50)
    
    if not check_environment():
        download_android_studio()
        create_package_zip()
        return
    
    if build_with_gradle():
        print("\n" + "=" * 50)
        print("构建完成!")
        print("=" * 50)
    else:
        print("\n构建失败，请检查错误信息")
        download_android_studio()

if __name__ == "__main__":
    main()
