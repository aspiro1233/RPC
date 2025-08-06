"""
Clean Air AI Chatbot - Smart Launcher
Checks dependencies and provides setup guidance
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'groq',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package_name in required_packages:
        try:
            __import__(package_name)
            print(f"✅ {package_name} installed")
        except ImportError:
            missing_packages.append(package_name)
            print(f"❌ {package_name} not found")
    
    return missing_packages

def check_environment():
    """Check environment configuration"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_example.exists():
        print("❌ .env.example file not found")
        return False
    
    if not env_file.exists():
        print("⚠️ .env file not found")
        print("📝 Please copy .env.example to .env and add your Groq API key")
        return False
    
    # Check if API key is set
    try:
        with open(env_file, 'r') as f:
            content = f.read()
            if 'your_groq_api_key_here' in content:
                print("⚠️ Default API key detected in .env")
                print("🔑 Please update GROQ_API_KEY with your actual key")
                return False
            elif 'GROQ_API_KEY=' in content:
                print("✅ .env file configured")
                # Test API connection
                api_works, message = check_groq_api()
                if api_works:
                    print(f"✅ {message}")
                    return True
                else:
                    print(f"❌ {message}")
                    return False
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    return False

def check_groq_api():
    """Check if Groq API key works and test model access"""
    try:
        from groq import Groq
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            return False, "API key not set or still using default value"
        
        # Test API connection
        client = Groq(api_key=api_key)
        
        # Test with a simple query
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello"}],
            model="llama-3.1-70b-versatile",
            max_tokens=10
        )
        
        return True, "API connection successful"
        
    except Exception as e:
        if "model_not_found" in str(e):
            return False, f"Model not found. Try these available models: llama-3.1-70b-versatile, mixtral-8x7b-32768, gemma-7b-it"
        return False, f"API test failed: {str(e)}"

def check_data_files():
    """Check if data files exist"""
    data_dir = Path('data')
    required_files = ['aqi.csv', 'idsp.csv', 'population_projection.csv', 'vahan.csv']
    
    if not data_dir.exists():
        print("❌ Data directory not found")
        return False
    
    missing_files = []
    for file in required_files:
        file_path = data_dir / file
        if file_path.exists():
            print(f"✅ {file} found")
        else:
            missing_files.append(file)
            print(f"⚠️ {file} not found (will use sample data)")
    
    return len(missing_files) == 0

def install_dependencies():
    """Install missing dependencies"""
    print("\n🔧 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from example"""
    try:
        with open('.env.example', 'r') as f:
            content = f.read()
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from example")
        print("🔑 Please edit .env and add your Groq API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def launch_app():
    """Launch the Streamlit application"""
    print("\n🚀 Launching Clean Air AI Chatbot...")
    print("📱 The app will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("⌨️ Press Ctrl+C to stop the application")
    print("\n" + "="*50)
    
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")

def main():
    """Main launcher function"""
    print("🌬️ Clean Air AI Chatbot - Smart Launcher")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        print("\n🔗 Download Python: https://python.org/downloads/")
        return
    
    print("\n📦 Checking dependencies...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        response = input(f"\n❓ Install {len(missing_packages)} missing packages? (y/n): ")
        if response.lower() in ['y', 'yes']:
            if not install_dependencies():
                return
        else:
            print("❌ Cannot proceed without required packages")
            return
    
    print("\n🔧 Checking environment...")
    env_configured = check_environment()
    
    if not env_configured:
        env_exists = Path('.env').exists()
        if not env_exists:
            response = input("\n❓ Create .env file from example? (y/n): ")
            if response.lower() in ['y', 'yes']:
                create_env_file()
        
        print("\n⚠️ Environment setup required:")
        print("1. Get API key from: https://console.groq.com/")
        print("2. Edit .env file and replace 'your_groq_api_key_here' with your actual key")
        print("3. Run this script again")
        return
    
    print("\n📊 Checking data files...")
    check_data_files()
    
    print("\n✅ All checks passed!")
    response = input("\n❓ Launch the application now? (y/n): ")
    if response.lower() in ['y', 'yes']:
        launch_app()
    else:
        print("\n🎯 To launch manually, run: streamlit run app.py")
        print("📖 See QUICKSTART.md for more information")

if __name__ == "__main__":
    main()
