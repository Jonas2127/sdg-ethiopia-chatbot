"""
DAY 1 TASK: Test Google Gemini API Connection
This script verifies your API key works correctly.

Prerequisites:
1. Get free API key from: https://aistudio.google.com/app/apikey
2. Create .env file with: GOOGLE_API_KEY=your_key_here
3. Install: pip install google-generativeai python-dotenv

Execute: python scripts/step2_test_gemini.py
"""

import os
from dotenv import load_dotenv

print("=" * 60)
print("TESTING GOOGLE GEMINI API CONNECTION")
print("=" * 60)

# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("\n✗ ERROR: GOOGLE_API_KEY not found in .env file")
    print("\nSteps to fix:")
    print("1. Visit: https://aistudio.google.com/app/apikey")
    print("2. Click 'Create API Key'")
    print("3. Copy the key")
    print("4. Create a .env file in the project root")
    print("5. Add this line: GOOGLE_API_KEY=your_key_here")
    exit(1)

print(f"\n✓ API Key found: {api_key[:10]}...{api_key[-5:]}")

# Test API connection
try:
    from google import genai
    
    client = genai.Client(api_key=api_key)
    
    print("\n--- Listing available models ---")
    try:
        models = client.models.list()
        available_models = [m.name for m in models]
        print(f"Found {len(available_models)} models")
        
        # Print first 10 models to see the naming format
        print("\nFirst 10 available models:")
        for m in available_models[:10]:
            print(f"  - {m}")
        
    except Exception as e:
        print(f"Could not list models: {e}")
    
    # Try multiple working models in order of preference (with models/ prefix)
    models_to_try = [
        'models/gemini-2.0-flash-lite',
        'models/gemini-2.0-flash',
        'models/gemini-2.0-flash-001',
        'models/gemini-1.5-flash-latest',
        'models/gemini-1.5-flash',
        'models/gemini-1.5-pro-latest',
        'models/gemini-1.5-pro',
        'models/gemini-1.5-flash-001',
        'models/gemini-1.0-pro'
    ]
    
    print("\n--- Testing models to find a working one ---")
    model_to_use = None
    last_error = None
    for test_model in models_to_try:
        try:
            print(f"Trying: {test_model}...", end=" ")
            response = client.models.generate_content(
                model=test_model,
                contents="Hi"
            )
            model_to_use = test_model
            print("✓ Works!")
            break
        except Exception as e:
            last_error = str(e)
            print(f"✗ Failed ({str(e)[:50]}...)")
            continue
    
    if not model_to_use:
        print(f"\n✗ No working models found")
        print(f"\nLast error details: {last_error}")
        exit(1)
    
    print("\n--- Sending test prompt to Gemini ---")
    response = client.models.generate_content(
        model=model_to_use,
        contents="Explain what Sustainable Development Goals are in one sentence."
    )
    
    print(f"\n✓ API CONNECTION SUCCESSFUL!")
    print(f"\nGemini's Response:")
    print(f"  {response.text}")
    
    print("\n" + "=" * 60)
    print("GEMINI API TEST PASSED")
    print("=" * 60)
    print("\nYou're ready to proceed to data collection!")
    
except ImportError as e:
    print(f"\n✗ Import error: {e}")
    print("Run: pip install google-genai python-dotenv")
except Exception as e:
    print(f"\n✗ API Error: {e}")
    print("\nPossible issues:")
    print("- Invalid API key (make sure it's correct in .env)")
    print("- Network connection problem")
    print("- API quota exceeded (unlikely with free tier)")
