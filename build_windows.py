#!/usr/bin/env python3
"""
Build script for creating Windows .exe executables
Can be run on Windows directly, or on Linux with Wine
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def check_pyinstaller():
    """Check if PyInstaller is available"""
    try:
        # Try running via python -m PyInstaller
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception:
        return False


def install_pyinstaller():
    """Install PyInstaller if not available"""
    print("\n📦 Installing PyInstaller...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            check=True
        )
        print("✅ PyInstaller installed successfully!\n")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install PyInstaller")
        return False


def build_windows_exe():
    """Build Windows .exe file"""
    print("=" * 70)
    print("Building AlfaGeir XBoard Engine - Windows .exe")
    print("=" * 70)
    
    # Check platform
    is_windows = platform.system() == 'Windows'
    
    if not is_windows:
        print("\n⚠️  WARNING: Building Windows .exe on non-Windows system")
        print("   This requires Wine or building on actual Windows")
        print("\n   Recommended approaches:")
        print("   1. Run this script on Windows")
        print("   2. Use GitHub Actions (see build_windows_github.yml)")
        print("   3. Use Wine (advanced)")
        print("\n   Continuing anyway...\n")
    
    # Use python -m PyInstaller to avoid PATH issues
    cmd = [
        sys.executable, "-m", "PyInstaller",
        '--onefile',  # Single executable file
        '--name', 'alfageir-xboard.exe',  # Windows executable name
        '--console',  # Console application
        '--clean',  # Clean before building
        'xboard_engine.py'
    ]
    
    print("Running: python -m PyInstaller", ' '.join(cmd[3:]))
    print()
    
    try:
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("\n" + "=" * 70)
            print("✅ SUCCESS! Windows executable created!")
            print("=" * 70)
            
            exe_path = os.path.join('dist', 'alfageir-xboard.exe')
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"\nExecutable: {Path(exe_path).absolute()}")
                print(f"Size: {size_mb:.1f} MB")
                print("\nYou can now:")
                print("  1. Run: dist\\alfageir-xboard.exe")
                print("  2. Use with WinBoard/Arena/Cute Chess")
                print("  3. Copy to other Windows PCs (no Python needed!)")
            else:
                print(f"\n⚠️  Expected executable not found at: {exe_path}")
            print("=" * 70)
        else:
            print("\n❌ Build failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def main():
    """Main build function"""
    print("\n🚀 AlfaGeir Chess Engine - Windows Build System")
    print("=" * 70)
    
    # Check/install PyInstaller
    if not check_pyinstaller():
        print("⚠️  PyInstaller not found")
        if not install_pyinstaller():
            print("\n❌ Cannot continue without PyInstaller")
            print("   Try manually: python -m pip install pyinstaller")
            sys.exit(1)
    else:
        print("✅ PyInstaller is available\n")
    
    # Check if on Windows or show warning
    if platform.system() != 'Windows':
        print("\n⚠️  You are running on:", platform.system())
        print("   To build Windows .exe, you have these options:\n")
        print("   Option 1 (RECOMMENDED): Use GitHub Actions")
        print("   ----------------------------------------")
        print("   - Push code to GitHub")
        print("   - GitHub will build Windows .exe automatically")
        print("   - Download from Actions artifacts\n")
        
        print("   Option 2: Build on actual Windows")
        print("   ---------------------------------")
        print("   - Copy project to Windows machine")
        print("   - Install: pip install pyinstaller chess")
        print("   - Run: python build_windows.py\n")
        
        print("   Option 3: Use Wine (complex)")
        print("   ---------------------------")
        print("   - Install Wine and Windows Python")
        print("   - Configure Wine environment")
        print("   - Run PyInstaller through Wine\n")
        
        response = input("Continue anyway? (y/N): ").lower()
        if response != 'y':
            print("Cancelled.")
            sys.exit(0)
    
    build_windows_exe()


if __name__ == "__main__":
    main()
