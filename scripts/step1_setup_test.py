"""
DAY 1 TASK: Test Python Environment and Basic Setup
Run this script to verify your installation is correct.

Execute: python scripts/step1_setup_test.py
"""

import sys
print("=" * 60)
print("SDG ETHIOPIA CHATBOT - ENVIRONMENT TEST")
print("=" * 60)

# Test 1: Python Version
print(f"\n✓ Python Version: {sys.version}")
if sys.version_info >= (3, 9):
    print("  [PASS] Python version is compatible")
else:
    print("  [FAIL] Please upgrade to Python 3.9+")

# Test 2: Core Libraries
print("\n--- Testing Core Libraries ---")
required_libs = [
    'pandas',
    'numpy',
    'requests',
]

for lib in required_libs:
    try:
        __import__(lib)
        print(f"✓ {lib} installed")
    except ImportError:
        print(f"✗ {lib} NOT installed - run: pip install {lib}")

# Test 3: File Structure
print("\n--- Testing Project Structure ---")
import os
required_dirs = [
    'data/raw',
    'data/processed',
    'docs',
    'scripts',
]

for dir_path in required_dirs:
    if os.path.exists(dir_path):
        print(f"✓ {dir_path} exists")
    else:
        print(f"✗ {dir_path} missing")

print("\n" + "=" * 60)
print("SETUP TEST COMPLETE")
print("=" * 60)
print("\nNext Steps:")
print("1. If any tests failed, install missing packages: pip install -r requirements.txt")
print("2. Get your FREE Gemini API key: https://aistudio.google.com/app/apikey")
print("3. Copy .env.example to .env and add your API key")
print("4. Run: python scripts/step2_test_gemini.py")
