"""
ProofLens AI - Setup and Testing Script
Quick installation and verification of all components
"""

import sys
import subprocess
import os


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print("✅ Python version compatible")
    return True


def install_dependencies():
    """Install required dependencies"""
    print_header("Installing Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def test_imports():
    """Test if all critical modules can be imported"""
    print_header("Testing Module Imports")
    
    modules = {
        'flask': 'Flask',
        'requests': 'Requests',
        'reportlab': 'ReportLab (PDF generation)',
        'pandas': 'Pandas (CSV export)',
        'razorpay': 'Razorpay (Payment processing)',
        'authlib': 'Authlib (OAuth)',
        'ollama': 'Ollama (AI)',
    }
    
    all_success = True
    
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Not installed")
            all_success = False
    
    return all_success


def test_custom_modules():
    """Test custom ProofLens AI modules"""
    print_header("Testing ProofLens AI Modules")
    
    modules = [
        ('deepfake_detector', 'Deepfake Detection Module'),
        ('url_checker', 'URL Reputation Checker'),
        ('export_reports', 'Export Reports Module'),
        ('config', 'Configuration'),
        ('models', 'Database Models'),
    ]
    
    all_success = True
    
    for module, name in modules:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name} - Error: {e}")
            all_success = False
    
    return all_success


def test_api_configs():
    """Test if API configurations are set"""
    print_header("Checking API Configurations")
    
    from config import Config
    
    configs = {
        'ARYA_VIDEO_API_TOKEN': 'Arya.ai Video API',
        'ARYA_IMAGE_API_TOKEN': 'Arya.ai Image API',
        'ARYA_AUDIO_API_TOKEN': 'Arya.ai Audio API',
        'VIRUSTOTAL_API_KEY': 'VirusTotal API',
        'GOOGLE_OAUTH_CLIENT_ID': 'Google OAuth Client ID',
        'GOOGLE_OAUTH_CLIENT_SECRET': 'Google OAuth Secret',
    }
    
    all_configured = True
    
    for key, name in configs.items():
        value = getattr(Config, key, None)
        if value and value != f'your-{key.lower().replace("_", "-")}':
            print(f"✅ {name}")
        else:
            print(f"⚠️  {name} - Not configured (optional for testing)")
    
    return True


def test_deepfake_detector():
    """Test deepfake detector module"""
    print_header("Testing Deepfake Detection")
    
    try:
        from deepfake_detector import VideoDeepfakeDetector, AudioDeepfakeDetector, ImageDeepfakeDetector
        print("✅ Deepfake detector classes loaded")
        print("   - VideoDeepfakeDetector")
        print("   - AudioDeepfakeDetector")
        print("   - ImageDeepfakeDetector")
        return True
    except Exception as e:
        print(f"❌ Error loading deepfake detector: {e}")
        return False


def test_url_checker():
    """Test URL checker module"""
    print_header("Testing URL Reputation Checker")
    
    try:
        from url_checker import URLReputationChecker, expand_shortened_url
        print("✅ URL checker loaded")
        print("   - URLReputationChecker class")
        print("   - expand_shortened_url function")
        return True
    except Exception as e:
        print(f"❌ Error loading URL checker: {e}")
        return False


def test_export_module():
    """Test export module"""
    print_header("Testing Export Module")
    
    try:
        from export_reports import ReportExporter, export_verification_report
        
        # Test PDF generation
        test_data = {
            'id': 1,
            'type': 'Text Verification',
            'authenticity_score': 85,
            'key_findings': ['Test finding 1', 'Test finding 2'],
            'score_breakdown': {
                'factual_accuracy': 35,
                'source_consistency': 25,
                'detail_accuracy': 15,
                'context_accuracy': 10
            }
        }
        
        exporter = ReportExporter()
        pdf_bytes = exporter.export_to_pdf(test_data)
        json_str = exporter.export_to_json(test_data)
        csv_bytes = exporter.export_to_csv(test_data)
        
        print("✅ Export module working")
        print(f"   - PDF: {len(pdf_bytes)} bytes")
        print(f"   - JSON: {len(json_str)} bytes")
        print(f"   - CSV: {len(csv_bytes)} bytes")
        return True
    except Exception as e:
        print(f"❌ Error testing export module: {e}")
        return False


def check_database():
    """Check if database exists"""
    print_header("Checking Database")
    
    db_files = ['prooflens.db', 'newsguard.db', 'instance/prooflens.db', 'instance/newsguard.db']
    
    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"✅ Database found: {db_file}")
            return True
    
    print("⚠️  No database found. Run 'flask db upgrade' to create it.")
    return False


def main():
    """Run all tests"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          ProofLens AI - Setup & Testing Script          ║")
    print("║              Truth Through Technology                     ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    results = []
    
    # Run all tests
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", install_dependencies()))
    results.append(("Module Imports", test_imports()))
    results.append(("Custom Modules", test_custom_modules()))
    results.append(("API Configurations", test_api_configs()))
    results.append(("Deepfake Detector", test_deepfake_detector()))
    results.append(("URL Checker", test_url_checker()))
    results.append(("Export Module", test_export_module()))
    results.append(("Database", check_database()))
    
    # Print summary
    print_header("Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! ProofLens AI is ready to use.")
        print("\nNext steps:")
        print("1. Run database migrations: flask db init && flask db migrate && flask db upgrade")
        print("2. Start the application: python app.py")
        print("3. Open browser: http://localhost:5000")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("\n")


if __name__ == "__main__":
    main()
