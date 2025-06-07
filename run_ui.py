#!/usr/bin/env python3
"""
Launcher script for Browser Use UI
"""

import os
import subprocess
import sys
from pathlib import Path

def check_environment():
    """Check if we're in the correct environment."""
    if not os.path.exists("browser_use_env"):
        print("❌ Error: browser_use_env not found!")
        print("Please run this from the Bowsruse directory.")
        return False
    
    if not os.path.exists("browser_use_ui.py"):
        print("❌ Error: browser_use_ui.py not found!")
        return False
    
    if not os.path.exists("flexible_browser_use.py"):
        print("❌ Error: flexible_browser_use.py not found!")
        return False
    
    return True

def main():
    """Main launcher."""
    print("🚀 Starting Browser Use UI...")
    
    if not check_environment():
        sys.exit(1)
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("⚠️  Warning: .env file not found!")
        print("You can configure API keys through the web interface.")
    
    # Start Streamlit
    try:
        print("🌐 Opening web interface at http://localhost:8501")
        print("📱 Use Ctrl+C to stop the server")
        print("-" * 50)
        
        # Activate virtual environment and run streamlit
        cmd = [
            "bash", "-c", 
            "source browser_use_env/bin/activate && streamlit run browser_use_ui.py --server.port 8501 --server.address localhost"
        ]
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Browser Use UI stopped.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting UI: {e}")
        print("Make sure Streamlit is installed: pip install streamlit")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 