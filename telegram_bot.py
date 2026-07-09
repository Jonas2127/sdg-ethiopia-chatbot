"""
SDG Ethiopia Chatbot - Telegram Bot
Unified live data from UN, World Bank, and ESS

Run with: python telegram_bot.py
"""

import os
import logging
import html
import re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import chromadb
from sentence_transformers import SentenceTransformer
from google import genai
from unified_data_fetcher import UnifiedDataFetcher

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================
# INITIALIZE COMPONENTS
# ============================================

def initialize_components():
    """Initialize all components once at startup"""
    load_dotenv()
    
    # Get API keys
    google_api_key = os.getenv('GOOGLE_API_KEY')
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not google_api_key:
        raise ValueError("❌ GOOGLE_API_KEY not found in .env file")
    
    if not telegram_token:
        raise ValueError("❌ TELEGRAM_BOT_TOKEN not found in .env file")
    
    # Load embedding model
    logger.info("Loading embedding model...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Load ChromaDB
    logger.info("Connecting to ChromaDB...")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="ethiopia_sdg")
    
    # Initialize Gemini - find available model
    logger.info("Initializing Gemini API...")
    gemini_client = genai.Client(api_key=google_api_key)
    
    # Try to find an available model
    available_model = None
    try:
        models = gemini_client.models.list()
        model_names = [m.name for m in models]
        logger.info(f"Available Gemini models: {model_names}")
        
        # Look for flash or pro models
        for name in model_names:
            if 'flash' in name.lower() or 'pro' in name.lower():
                available_model = name
                break
        if not available_model and model_names:
            available_model = model_names[0]
    except Exception as e:
        logger.warning(f"Could not list models: {e}. Using fallback.")
        # Fallback to try common names
        available_model = 'models/gemini-1.5-flash'
    
    logger.info(f"Using Gemini model: {available_model}")
    
    # Initialize unified fetcher
    logger.info("Initializing unified data fetcher...")
    fetcher = UnifiedDataFetcher()
    
    logger.info("✅ All components initialized successfully!")
    
    return {
        'embedding_model': embedding_model,
        'collection': collection,
        'gemini_client': gemini_client,
        'fetcher': fetcher,
        'available_model': available_model,
        'telegram_token': telegram_token
    }

# Initialize components
components = initialize_components()

# ============================================
# CHATBOT LOGIC
# ============================================

def get_answer(question):
    """
    Get answer from unified chatbot with live data
    
    Args:
        question: User's question
    
    Returns:
        tuple: (answer_text, stored_count, live_count, live_summary)
    """
    
    # Step 1: Search local database
    logger.info(f"Searching stored database for: {question}")
    query_embedding = components['embedding_model'].encode([question])
    results = components['collection'].query(
        query_embeddings=query_embedding.tolist(),
        n_results=12
    )
    
    stored_context = []
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        stored_context.append(f"[STORED DATA] Source {i+1}:\n{doc}\n")
    
    # Step 2: Fetch live data from all sources
    logger.info("Fetching live data from all sources...")
    live_context = []
    live_summary = {}
    
    try:
        all_data = components['fetcher'].fetch_all_sources(question)
        
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
        
        logger.info(f"Live data summary: {live_summary}")
        
    except Exception as e:
        logger.error(f"Live data fetch error: {e}")
    
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
- Be concise but comprehensive (keep responses under 4096 characters for Telegram)
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
    logger.info("Generating response with Gemini...")
    for attempt in range(3):
        try:
            response = components['gemini_client'].models.generate_content(
                model=components['available_model'],
                contents=prompt
            )
            
            answer = response.text
            
            # Truncate if too long for Telegram (max 4096 chars)
            if len(answer) > 4000:
                answer = answer[:4000] + "\n\n...(truncated)"
            
            return answer, len(stored_context), len(live_context), live_summary
            
        except Exception as e:
            error_str = str(e)
            logger.error(f"Gemini API error (attempt {attempt + 1}): {error_str}")
            
            if "503" in error_str or "UNAVAILABLE" in error_str:
                if attempt < 2:
                    import time
                    time.sleep(2)
                    continue
                else:
                    return "🔄 AI service is temporarily busy. Please try again in a moment.", 0, 0, {}
            else:
                return f"❌ Error: {error_str}", 0, 0, {}
    
    return "❌ Failed to get response. Please try again.", 0, 0, {}

