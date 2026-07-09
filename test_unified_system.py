"""
Quick Test Script for Unified System
Run this to verify everything is working correctly
"""

import os
import sys
from pathlib import Path

print("=" * 70)
print("SDG ETHIOPIA CHATBOT - UNIFIED SYSTEM TEST")
print("=" * 70)

# Test 1: Check Python version
print("\n1️⃣ Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 8:
    print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
else:
    print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
    sys.exit(1)

# Test 2: Check required files exist
print("\n2️⃣ Checking required files...")
required_files = [
    'unified_data_fetcher.py',
    'app.py',
    'telegram_bot.py',
    'requirements.txt',
    '.env'
]

all_files_exist = True
for file in required_files:
    if Path(file).exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} (MISSING)")
        all_files_exist = False

if not all_files_exist:
    print("\n   ⚠️  Some required files are missing!")
    sys.exit(1)

# Test 3: Check .env configuration
print("\n3️⃣ Checking .env configuration...")
from dotenv import load_dotenv
load_dotenv()

google_key = os.getenv('GOOGLE_API_KEY')
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')

if google_key and len(google_key) > 10:
    print(f"   ✅ GOOGLE_API_KEY (configured)")
else:
    print(f"   ❌ GOOGLE_API_KEY (missing or invalid)")
    print("      Add to .env: GOOGLE_API_KEY=your_key_here")

if telegram_token and len(telegram_token) > 10:
    print(f"   ✅ TELEGRAM_BOT_TOKEN (configured)")
else:
    print(f"   ⚠️  TELEGRAM_BOT_TOKEN (not configured - optional for Telegram bot)")

# Test 4: Check dependencies
print("\n4️⃣ Checking dependencies...")
required_packages = {
    'streamlit': 'streamlit',
    'chromadb': 'chromadb',
    'sentence_transformers': 'sentence-transformers',
    'google.genai': 'google-generativeai',
    'requests': 'requests',
    'bs4': 'beautifulsoup4',
    'PyPDF2': 'PyPDF2',
    'telegram': 'python-telegram-bot'
}

missing_packages = []
for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
        print(f"   ✅ {package_name}")
    except ImportError:
        print(f"   ❌ {package_name} (not installed)")
        missing_packages.append(package_name)

if missing_packages:
    print(f"\n   ⚠️  Install missing packages:")
    print(f"      pip install {' '.join(missing_packages)}")
    sys.exit(1)

# Test 5: Check ChromaDB
print("\n5️⃣ Checking ChromaDB...")
try:
    import chromadb
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="ethiopia_sdg")
    doc_count = collection.count()
    print(f"   ✅ ChromaDB connected ({doc_count:,} documents)")
except Exception as e:
    print(f"   ❌ ChromaDB error: {e}")
    print("      Run: python scripts/step7_build_vector_db.py")
    sys.exit(1)

# Test 6: Test unified data fetcher
print("\n6️⃣ Testing unified data fetcher...")
try:
    from unified_data_fetcher import UnifiedDataFetcher
    fetcher = UnifiedDataFetcher()
    print(f"   ✅ UnifiedDataFetcher initialized")
    
    # Quick test - World Bank
    print("   🌐 Testing World Bank API...")
    wb_data = fetcher.fetch_worldbank_indicator('SI.POV.DDAY')
    if wb_data:
        print(f"   ✅ World Bank API working: {wb_data['indicator'][:50]}...")
    else:
        print(f"   ⚠️  World Bank API: No data (may be temporary)")
    
    # Quick test - ESS (don't fail if website is down)
    print("   🌐 Testing ESS website...")
    try:
        ess_data = fetcher.search_ess_by_keyword('poverty')
        if ess_data:
            print(f"   ✅ ESS website working: {len(ess_data)} results")
        else:
            print(f"   ⚠️  ESS website: No data (may be temporary)")
    except:
        print(f"   ⚠️  ESS website: Connection issue (temporary)")
    
except Exception as e:
    print(f"   ❌ Fetcher test failed: {e}")
    sys.exit(1)

# Test 7: Test Gemini API
print("\n7️⃣ Testing Google Gemini API...")
if google_key:
    try:
        from google import genai
        client = genai.Client(api_key=google_key)
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents='Say "API test successful" in 3 words'
        )
        print(f"   ✅ Gemini API working: {response.text[:50]}")
    except Exception as e:
        print(f"   ⚠️  Gemini API test issue: {e}")
        print("      Note: This is just a test. The app may still work!")
        print("      Try running: python -m streamlit run app.py")
else:
    print(f"   ⚠️  Skipping Gemini test (no API key)")

# Test 8: Check cache directory
print("\n8️⃣ Checking cache directory...")
cache_dir = Path('./cache')
if cache_dir.exists():
    cache_files = list(cache_dir.glob('*.json'))
    print(f"   ✅ Cache directory exists ({len(cache_files)} cached items)")
else:
    print(f"   ℹ️  Cache directory will be created on first run")

# Final summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if google_key and doc_count > 0:
    print("\n✅ System is ready!")
    print("\n📝 Next steps:")
    print("   1. Run web app:       streamlit run app.py")
    print("   2. Run Telegram bot:  python telegram_bot.py")
    print("\n💡 Try asking:")
    print("   - What is Ethiopia's poverty rate?")
    print("   - Show me education statistics")
    print("   - Latest health indicators")
else:
    print("\n⚠️  System needs configuration:")
    if not google_key:
        print("   - Add GOOGLE_API_KEY to .env")
    if doc_count == 0:
        print("   - Run: python scripts/step7_build_vector_db.py")

print("\n" + "=" * 70)
print("For detailed guide, see: UNIFIED_SYSTEM_GUIDE.md")
print("=" * 70)
