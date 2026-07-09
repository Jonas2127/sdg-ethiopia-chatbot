"""
SDG Ethiopia Chatbot - Unified Live System
Fetches real-time data from UN, World Bank, and ESS

Run with: streamlit run app.py
"""

import streamlit as st
import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
from unified_data_fetcher import UnifiedDataFetcher

# Page configuration
st.set_page_config(
    page_title="SDG Ethiopia Chatbot",
    page_icon="🇪🇹",
    layout="wide"
)

# Apply ESS-inspired color scheme and Times New Roman font
st.markdown("""
    <style>
    /* Global font */
    * {
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    /* Main title styling - bright green for Ethiopia */
    h1 {
        color: #00B140 !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subtitle styling */
    h3 {
        color: #4267B2 !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar styling - ESS dark theme */
    [data-testid="stSidebar"] {
        background-color: #2c2c2c !important;
    }
    
    [data-testid="stSidebar"] .element-container {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p {
        color: #ffffff !important;
    }
    
    /* Sidebar title with ESS blue accent */
    [data-testid="stSidebar"] h1 {
        color: #6BA3D8 !important;
        border-bottom: 3px solid #4267B2;
        padding-bottom: 10px;
    }
    
    /* Main content background */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Answer section styling */
    .element-container h3 {
        color: #4267B2 !important;
        border-left: 4px solid #4267B2;
        padding-left: 10px;
    }
    
    /* Metric styling - ESS inspired */
    [data-testid="stMetric"] {
        background-color: #2c2c2c;
        padding: 15px;
        border-radius: 8px;
        color: white;
    }
    
    [data-testid="stMetric"] label {
        color: #ffffff !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #6BA3D8 !important;
        font-size: 28px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# INITIALIZE COMPONENTS
# ============================================

@st.cache_resource
def load_models():
    """Load models and initialize fetcher once"""
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        st.error("❌ GOOGLE_API_KEY not found in .env file")
        st.stop()
    
    # Load embedding model
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Try to load ChromaDB (optional - works without it)
    collection = None
    try:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        collection = chroma_client.get_collection(name="ethiopia_sdg")
        st.success("✅ Local database loaded (11,346 documents)")
    except Exception as e:
        st.warning("⚠️ Local database not available. Using live data only from World Bank, ESS, and UN.")
        collection = None
    
    # Initialize Gemini - find available model
    from google import genai
    gemini_client = genai.Client(api_key=api_key)
    
    # Try to find an available model
    available_model = None
    try:
        models = gemini_client.models.list()
        model_names = [m.name for m in models]
        # Look for flash or pro models
        for name in model_names:
            if 'flash' in name.lower() or 'pro' in name.lower():
                available_model = name
                break
        if not available_model and model_names:
            available_model = model_names[0]
    except:
        # Fallback to try common names
        available_model = 'models/gemini-1.5-flash'
    
    # Initialize unified fetcher
    fetcher = UnifiedDataFetcher()
    
    return embedding_model, collection, gemini_client, fetcher, available_model

embedding_model, collection, gemini_client, fetcher, available_model = load_models()

# ============================================
# CHATBOT FUNCTION - UNIFIED LIVE DATA
# ============================================

def ask_chatbot(question, fetch_live=True):
    """
    Unified chatbot with live data from all three sources
    
    Args:
        question: User's question
        fetch_live: Whether to fetch live data (default: True)
    """
    
    # Step 1: Search local database (if available)
    stored_context = []
    if collection is not None:
        with st.spinner("🔍 Searching stored database..."):
            query_embedding = embedding_model.encode([question])
            results = collection.query(
                query_embeddings=query_embedding.tolist(),
                n_results=12  # Balance between stored and live data
            )
            
            for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                stored_context.append(f"[STORED DATA] Source {i+1}:\n{doc}\n")
    else:
        st.info("ℹ️ Using live data sources only (World Bank + ESS + UN)")
    
    # Step 2: Fetch live data from all sources
    live_context = []
    live_summary = {}
    
    if fetch_live:
        with st.spinner("🌐 Fetching LIVE data from UN, World Bank, and ESS..."):
            try:
                all_data = fetcher.fetch_all_sources(question)
                
                # Process World Bank data
                if all_data['world_bank']:
                    for data in all_data['world_bank']:
                        live_text = f"""[WORLD BANK LIVE DATA - {data['fetched_at']}]
Indicator: {data['indicator']}
Year: {data['year']}
Value: {data['value']}
Country: {data['country']}
Source: {data['source']}
"""
                        live_context.append(live_text)
                    
                    live_summary['world_bank'] = len(all_data['world_bank'])
                
                # Process ESS data
                if all_data['ess']:
                    for data in all_data['ess']:
                        live_text = f"""[ESS LIVE DATA - {data['fetched_at']}]
Title: {data.get('title', 'N/A')}
Content: {data['content']}
Source: {data['source']}
"""
                        live_context.append(live_text)
                    
                    live_summary['ess'] = len(all_data['ess'])
                
                # Process UN status
                if all_data['un']:
                    un_text = f"""[UN SDG DATABASE STATUS]
Last Check: {all_data['un'].get('last_check', 'N/A')}
Message: {all_data['un'].get('message', 'N/A')}
Portal: {all_data['un'].get('portal_url', 'N/A')}
"""
                    live_context.append(un_text)
                    live_summary['un'] = 'checked'
                
                # Display live data summary with individual status
                status_parts = []
                
                if 'world_bank' in live_summary:
                    status_parts.append(f"🌍 World Bank: {live_summary['world_bank']} indicators")
                else:
                    status_parts.append(f"⚠️ World Bank: No data")
                
                if 'ess' in live_summary:
                    status_parts.append(f"🇪🇹 ESS: {live_summary['ess']} results")
                else:
                    status_parts.append(f"⚠️ ESS: No data")
                
                if 'un' in live_summary:
                    status_parts.append(f"🔵 UN: {live_summary['un']}")
                
                if status_parts:
                    st.success(" | ".join(status_parts))
                else:
                    st.info("ℹ️ No live data found. Using stored database only.")
                
            except Exception as e:
                st.warning(f"⚠️ Live data fetch error: {str(e)}. Using stored database.")
    
    # Step 3: Combine all contexts
    combined_context = "\n".join(stored_context + live_context)
    
    # Step 4: Create comprehensive prompt
    prompt = f"""You are an expert assistant on Ethiopia's Sustainable Development Goals (SDGs).

You have access to THREE types of data:
1. [STORED DATA] - Historical data from your local database (11,346 documents)
2. [WORLD BANK LIVE DATA] - Real-time indicators fetched just now from World Bank API
3. [ESS LIVE DATA] - Real-time data from Ethiopian Statistical Service website
4. [UN SDG DATABASE STATUS] - Latest update status from UN SDG portal

Guidelines:
- Prioritize the MOST RECENT data available
- If live data is newer than stored data, mention it's the latest available
- Use specific numbers, years, and trends from the data
- Be concise but comprehensive
- Always cite the data source and year
- If data from multiple sources conflict, mention both and explain the difference
- **CRITICAL - For Future Year Requests (2023-2026+)**:
  * STEP 1: State clearly "Official verified data for [year] is NOT YET AVAILABLE"
  * STEP 2: Provide the MOST RECENT VERIFIED DATA (with exact year and source)
  * STEP 3: YOU MUST provide a PROJECTION/ESTIMATE for the requested year:
    a) Look at the historical trend in the data (e.g., if 2016: 40%, 2018: 38%, 2021: 36%)
    b) Calculate the average annual change rate
    c) Extrapolate to the requested year
    d) Present it as: "📈 ESTIMATED PROJECTION for [year]: approximately X% (based on Y trend)"
    e) Add disclaimer: "⚠️ This is a statistical projection, not official data"
  * STEP 4: Mention where to check for official updates (World Bank, ESS, UN)
  * **IMPORTANT**: You MUST complete all 4 steps. Don't skip the projection!