# ============================================
# TELEGRAM BOT COMMANDS
# ============================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is issued"""
    welcome_message = """🇪🇹 <b>Welcome to SDG Ethiopia Chatbot!</b>

I provide instant access to Ethiopia's Sustainable Development Goals (SDGs) data from multiple authoritative sources:

📊 <b>Data Sources:</b>
🌍 World Bank API - Real-time indicators
🇪🇹 ESS Website - Latest Ethiopian statistics  
🔵 UN SDG Database - Quarterly updates
📁 11,346 stored historical documents

💡 <b>Example Questions:</b>
• What is Ethiopia's current poverty rate?
• Show me education enrollment trends
• Latest child mortality statistics
• Access to electricity in Ethiopia
• Forest coverage changes over time

📱 <b>Commands:</b>
/start - Show this welcome message
/help - How to use the bot
/examples - More example questions
/stats - Bot statistics
/about - About the developer

Just ask me any question about Ethiopia's SDG data! 🚀
"""
    await update.message.reply_text(welcome_message, parse_mode='HTML')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message when /help is issued"""
    help_message = """📖 <b>How to Use This Bot</b>

Simply type your question in plain English!

<b>Examples:</b>
1️⃣ "What is Ethiopia's GDP growth rate?"
2️⃣ "Show poverty trends since 2010"
3️⃣ "How many children are enrolled in primary school?"
4️⃣ "What percentage of Ethiopians have electricity?"
5️⃣ "Latest data on child mortality"

<b>Tips for Best Results:</b>
✅ Be specific (mention years, indicators, regions)
✅ Ask about measurable data points
✅ Use keywords like "latest", "trend", "compare"

<b>Data Coverage:</b>
📅 Years: 1995-2026
📊 Indicators: 465+ unique metrics
🌍 Sources: UN, World Bank, ESS

Need examples? Type /examples
"""
    await update.message.reply_text(help_message, parse_mode='HTML')

async def examples_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send example questions when /examples is issued"""
    examples_message = """💡 <b>Example Questions by Category</b>

<b>📉 Poverty &amp; Income:</b>
• What is Ethiopia's poverty headcount ratio?
• Show income inequality trends
• GDP per capita over time

<b>🎓 Education:</b>
• Primary school enrollment rate
• Literacy rate in Ethiopia
• Gender gap in education

<b>🏥 Health:</b>
• Child mortality rates
• Life expectancy trends
• Access to healthcare facilities

<b>⚡ Infrastructure:</b>
• Electricity access in rural areas
• Clean water availability
• Internet penetration rate

<b>🌳 Environment:</b>
• Forest coverage changes
• CO2 emissions data
• Renewable energy usage

<b>👥 Demographics:</b>
• Population growth rate
• Urban vs rural population
• Youth unemployment rate

Try any of these or ask your own question!
"""
    await update.message.reply_text(examples_message, parse_mode='HTML')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics when /stats is issued"""
    try:
        # Get collection stats
        collection_count = components['collection'].count()
        
        stats_message = f"""📊 <b>Bot Statistics</b>

<b>Database:</b>
📁 Stored Documents: {collection_count:,}
📊 Unique Indicators: 465+
📅 Data Years: 1995-2026

<b>Live Data Sources:</b>
🌍 World Bank API: Active
🇪🇹 ESS Website: Active
🔵 UN SDG Database: Active

<b>AI Model:</b>
🤖 {html.escape(components['available_model'])}

