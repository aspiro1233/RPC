#!/usr/bin/env python3
"""
Clean Air AI Chatbot - Deployment Helper
Automates the deployment process to Streamlit Cloud
"""

import os
import subprocess
import sys
from pathlib import Path

def check_git_status():
    """Check if git is initialized and files are committed"""
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git repository not initialized")
            return False
        
        # Check if there are uncommitted changes
        result = subprocess.run(['git', 'diff', '--name-only'], capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️ There are uncommitted changes:")
            print(result.stdout)
            return False
        
        print("✅ Git repository is clean")
        return True
    except FileNotFoundError:
        print("❌ Git is not installed")
        return False

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        '.streamlit/config.toml',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def check_data_files():
    """Check if data files exist"""
    data_dir = Path('data')
    if not data_dir.exists():
        print("⚠️ Data directory not found - app will use sample data")
        return True
    
    data_files = list(data_dir.glob('*.csv'))
    if not data_files:
        print("⚠️ No CSV files found in data directory - app will use sample data")
    else:
        print(f"✅ Found {len(data_files)} data files")
    
    return True

def create_env_example():
    """Create .env.example file if it doesn't exist"""
    env_example = Path('.env.example')
    if not env_example.exists():
        content = """# Clean Air AI Chatbot Environment Variables
# Copy this file to .env and replace with your actual values

# Groq API Configuration
# Get your API key from: https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Optional: Model Configuration
# Available models: llama-3.1-70b-versatile, mixtral-8x7b-32768, gemma-7b-it
GROQ_MODEL=llama-3.1-70b-versatile

# Optional: Application Settings
DEBUG=False
LOG_LEVEL=INFO
"""
        with open(env_example, 'w') as f:
            f.write(content)
        print("✅ Created .env.example file")

def check_remote_repo():
    """Check if remote repository is configured"""
    try:
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if 'origin' in result.stdout:
            print("✅ Remote repository configured")
            return True
        else:
            print("⚠️ No remote repository configured")
            return False
    except Exception as e:
        print(f"❌ Error checking remote repository: {e}")
        return False

def push_to_github():
    """Push changes to GitHub"""
    try:
        print("📤 Pushing to GitHub...")
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Update for Streamlit deployment'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ Successfully pushed to GitHub")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing to GitHub: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Clean Air AI Chatbot - Deployment Helper")
    print("=" * 50)
    
    # Check prerequisites
    if not check_required_files():
        print("\n❌ Please fix missing files before deployment")
        return
    
    if not check_data_files():
        print("\n❌ Data files check failed")
        return
    
    create_env_example()
    
    # Check git status
    if not check_git_status():
        response = input("\n❓ Initialize git and commit changes? (y/n): ")
        if response.lower() in ['y', 'yes']:
            try:
                subprocess.run(['git', 'init'], check=True)
                subprocess.run(['git', 'add', '.'], check=True)
                subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
                print("✅ Git initialized and changes committed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error initializing git: {e}")
                return
        else:
            print("❌ Cannot proceed without git setup")
            return
    
    # Check remote repository
    if not check_remote_repo():
        print("\n📝 To deploy to Streamlit Cloud, you need to:")
        print("1. Create a repository on GitHub")
        print("2. Add it as remote: git remote add origin <your-repo-url>")
        print("3. Push your code: git push -u origin main")
        return
    
    # Push to GitHub
    if not push_to_github():
        print("\n❌ Failed to push to GitHub")
        return
    
    print("\n🎉 Deployment preparation complete!")
    print("\n📋 Next steps:")
    print("1. Go to https://share.streamlit.io/")
    print("2. Sign in with GitHub")
    print("3. Click 'New app'")
    print("4. Select your repository")
    print("5. Set main file path to: app.py")
    print("6. Add your GROQ_API_KEY in the secrets section")
    print("7. Click 'Deploy!'")
    
    print("\n🔑 Required secrets for Streamlit Cloud:")
    print("GROQ_API_KEY = your_actual_groq_api_key_here")
    print("GROQ_MODEL = llama-3.1-70b-versatile")
    
    print("\n📖 For detailed instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main() 