Context (Ethiopia SDG Data from all sources):
{combined_context}

Question: {question}

Answer (Remember: If asked about 2024-2026, you MUST provide both verified data AND projection):"""
    
    # Step 5: Generate response with Gemini
    with st.spinner("🤖 Generating answer..."):
        for attempt in range(3):
            try:
                response = gemini_client.models.generate_content(
                    model=available_model,
                    contents=prompt
                )
                
                return response.text, len(stored_context), len(live_context)
                
            except Exception as e:
                error_str = str(e)
                if "503" in error_str or "UNAVAILABLE" in error_str:
                    if attempt < 2:
                        import time
                        time.sleep(2)
                        continue
                    else:
                        st.error("🔄 AI service is temporarily busy. Please try again in a moment.")
                        return None, 0, 0
                else:
                    st.error(f"❌ Error: {error_str}")
                    return None, 0, 0
        
        return None, 0, 0

# ============================================
# STREAMLIT UI
# ============================================

# Sidebar
with st.sidebar:
    st.title("📊 SDG Ethiopia Chatbot")
    st.markdown("**Unified Live Data System**")
    st.markdown("---")
    
    # Display ESS logo in sidebar - larger and circular
    ess_logo_path = "./assets/ess_logo_ethiopia.png"
    if os.path.exists(ess_logo_path):
        try:
            from PIL import Image, ImageDraw
            import base64
            from io import BytesIO
            
            # Open ESS logo
            img = Image.open(ess_logo_path)
            
            # Convert to RGBA if needed for transparency
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Make it square by cropping to center (to avoid distortion)
            width, height = img.size
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
            img_square = img.crop((left, top, right, bottom))
            
            # Resize to 220x220 for larger display
            img_square = img_square.resize((220, 220), Image.Resampling.LANCZOS)
            
            # Create circular mask
            mask = Image.new('L', (220, 220), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 220, 220), fill=255)
            
            # Apply circular mask
            output = Image.new('RGBA', (220, 220), (0, 0, 0, 0))
            output.paste(img_square, (0, 0))
            output.putalpha(mask)
            
            # Convert to base64
            buffered = BytesIO()
            output.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Display centered with circular styling
            st.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <img src="data:image/png;base64,{img_b64}" 
                         style="width: 220px; 
                                height: 220px; 
                                border-radius: 50%;
                                object-fit: cover;
                                display: block;
                                margin: 0 auto;
                                box-shadow: 0 6px 12px rgba(0,0,0,0.4);
                                border: 4px solid #00B140;
                                image-rendering: -webkit-optimize-contrast;
                                image-rendering: crisp-edges;">
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            # Fallback if image processing fails
            st.image(ess_logo_path, use_container_width=False, width=220)
    
    
    st.markdown("### 🌐 Data Sources")
    st.markdown("""
    **Live Data:**
    - 🌍 **World Bank API** - Real-time indicators
    - 🇪🇹 **ESS Website** - Latest Ethiopian statistics
    - 🔵 **UN SDG Database** - Quarterly updates
    
    **Stored Data:**
    - 📁 11,346 historical documents (if available)
    - 📊 465 unique indicators
    - 📅 Years: 1995-2026
    """)
    
    st.markdown("---")
    
    # Data fetching toggle
    st.markdown("### ⚙️ Settings")
    fetch_live = st.checkbox("Fetch Live Data", value=True, 
                            help="Enable real-time data fetching from all sources")
    
    # Use session state to track if cache was just cleared
    if 'cache_cleared' not in st.session_state:
        st.session_state.cache_cleared = False
    
    if st.button("🗑️ Clear Cache"):
        fetcher.clear_cache()
        st.session_state.cache_cleared = True
        st.rerun()  # Rerun to show success message
    
    if st.session_state.cache_cleared:
        st.success("✓ Cache cleared! Ask a new question to fetch fresh data.")
        st.session_state.cache_cleared = False
    
    st.markdown("---")
    st.markdown("### 💡 Example Questions")
    st.markdown("""
    - What is Ethiopia's current poverty rate?
    - Show me education enrollment trends
    - Latest child mortality statistics
    - Access to electricity in Ethiopia
    - Forest coverage changes over time
    """)

# Main content - Logo and Title
st.markdown("""
    <style>
    .main .block-container img {
        border-radius: 50% !important;
        object-fit: cover !important;
    }
    .logo-main {
        border-radius: 50% !important;
        width: 200px !important;
        height: 200px !important;
        object-fit: cover !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
        border: 4px solid #4169E1 !important;
    }
    </style>
