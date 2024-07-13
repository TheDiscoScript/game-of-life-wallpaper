# test_imports.py
try:
    from PIL import Image
    from AppKit import NSWorkspace, NSScreen
    print("Imports successful!")
except ImportError as e:
    print(f"Import error: {e}")