<b>Status:</b> ✅ All systems operational
"""
        await update.message.reply_text(stats_message, parse_mode='HTML')
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error getting stats: {str(e)}")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show information about the developer when /about is issued"""
    about_message = """👨‍💻 <b>About the Developer</b>

<b>Name:</b> Yonas Abiyu Ghion
<b>University:</b> Bahir Dar University 🎓
<b>Program:</b> Data Science (3rd Year)
<b>Location:</b> Ethiopia 🇪🇹

<b>Project Overview:</b>
This intelligent chatbot was built to democratize access to Ethiopia's development data. By combining AI technology with authoritative data sources, it makes complex statistics accessible to everyone - from researchers and policymakers to students and citizens.

<b>Technical Stack:</b>
• 🤖 AI: Google Gemini
• 🔍 Vector DB: ChromaDB (11,346+ docs)
• 🌐 Live APIs: UN, World Bank, ESS
• 💻 Built with: Python, LangChain
• 📱 Platform: Telegram Bot API

<b>Mission:</b>
Making data-driven decision making accessible to all Ethiopians by bridging the gap between raw statistics and actionable insights.

<b>Connect:</b>
Have feedback or suggestions? The bot is continuously evolving to serve you better!

---
<i>"Data is the new oil, but insights are the refined fuel."</i>
"""
    await update.message.reply_text(about_message, parse_mode='HTML')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages (questions)"""
    user_question = update.message.text
    user_name = update.effective_user.first_name
    chat_id = update.effective_chat.id
    
    logger.info(f"Question from {user_name} (chat_id: {chat_id}): {user_question}")
    
    try:
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        # Get answer (send typing indicator periodically during this)
        import asyncio
        
        # Run get_answer in a way that allows us to send typing indicators
        answer_task = asyncio.create_task(
            asyncio.to_thread(get_answer, user_question)
        )
        
        # Keep sending typing indicator while waiting
        while not answer_task.done():
            await context.bot.send_chat_action(chat_id=chat_id, action="typing")
            try:
                await asyncio.wait_for(asyncio.shield(answer_task), timeout=4.0)
            except asyncio.TimeoutError:
                continue  # Keep looping and send typing indicator again
        
        # Get the result
        answer, stored_count, live_count, live_summary = await answer_task
        
        # Build status message
        status_parts = []
        if 'world_bank' in live_summary:
            status_parts.append(f"🌍 World Bank: {live_summary['world_bank']}")
        if 'ess' in live_summary:
            status_parts.append(f"🇪🇹 ESS: {live_summary['ess']}")
        if 'un' in live_summary:
            status_parts.append(f"🔵 UN: checked")
        
        status_line = " | ".join(status_parts) if status_parts else "Using stored data"
        
        # Build final message
        # Convert AI's markdown formatting to HTML for better readability
        
        # Convert common markdown patterns to HTML
        formatted_answer = answer
        
        # Convert **bold** to <b>bold</b>
        formatted_answer = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', formatted_answer)
        
        # Convert *italic* to <i>italic</i> (but not already converted ** patterns)
        formatted_answer = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', formatted_answer)
        
        # Convert bullet points to proper format
        formatted_answer = formatted_answer.replace('* ', '• ')
        formatted_answer = formatted_answer.replace('- ', '• ')
        
        # Escape remaining HTML special characters but preserve our formatting tags
        formatted_answer = formatted_answer.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Restore our HTML tags
        formatted_answer = formatted_answer.replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
        formatted_answer = formatted_answer.replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>')
        
        safe_status = html.escape(status_line)
        
        final_message = f"""📊 <b>Answer:</b>

{formatted_answer}

━━━━━━━━━━━━━━━
📈 <b>Sources:</b> {stored_count} stored + {live_count} live
🌐 <b>Live Data:</b> {safe_status}
"""
        
        # Send answer using HTML parse mode (more forgiving than Markdown)
        try:
            await update.message.reply_text(final_message, parse_mode='HTML')
        except Exception as parse_error:
            # If even HTML fails, send as plain text with cleaned formatting
            logger.warning(f"HTML parse error, sending as plain text: {parse_error}")
            
            # Remove all formatting
            clean_answer = re.sub(r'[*_`<>]', '', answer)
            
            plain_message = f"""📊 Answer:

{clean_answer}

━━━━━━━━━━━━━━━
📈 Sources: {stored_count} stored + {live_count} live
🌐 Live Data: {status_line}
"""
            await update.message.reply_text(plain_message)
        
        logger.info(f"Response sent: {stored_count} stored + {live_count} live sources")
        
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.message:
        await update.message.reply_text(
            "❌ Sorry, an error occurred. Please try again or contact support."
        )

# ============================================
# MAIN
# ============================================

def main():
    """Start the bot"""
    logger.info("🚀 Starting SDG Ethiopia Telegram Bot...")
    
    # Create application
    application = Application.builder().token(components['telegram_token']).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("examples", examples_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