""", unsafe_allow_html=True)

logo_path = "./assets/sm_1684604849.312469.jpg"
if os.path.exists(logo_path):
    try:
        from PIL import Image
        import base64
        from io import BytesIO
        
        # Open image and convert to square for perfect circle
        img = Image.open(logo_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Make it square by cropping to center
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        img_square = img.crop((left, top, right, bottom))
        
        # Resize to 200x200 for consistent display
        img_square = img_square.resize((200, 200), Image.Resampling.LANCZOS)
        
        # Convert to base64
        buffered = BytesIO()
        img_square.save(buffered, format="JPEG", quality=95)
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        
        col1, col2 = st.columns([1, 3])
        with col1:
            # Use HTML with clip-path for perfect circle
            st.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <img src="data:image/jpeg;base64,{img_b64}" 
                         style="width: 200px; 
                                height: 200px; 
                                border-radius: 50%;
                                clip-path: circle(50%);
                                object-fit: cover;
                                display: block;
                                margin: 0 auto;
                                box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                                border: 4px solid #4169E1;">
                </div>
            """, unsafe_allow_html=True)
        with col2:
            # Load ESS icon for title
            ess_icon_path = "./assets/ess_logo_ethiopia.png"
            if os.path.exists(ess_icon_path):
                ess_icon = Image.open(ess_icon_path)
                
                # Resize icon to 70x70 for better visibility
                ess_icon = ess_icon.resize((70, 70), Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffered_icon = BytesIO()
                ess_icon.save(buffered_icon, format="PNG")
                icon_b64 = base64.b64encode(buffered_icon.getvalue()).decode()
                
                st.markdown(f"""
                    <h1 style="color: #00B140; margin: 0 0 10px 0; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); line-height: 1.2; display: flex; align-items: center; gap: 8px;">
                        <img src="data:image/png;base64,{icon_b64}" 
                             style="width: 60px; 
                                    height: 60px; 
                                    object-fit: contain;
                                    display: inline-block;
                                    vertical-align: middle;">
                        <span>SDG Ethiopia Chatbot</span>
                    </h1>
                    <h3 style="color: #4267B2; font-weight: 600; margin: 0 0 5px 0;">Ask questions about Ethiopia's Sustainable Development Goals</h3>
                    <p style="color: #6BA3D8; font-style: italic; font-size: 18px; margin: 0;">Powered by real-time data from UN, World Bank, and ESS</p>
                """, unsafe_allow_html=True)
            else:
                # Fallback if icon not found
                st.markdown("""
                    <h1 style="color: #00B140; margin-bottom: 0; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">🇪🇹 SDG Ethiopia Chatbot</h1>
                    <h3 style="color: #4267B2; font-weight: 600; margin-top: 5px;">Ask questions about Ethiopia's Sustainable Development Goals</h3>
                    <p style="color: #6BA3D8; font-style: italic; font-size: 18px;">Powered by real-time data from UN, World Bank, and ESS</p>
                """, unsafe_allow_html=True) 
    except ImportError:
        # Fallback if PIL is not available
        st.warning("⚠️ Install Pillow for better logo display: pip install Pillow")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(logo_path, width=200)
        with col2:
            # Try to load ESS icon
            ess_icon_path = "./assets/ess_logo_ethiopia.png"
            if os.path.exists(ess_icon_path):
                try:
                    import base64
                    from PIL import Image
                    from io import BytesIO
                    
                    ess_icon = Image.open(ess_icon_path)
                    ess_icon = ess_icon.resize((70, 70), Image.Resampling.LANCZOS)
                    buffered = BytesIO()
                    ess_icon.save(buffered, format="PNG")
                    icon_b64 = base64.b64encode(buffered.getvalue()).decode()
                    
                    st.markdown(f"""
                        <h1 style="color: #00B140; margin: 0 0 10px 0; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); line-height: 1.2; display: flex; align-items: center; gap: 8px;">
                            <img src="data:image/png;base64,{icon_b64}" 
                                 style="width: 60px; 
                                        height: 60px; 
                                        object-fit: contain;
                                        display: inline-block;
                                        vertical-align: middle;">
                            <span>SDG Ethiopia Chatbot</span>
                        </h1>
                        <h3 style="color: #4267B2; font-weight: 600; margin: 0 0 5px 0;">Ask questions about Ethiopia's Sustainable Development Goals</h3>
                        <p style="color: #6BA3D8; font-style: italic; font-size: 18px; margin: 0;">Powered by real-time data from UN, World Bank, and ESS</p>
                    """, unsafe_allow_html=True)
                except:
                    st.markdown("""
                        <h1 style="color: #00B140; margin-bottom: 0; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">🇪🇹 SDG Ethiopia Chatbot</h1>
                        <h3 style="color: #4267B2; font-weight: 600; margin-top: 5px;">Ask questions about Ethiopia's Sustainable Development Goals</h3>
                        <p style="color: #6BA3D8; font-style: italic; font-size: 18px;">Powered by real-time data from UN, World Bank, and ESS</p>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <h1 style="color: #00B140; margin-bottom: 0; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">🇪🇹 SDG Ethiopia Chatbot</h1>
                    <h3 style="color: #4267B2; font-weight: 600; margin-top: 5px;">Ask questions about Ethiopia's Sustainable Development Goals</h3>
                    <p style="color: #6BA3D8; font-style: italic; font-size: 18px;">Powered by real-time data from UN, World Bank, and ESS</p>
                """, unsafe_allow_html=True)
else:
    st.title("🇪🇹 SDG Ethiopia Chatbot")
    st.markdown("**Ask questions about Ethiopia's Sustainable Development Goals**")
    st.markdown("*Powered by real-time data from UN, World Bank, and ESS*")

# Input area
user_question = st.text_input(
    "Your Question:",
    placeholder="e.g., What is Ethiopia's poverty rate in 2024?",
    key="question_input"
)

# Search button
# Only process question if cache wasn't just cleared
if not st.session_state.get('cache_cleared', False):
    if st.button("🔍 Search", type="primary") or user_question:
        if user_question:
            with st.container():
                # Get answer
                answer, stored_count, live_count = ask_chatbot(user_question, fetch_live=fetch_live)
                
                if answer:
                    # Display answer
                    st.markdown("### 📝 Answer")
                    st.markdown(answer)
                    
                    # Display source statistics
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📁 Stored Sources", stored_count)
                with col2:
                    st.metric("🌐 Live Sources", live_count)
                with col3:
                    st.metric("📊 Total Sources", stored_count + live_count)
                
                # Show expander with raw context
                with st.expander("🔍 View Source Documents"):
                    st.markdown("**Note:** This shows the retrieved context used to generate the answer.")
                    st.text(f"Retrieved {stored_count} stored documents and {live_count} live data sources")
        else:
            st.warning("⚠️ Please enter a question")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>SDG Ethiopia Chatbot v2.0 - Unified Live Data System</p>
    <p>Data sources: UN SDG Database | World Bank Open Data | Ethiopian Statistical Service</p>
</div>
""", unsafe_allow_html=True)
