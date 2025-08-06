#!/usr/bin/env python3
"""
Dependency Fixer for Pionex Trading Bot
Fixes common dependency issues and version conflicts
"""

import subprocess
import sys
import os
from typing import List, Dict

def run_command(command: str) -> bool:
    """Run a command and return success status"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {command}")
            return True
        else:
            print(f"❌ Failed: {command}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def check_python_version():
    """Check and suggest Python version fixes"""
    print("\n🐍 Checking Python version...")
    
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 7):
        print("❌ Python 3.7+ is required")
        print("💡 Solution: Install Python 3.8 or higher")
        return False
    elif version < (3, 8):
        print("⚠️  Python 3.8+ is recommended")
        print("💡 Solution: Consider upgrading to Python 3.8+ for better performance")
        return True
    else:
        print("✅ Python version is compatible")
        return True

def fix_core_dependencies():
    """Fix core dependencies"""
    print("\n📦 Fixing core dependencies...")
    
    # Install/upgrade core dependencies
    core_packages = [
        "Flask==2.3.3",
        "Flask-SocketIO==5.3.6",
        "Werkzeug==2.3.7",
        "requests==2.31.0",
        "python-dotenv==1.0.0",
        "pandas==2.1.4",
        "numpy==1.24.3",
        "ta==0.10.2",
        "aiohttp==3.9.1",
        "websockets==12.0",
        "schedule==1.2.0",
        "pytz==2023.3",
        "PyYAML==6.0.1",
        "psutil==5.9.6",
        "eventlet==0.33.3",
        "matplotlib==3.7.2"
    ]
    
    success_count = 0
    for package in core_packages:
        if run_command(f"pip install {package}"):
            success_count += 1
    
    print(f"\n📊 Core dependencies: {success_count}/{len(core_packages)} installed successfully")
    return success_count == len(core_packages)

def fix_version_conflicts():
    """Fix known version conflicts"""
    print("\n🔧 Fixing version conflicts...")
    
    # Fix NumPy and pandas compatibility
    print("Fixing NumPy and pandas compatibility...")
    run_command("pip install numpy==1.24.3")
    run_command("pip install pandas==2.1.4")
    
    # Fix Flask and Werkzeug compatibility
    print("Fixing Flask and Werkzeug compatibility...")
    run_command("pip install Flask==2.3.3")
    run_command("pip install Werkzeug==2.3.7")
    
    # Fix matplotlib backend issues
    print("Fixing matplotlib backend...")
    run_command("pip install matplotlib==3.7.2")
    
    return True

def install_optional_dependencies():
    """Install optional dependencies"""
    print("\n🔧 Installing optional dependencies...")
    
    optional_packages = [
        "Pillow",  # PIL
        "scipy",
        "scikit-learn",
        "plotly",
        "seaborn"
    ]
    
    success_count = 0
    for package in optional_packages:
        if run_command(f"pip install {package}"):
            success_count += 1
    
    print(f"\n📊 Optional dependencies: {success_count}/{len(optional_packages)} installed successfully")
    return success_count

def create_virtual_environment():
    """Create and activate virtual environment"""
    print("\n🔧 Setting up virtual environment...")
    
    venv_name = "pionex_env"
    
    # Check if virtual environment exists
    if os.path.exists(venv_name):
        print(f"Virtual environment '{venv_name}' already exists")
        return True
    
    # Create virtual environment
    if run_command(f"python -m venv {venv_name}"):
        print(f"✅ Virtual environment '{venv_name}' created successfully")
        print(f"💡 To activate: {venv_name}\\Scripts\\activate (Windows) or source {venv_name}/bin/activate (Linux/Mac)")
        return True
    else:
        print("❌ Failed to create virtual environment")
        return False

def generate_requirements_file():
    """Generate updated requirements.txt"""
    print("\n📝 Generating updated requirements.txt...")
    
    requirements_content = """# Core Web Framework
Flask==2.3.3
Flask-SocketIO==5.3.6
Werkzeug==2.3.7

# HTTP and Networking
requests==2.31.0
aiohttp==3.9.1
websockets==12.0

# Environment and Configuration
python-dotenv==1.0.0
PyYAML==6.0.1
pytz==2023.3

# Data Processing and Analysis
pandas==2.1.4
numpy==1.24.3
ta==0.10.2

# Technical Analysis and Charting
matplotlib==3.7.2

# System and Process Management
psutil==5.9.6
schedule==1.2.0

# Async and Event Handling
asyncio==3.4.3
eventlet==0.33.3

# Optional Dependencies (uncomment if needed)
# Pillow  # PIL replacement
# scipy
# scikit-learn
# plotly
# seaborn
"""
    
    try:
        with open("requirements_fixed.txt", "w") as f:
            f.write(requirements_content)
        print("✅ Generated requirements_fixed.txt")
        return True
    except Exception as e:
        print(f"❌ Failed to generate requirements file: {e}")
        return False

def main():
    """Main function to fix dependencies"""
    print("🔧 Pionex Trading Bot - Dependency Fixer")
    print("=" * 60)
    
    # Check Python version
    python_ok = check_python_version()
    
    if not python_ok:
        print("\n❌ Python version issue must be fixed manually")
        print("Please install Python 3.8 or higher")
        return False
    
    # Ask user what to fix
    print("\n🔧 What would you like to fix?")
    print("1. Install/upgrade all core dependencies")
    print("2. Fix version conflicts")
    print("3. Install optional dependencies")
    print("4. Create virtual environment")
    print("5. Generate updated requirements file")
    print("6. All of the above")
    
    try:
        choice = input("\nEnter your choice (1-6): ").strip()
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        return False
    
    success = True
    
    if choice in ['1', '6']:
        success &= fix_core_dependencies()
    
    if choice in ['2', '6']:
        success &= fix_version_conflicts()
    
    if choice in ['3', '6']:
        install_optional_dependencies()
    
    if choice in ['4', '6']:
        success &= create_virtual_environment()
    
    if choice in ['5', '6']:
        success &= generate_requirements_file()
    
    print("\n" + "=" * 60)
    
    if success:
        print("🎉 Dependency fixing completed successfully!")
        print("\n💡 Next steps:")
        print("1. Run: python quick_dependency_check.py")
        print("2. Run: python gui_app.py")
    else:
        print("❌ Some dependency fixes failed")
        print("Please check the errors above and try again")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Operation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(2) 