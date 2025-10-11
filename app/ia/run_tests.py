"""
Test runner script for #Dô Backend
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🧪 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Run all tests"""
    print("🎵 #Dô Backend - Test Runner")
    print("=" * 40)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Install dependencies if needed
    print("📦 Checking dependencies...")
    try:
        import fastapi
        import pytest
        import tensorflow
        print("✅ Dependencies already installed")
    except ImportError:
        print("📦 Installing dependencies...")
        if not run_command("pip install -r requirements.txt", "Installing dependencies"):
            return False
    
    # Run unit tests
    print("\n🔬 Running Unit Tests...")
    test_commands = [
        ("pytest backend/tests/test_auth_service.py -v", "Auth Service Tests"),
        ("pytest backend/tests/test_ml_service.py -v", "ML Service Tests"),
        ("pytest backend/tests/test_integration.py -v", "Integration Tests")
    ]
    
    all_passed = True
    for command, description in test_commands:
        if not run_command(command, description):
            all_passed = False
    
    # Run coverage if available
    print("\n📊 Running Coverage Analysis...")
    if run_command("pytest --cov=backend backend/tests/ --cov-report=html", "Coverage Analysis"):
        print("📈 Coverage report generated in htmlcov/index.html")
    
    # Summary
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed successfully!")
        print("\n📋 Test Summary:")
        print("  ✅ Auth Service Tests")
        print("  ✅ ML Service Tests") 
        print("  ✅ Integration Tests")
        print("  ✅ Coverage Analysis")
    else:
        print("❌ Some tests failed. Please check the output above.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
