"""
Start server script for #Dô Backend
"""
import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Please copy env.example to .env and configure it.")
        return False
    
    # Check required environment variables
    required_vars = [
        "SECRET_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease configure your .env file.")
        return False
    
    print("✅ Environment configuration looks good!")
    return True

def install_dependencies():
    """Install dependencies if needed"""
    print("📦 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Dependencies already installed")
        return True
    except ImportError:
        print("📦 Installing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting #Dô Backend Server...")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Check environment
    if not check_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Start server
    print("\n🌐 Server starting at http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🎵 #Dô - Assistente de Prática Musical")
    print("Backend Server")
    print("=" * 50)
    
    success = start_server()
    if not success:
        print("\n❌ Failed to start server")
        sys.exit(1)
    
    print("\n✅ Server stopped successfully")

if __name__ == "__main__":
    main()
