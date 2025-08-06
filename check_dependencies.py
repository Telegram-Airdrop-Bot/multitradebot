#!/usr/bin/env python3
"""
Dependency Compatibility Checker for Pionex Trading Bot
Checks all dependencies for version compatibility and conflicts
"""

import subprocess
import sys
import pkg_resources
import importlib
from typing import Dict, List, Tuple
import json
from datetime import datetime

class DependencyChecker:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.success = []
        
    def log_issue(self, message: str, severity: str = "ERROR"):
        """Log an issue with severity level"""
        self.issues.append({
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        })
        print(f"❌ {severity}: {message}")
    
    def log_warning(self, message: str):
        """Log a warning"""
        self.warnings.append({
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        print(f"⚠️  WARNING: {message}")
    
    def log_success(self, message: str):
        """Log a success message"""
        self.success.append({
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        print(f"✅ SUCCESS: {message}")
    
    def check_python_version(self) -> bool:
        """Check Python version compatibility"""
        print("\n🐍 Checking Python version...")
        
        version = sys.version_info
        print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
        
        # Check minimum Python version (3.7+)
        if version < (3, 7):
            self.log_issue("Python 3.7 or higher is required", "CRITICAL")
            return False
        elif version < (3, 8):
            self.log_warning("Python 3.8+ is recommended for better performance")
        else:
            self.log_success(f"Python {version.major}.{version.minor} is compatible")
        
        return True
    
    def get_installed_packages(self) -> Dict[str, str]:
        """Get all installed packages and their versions"""
        try:
            installed = {}
            for dist in pkg_resources.working_set:
                installed[dist.project_name] = dist.version
            return installed
        except Exception as e:
            self.log_issue(f"Failed to get installed packages: {e}")
            return {}
    
    def check_package_import(self, package_name: str, import_name: str = None) -> bool:
        """Check if a package can be imported"""
        try:
            import_name = import_name or package_name
            importlib.import_module(import_name)
            return True
        except ImportError:
            return False
    
    def check_core_dependencies(self) -> Dict[str, bool]:
        """Check core dependencies"""
        print("\n📦 Checking core dependencies...")
        
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
        
        results = {}
        for package, import_name in core_deps.items():
            if self.check_package_import(package, import_name):
                self.log_success(f"{package} is installed and importable")
                results[package] = True
            else:
                self.log_issue(f"{package} is not installed or not importable")
                results[package] = False
        
        return results
    
    def check_version_compatibility(self) -> Dict[str, Dict]:
        """Check version compatibility for key packages"""
        print("\n🔍 Checking version compatibility...")
        
        installed = self.get_installed_packages()
        
        # Define compatibility requirements
        compatibility_requirements = {
            'Flask': {
                'min': '2.0.0',
                'max': '3.0.0',
                'recommended': '2.3.3',
                'description': 'Web framework'
            },
            'Flask-SocketIO': {
                'min': '5.0.0',
                'max': '6.0.0',
                'recommended': '5.3.6',
                'description': 'WebSocket support'
            },
            'requests': {
                'min': '2.25.0',
                'max': '3.0.0',
                'recommended': '2.31.0',
                'description': 'HTTP library'
            },
            'pandas': {
                'min': '1.3.0',
                'max': '3.0.0',
                'recommended': '2.1.4',
                'description': 'Data manipulation'
            },
            'numpy': {
                'min': '1.21.0',
                'max': '2.0.0',
                'recommended': '1.24.3',
                'description': 'Numerical computing'
            },
            'matplotlib': {
                'min': '3.5.0',
                'max': '4.0.0',
                'recommended': '3.7.0',
                'description': 'Plotting library'
            }
        }
        
        results = {}
        
        for package, requirements in compatibility_requirements.items():
            if package in installed:
                current_version = installed[package]
                results[package] = {
                    'current': current_version,
                    'status': 'unknown',
                    'message': ''
                }
                
                # Parse version numbers
                try:
                    current_parts = [int(x) for x in current_version.split('.')]
                    min_parts = [int(x) for x in requirements['min'].split('.')]
                    max_parts = [int(x) for x in requirements['max'].split('.')]
                    recommended_parts = [int(x) for x in requirements['recommended'].split('.')]
                    
                    # Check minimum version
                    if current_parts < min_parts:
                        self.log_issue(f"{package} {current_version} is too old. Minimum: {requirements['min']}")
                        results[package]['status'] = 'too_old'
                        results[package]['message'] = f"Version {current_version} is too old"
                    
                    # Check maximum version
                    elif current_parts >= max_parts:
                        self.log_warning(f"{package} {current_version} is newer than tested. Max tested: {requirements['max']}")
                        results[package]['status'] = 'too_new'
                        results[package]['message'] = f"Version {current_version} is newer than tested"
                    
                    # Check if it's the recommended version
                    elif current_version == requirements['recommended']:
                        self.log_success(f"{package} {current_version} is the recommended version")
                        results[package]['status'] = 'recommended'
                        results[package]['message'] = f"Version {current_version} is recommended"
                    
                    else:
                        self.log_success(f"{package} {current_version} is compatible")
                        results[package]['status'] = 'compatible'
                        results[package]['message'] = f"Version {current_version} is compatible"
                        
                except ValueError:
                    self.log_warning(f"Could not parse version for {package}: {current_version}")
                    results[package]['status'] = 'unknown'
                    results[package]['message'] = f"Could not parse version {current_version}"
            else:
                self.log_issue(f"{package} is not installed")
                results[package] = {
                    'current': 'not_installed',
                    'status': 'missing',
                    'message': 'Package not installed'
                }
        
        return results
    
    def check_conflicts(self) -> List[Dict]:
        """Check for known package conflicts"""
        print("\n⚠️  Checking for known conflicts...")
        
        conflicts = []
        
        # Check for common conflicts
        installed = self.get_installed_packages()
        
        # Flask and Werkzeug version conflicts
        if 'Flask' in installed and 'Werkzeug' in installed:
            flask_version = installed['Flask']
            werkzeug_version = installed['Werkzeug']
            
            # Flask 2.3.x requires Werkzeug 2.3.x
            if flask_version.startswith('2.3') and not werkzeug_version.startswith('2.3'):
                conflict = {
                    'type': 'version_conflict',
                    'packages': ['Flask', 'Werkzeug'],
                    'message': f'Flask {flask_version} requires Werkzeug 2.3.x, but {werkzeug_version} is installed'
                }
                conflicts.append(conflict)
                self.log_issue(conflict['message'])
        
        # NumPy and pandas version conflicts
        if 'numpy' in installed and 'pandas' in installed:
            numpy_version = installed['numpy']
            pandas_version = installed['pandas']
            
            # Check for known incompatibilities
            if numpy_version.startswith('1.24') and pandas_version.startswith('2.0'):
                self.log_warning("NumPy 1.24.x with pandas 2.0.x may have compatibility issues")
        
        # Matplotlib backend conflicts
        try:
            import matplotlib
            backend = matplotlib.get_backend()
            if backend == 'TkAgg' and not self.check_package_import('tkinter'):
                conflict = {
                    'type': 'backend_conflict',
                    'packages': ['matplotlib'],
                    'message': 'Matplotlib is using TkAgg backend but tkinter is not available'
                }
                conflicts.append(conflict)
                self.log_warning(conflict['message'])
        except ImportError:
            pass
        
        return conflicts
    
    def check_optional_dependencies(self) -> Dict[str, bool]:
        """Check optional dependencies"""
        print("\n🔧 Checking optional dependencies...")
        
        optional_deps = {
            'tkinter': 'tkinter',
            'PIL': 'PIL',
            'scipy': 'scipy',
            'scikit-learn': 'sklearn',
            'plotly': 'plotly',
            'seaborn': 'seaborn'
        }
        
        results = {}
        for package, import_name in optional_deps.items():
            if self.check_package_import(package, import_name):
                self.log_success(f"{package} is available (optional)")
                results[package] = True
            else:
                self.log_warning(f"{package} is not available (optional)")
                results[package] = False
        
        return results
    
    def check_system_requirements(self) -> Dict[str, bool]:
        """Check system requirements"""
        print("\n💻 Checking system requirements...")
        
        system_checks = {
            'Internet Connection': self.check_internet_connection(),
            'File System Write': self.check_file_system_write(),
            'Memory Available': self.check_memory_available(),
            'Disk Space': self.check_disk_space()
        }
        
        for check, result in system_checks.items():
            if result:
                self.log_success(f"{check} is available")
            else:
                self.log_issue(f"{check} is not available")
        
        return system_checks
    
    def check_internet_connection(self) -> bool:
        """Check internet connection"""
        try:
            import requests
            response = requests.get('https://api.pionex.com', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def check_file_system_write(self) -> bool:
        """Check if we can write to file system"""
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=True) as f:
                f.write('test')
            return True
        except:
            return False
    
    def check_memory_available(self) -> bool:
        """Check if sufficient memory is available"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            # Check if at least 100MB is available
            return memory.available > 100 * 1024 * 1024
        except:
            return True  # Assume OK if we can't check
    
    def check_disk_space(self) -> bool:
        """Check if sufficient disk space is available"""
        try:
            import psutil
            disk = psutil.disk_usage('.')
            # Check if at least 100MB is available
            return disk.free > 100 * 1024 * 1024
        except:
            return True  # Assume OK if we can't check
    
    def generate_report(self) -> Dict:
        """Generate comprehensive report"""
        print("\n📊 Generating dependency report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'checks': {
                'python_version': self.check_python_version(),
                'core_dependencies': self.check_core_dependencies(),
                'version_compatibility': self.check_version_compatibility(),
                'conflicts': self.check_conflicts(),
                'optional_dependencies': self.check_optional_dependencies(),
                'system_requirements': self.check_system_requirements()
            },
            'summary': {
                'total_issues': len(self.issues),
                'total_warnings': len(self.warnings),
                'total_success': len(self.success)
            },
            'issues': self.issues,
            'warnings': self.warnings,
            'success': self.success
        }
        
        return report
    
    def print_summary(self, report: Dict):
        """Print summary of the report"""
        print("\n" + "="*60)
        print("📋 DEPENDENCY COMPATIBILITY SUMMARY")
        print("="*60)
        
        summary = report['summary']
        print(f"✅ Success: {summary['total_success']}")
        print(f"⚠️  Warnings: {summary['total_warnings']}")
        print(f"❌ Issues: {summary['total_issues']}")
        
        if summary['total_issues'] == 0:
            print("\n🎉 All dependencies are compatible!")
        elif summary['total_issues'] <= 2:
            print("\n⚠️  Minor issues detected. Check warnings above.")
        else:
            print("\n❌ Multiple issues detected. Please fix before running.")
        
        print("="*60)
    
    def save_report(self, report: Dict, filename: str = None):
        """Save report to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dependency_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n💾 Report saved to: {filename}")
            return filename
        except Exception as e:
            print(f"\n❌ Failed to save report: {e}")
            return None

def main():
    """Main function to run dependency checks"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check dependency compatibility")
    parser.add_argument("--save", action="store_true", help="Save report to JSON file")
    parser.add_argument("--output", help="Output filename for report")
    
    args = parser.parse_args()
    
    print("🔍 Pionex Trading Bot - Dependency Compatibility Checker")
    print("="*60)
    
    checker = DependencyChecker()
    
    try:
        # Run all checks
        report = checker.generate_report()
        
        # Print summary
        checker.print_summary(report)
        
        # Save report if requested
        if args.save:
            filename = args.output or None
            checker.save_report(report, filename)
        
        # Exit with appropriate code
        if report['summary']['total_issues'] == 0:
            sys.exit(0)  # Success
        elif report['summary']['total_issues'] <= 2:
            sys.exit(1)  # Warning
        else:
            sys.exit(2)  # Error
            
    except KeyboardInterrupt:
        print("\n⚠️  Dependency check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Dependency check failed: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main() 