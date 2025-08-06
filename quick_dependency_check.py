#!/usr/bin/env python3
"""
Quick Dependency Checker for Pionex Trading Bot
Simple script to quickly check if all required dependencies are installed
"""

import sys
import importlib
from typing import Dict, List

def check_package(package_name: str, import_name: str = None) -> bool:
    """Check if a package can be imported"""
    try:
        import_name = import_name or package_name
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def get_package_version(package_name: str) -> str:
    """Get version of an installed package"""
    try:
        module = importlib.import_module(package_name)
        if hasattr(module, '__version__'):
            return module.__version__
        else:
            return 'unknown'
    except ImportError:
        return 'not_installed'

def quick_check():
    """Run quick dependency check"""
    print("🔍 Quick Dependency Check for Pionex Trading Bot")
    print("=" * 50)
    
    # Core dependencies
    core_deps = {
        'Flask': 'flask',
        'Flask-SocketIO': 'flask_socketio',
        'requests': 'requests',
        'python-dotenv': 'dotenv',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'ta': 'ta',
        'aiohttp': 'aiohttp',
        'websockets': 'websockets',
        'schedule': 'schedule',
        'pytz': 'pytz',
        'PyYAML': 'yaml',
        'psutil': 'psutil',
        'eventlet': 'eventlet',
        'matplotlib': 'matplotlib'
    }
    
    # Optional dependencies
    optional_deps = {
        'tkinter': 'tkinter',
        'PIL': 'PIL',
        'scipy': 'scipy',
        'scikit-learn': 'sklearn',
        'plotly': 'plotly',
        'seaborn': 'seaborn'
    }
    
    print("\n📦 Core Dependencies:")
    print("-" * 30)
    
    core_results = {}
    for package, import_name in core_deps.items():
        if check_package(package, import_name):
            version = get_package_version(import_name)
            print(f"✅ {package}: {version}")
            core_results[package] = True
        else:
            print(f"❌ {package}: NOT INSTALLED")
            core_results[package] = False
    
    print("\n🔧 Optional Dependencies:")
    print("-" * 30)
    
    optional_results = {}
    for package, import_name in optional_deps.items():
        if check_package(package, import_name):
            version = get_package_version(import_name)
            print(f"✅ {package}: {version}")
            optional_results[package] = True
        else:
            print(f"⚠️  {package}: NOT INSTALLED (optional)")
            optional_results[package] = False
    
    # Summary
    print("\n📊 Summary:")
    print("-" * 30)
    
    core_installed = sum(core_results.values())
    core_total = len(core_results)
    optional_installed = sum(optional_results.values())
    optional_total = len(optional_results)
    
    print(f"Core Dependencies: {core_installed}/{core_total} installed")
    print(f"Optional Dependencies: {optional_installed}/{optional_total} installed")
    
    if core_installed == core_total:
        print("\n🎉 All core dependencies are installed!")
        return True
    else:
        missing = [pkg for pkg, installed in core_results.items() if not installed]
        print(f"\n❌ Missing core dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"\n🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 7):
        print("❌ Python 3.7+ is required")
        return False
    elif version < (3, 8):
        print("⚠️  Python 3.8+ is recommended")
    else:
        print("✅ Python version is compatible")
    
    return True

def main():
    """Main function"""
    print("🔍 Pionex Trading Bot - Quick Dependency Check")
    print("=" * 60)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check dependencies
    deps_ok = quick_check()
    
    print("\n" + "=" * 60)
    
    if python_ok and deps_ok:
        print("🎉 All checks passed! You're ready to run the trading bot.")
        sys.exit(0)
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 