import os
import sys
import webbrowser
from threading import Timer
import uvicorn

def verify_and_setup():
    print("=== Rental Pro Application Setup ===")
    
    # 1. Check Python dependencies
    try:
        import docx
        import win32com.client
        import fastapi
        import uvicorn
        print("[OK] Python dependencies verified successfully.")
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e.name}")
        print("Please run: pip install fastapi uvicorn python-docx pywin32")
        sys.exit(1)

    # 2. Run Template Creation
    try:
        from create_template import create_template
        create_template()
    except Exception as e:
        print(f"[ERROR] Failed to create TEMPLATE.docx: {e}")
        sys.exit(1)

def open_browser():
    url = "http://127.0.0.1:8000"
    print(f"\n[OK] Launching browser: {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    verify_and_setup()
    
    # Schedule browser opening after 1.5 seconds (giving uvicorn time to start)
    Timer(1.5, open_browser).start()
    
    print("\n[OK] Starting FastAPI server on port 8000...")
    print("Press Ctrl+C to terminate.")
    
    # Run FastAPI server
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info", reload=False)
