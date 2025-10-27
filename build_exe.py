#!/usr/bin/env python3
"""
Build script for creating AlfaGeir executables
Creates standalone executables for both GUI and XBoard versions
"""

import subprocess
import sys
import os


def build_xboard_engine():
    """Build the XBoard engine executable"""
    print("=" * 70)
    print("Building AlfaGeir XBoard Engine Executable")
    print("=" * 70)
    
    cmd = [
        'pyinstaller',
        '--onefile',  # Single executable file
        '--name', 'alfageir-xboard',  # Output name
        '--console',  # Console application
        '--clean',  # Clean before building
        'xboard_engine.py'
    ]
    
    print("\nRunning:", ' '.join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "=" * 70)
        print("✅ SUCCESS! XBoard engine executable created!")
        print("=" * 70)
        print("\nExecutable location:")
        print("  ./dist/alfageir-xboard")
        print("\nYou can run it with:")
        print("  ./dist/alfageir-xboard")
        print("\nOr use it with XBoard:")
        print("  xboard -fcp './dist/alfageir-xboard'")
        print("=" * 70)
    else:
        print("\n❌ Build failed!")
        sys.exit(1)


def build_gui():
    """Build the GUI executable"""
    print("\n" + "=" * 70)
    print("Building AlfaGeir GUI Executable")
    print("=" * 70)
    
    # Check if images directory exists
    if not os.path.exists('images'):
        print("⚠️  Warning: images directory not found")
        print("   GUI may not work without chess piece images")
    
    cmd = [
        'pyinstaller',
        '--onefile',  # Single executable file
        '--name', 'alfageir-gui',  # Output name
        '--windowed',  # No console (GUI app)
        '--add-data', 'images:images',  # Include images
        '--clean',  # Clean before building
        'chessboard.py'
    ]
    
    print("\nRunning:", ' '.join(cmd))
    print()
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "=" * 70)
        print("✅ SUCCESS! GUI executable created!")
        print("=" * 70)
        print("\nExecutable location:")
        print("  ./dist/alfageir-gui")
        print("\nYou can run it with:")
        print("  ./dist/alfageir-gui")
        print("=" * 70)
    else:
        print("\n❌ Build failed!")
        sys.exit(1)


def main():
    """Main build function"""
    print("\n🚀 AlfaGeir Chess Engine - Build System")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'xboard':
            build_xboard_engine()
        elif sys.argv[1] == 'gui':
            build_gui()
        elif sys.argv[1] == 'all':
            build_xboard_engine()
            build_gui()
        else:
            print("\nUsage: python build_exe.py [xboard|gui|all]")
            print("\n  xboard - Build XBoard engine only")
            print("  gui    - Build GUI only")
            print("  all    - Build both")
            sys.exit(1)
    else:
        # Default: build XBoard engine only
        print("\nBuilding XBoard engine (default)")
        print("Use 'python build_exe.py all' to build both\n")
        build_xboard_engine()


if __name__ == "__main__":
    main()
