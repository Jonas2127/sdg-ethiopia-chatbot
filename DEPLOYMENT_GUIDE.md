# 🚀 Deployment Guide - 24/7 Online Chatbot

Complete guide to deploy your SDG Ethiopia Chatbot for 24/7 availability and share with ESS advisors.

---

## 📋 Table of Contents
1. [Deployment Options Comparison](#deployment-options-comparison)
2. [Option A: Streamlit Cloud (Recommended - FREE)](#option-a-streamlit-cloud-free)
3. [Option B: Render.com (Good Alternative - FREE)](#option-b-rendercom-free)
4. [Option C: PythonAnywhere (Limited Free)](#option-c-pythonanywhere-limited-free)
5. [Option D: ESS Internal Server](#option-d-ess-internal-server)
6. [Telegram Bot Deployment](#telegram-bot-deployment)
7. [Sharing with ESS Advisors](#sharing-with-ess-advisors)

---

## 🔍 Deployment Options Comparison

| Option | Cost | Difficulty | Speed | Best For |
|--------|------|------------|-------|----------|
| **Streamlit Cloud** | FREE | ⭐ Easy | Fast | Web interface |
| **Render.com** | FREE | ⭐⭐ Medium | Fast | Web + API |
| **PythonAnywhere** | Free (limited) | ⭐⭐ Medium | Slow | Simple hosting |
| **ESS Server** | Free (internal) | ⭐⭐⭐ Hard | Very Fast | Official deployment |

---

## ✅ Option A: Streamlit Cloud (RECOMMENDED - FREE)

### Why Streamlit Cloud?
- ✅ **100% FREE** forever
- ✅ **Easy deployment** (5 minutes)
- ✅ **Auto-updates** when you push to GitHub
- ✅ **Built for Streamlit** (your web interface)
- ✅ **Reliable** (99.9% uptime)
- ✅ **HTTPS** (secure) with custom domain support

### Step-by-Step Deployment:

#### 1️⃣ Prepare Your Project

**Create `.streamlit/config.toml` file:**
```bash
mkdir .streamlit
```

Create file: `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#00B140"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "serif"

[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

**Create `.streamlit/secrets.toml` for API keys:**
```toml
GOOGLE_API_KEY = "your_google_api_key_here"
TELEGRAM_BOT_TOKEN = "your_telegram_token_here"
```

⚠️ **Add to `.gitignore`:**
```
.streamlit/secrets.toml
.env
```

#### 2️⃣ Push to GitHub

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit - SDG Ethiopia Chatbot"

# Create GitHub repository
# Go to: https://github.com/new
# Name it: sdg-ethiopia-chatbot
# Don't initialize with README (you already have one)

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/sdg-ethiopia-chatbot.git
git branch -M main
git push -u origin main
```

#### 3️⃣ Deploy on Streamlit Cloud

1. **Go to:** https://share.streamlit.io/
2. **Sign in** with GitHub
3. **Click:** "New app"
4. **Fill in:**
   - Repository: `YOUR_USERNAME/sdg-ethiopia-chatbot`
   - Branch: `main`
   - Main file path: `app.py`
5. **Click:** "Advanced settings"
6. **Add secrets** (copy from `.streamlit/secrets.toml`)
7. **Click:** "Deploy!"

#### 4️⃣ Get Your URL

After deployment, you'll get a URL like:
```
https://sdg-ethiopia-chatbot-XXXXX.streamlit.app
```

**Optional: Custom Domain**
- Go to Settings → General
- Add custom domain: `chatbot.ess.gov.et` (if ESS has this)

#### 5️⃣ Share with ESS Advisors

Send them:
```
🔗 SDG Ethiopia Chatbot
https://your-app.streamlit.app

📱 Telegram Bot
https://t.me/your_bot_username

📧 Access:
- No login required
- Works 24/7
- Mobile-friendly
```

---

## 🟢 Option B: Render.com (Good Alternative - FREE)

### Step-by-Step:

#### 1️⃣ Create `render.yaml`

```yaml
services:
  - type: web
    name: sdg-ethiopia-chatbot
    env: python
    region: frankfurt  # Closer to Ethiopia
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: GOOGLE_API_KEY
        sync: false
      - key: TELEGRAM_BOT_TOKEN
        sync: false
```

#### 2️⃣ Push to GitHub (same as above)

#### 3️⃣ Deploy on Render

1. **Go to:** https://render.com
2. **Sign up** with GitHub
3. **New** → **Blueprint**
4. **Connect repository:** `sdg-ethiopia-chatbot`
5. **Add environment variables:**
   - `GOOGLE_API_KEY`: Your key
   - `TELEGRAM_BOT_TOKEN`: Your token
6. **Deploy**

#### 4️⃣ Get URL
```
https://sdg-ethiopia-chatbot.onrender.com
```

---

## 🟡 Option C: PythonAnywhere (Limited Free)

### Limitations:
- ❌ Only 100 seconds CPU/day (free tier)
- ❌ Needs daily restart
- ✅ Good for testing

### Quick Setup:

1. **Sign up:** https://www.pythonanywhere.com
2. **Upload files:** Use "Files" tab
3. **Install packages:**
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
4. **Create web app:**
   - Web tab → Add new web app
   - Manual configuration
   - Python 3.10
   - WSGI file: Point to your app
5. **Set environment variables:** in WSGI file

---

## 🏢 Option D: ESS Internal Server (Best for Official Use)

### Requirements:
- ESS IT department access
- Server with Python 3.10+
- Static IP or domain

### Deployment Steps:

#### 1️⃣ Server Setup (Ubuntu/Linux)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.10 python3.10-venv python3-pip nginx -y

# Create deployment user
sudo useradd -m -s /bin/bash chatbot
sudo su - chatbot

# Clone repository
git clone https://github.com/YOUR_USERNAME/sdg-ethiopia-chatbot.git
cd sdg-ethiopia-chatbot

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2️⃣ Create Systemd Service

Create `/etc/systemd/system/sdg-chatbot.service`:

```ini
[Unit]
Description=SDG Ethiopia Chatbot
After=network.target

[Service]
Type=simple
User=chatbot
WorkingDirectory=/home/chatbot/sdg-ethiopia-chatbot
Environment="PATH=/home/chatbot/sdg-ethiopia-chatbot/venv/bin"
ExecStart=/home/chatbot/sdg-ethiopia-chatbot/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable sdg-chatbot
sudo systemctl start sdg-chatbot
sudo systemctl status sdg-chatbot
```

#### 3️⃣ Configure Nginx (Reverse Proxy)

Create `/etc/nginx/sites-available/chatbot`:

```nginx
server {
    listen 80;
    server_name chatbot.ess.gov.et;  # Your domain

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

**Enable:**
```bash
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 4️⃣ SSL Certificate (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d chatbot.ess.gov.et
```

---

## 📱 Telegram Bot Deployment

### Keep Telegram Bot Running 24/7:

#### Option 1: Same Server as Web App

**Create service:** `/etc/systemd/system/telegram-bot.service`

```ini
[Unit]
Description=SDG Ethiopia Telegram Bot
After=network.target

[Service]
Type=simple
User=chatbot
WorkingDirectory=/home/chatbot/sdg-ethiopia-chatbot
Environment="PATH=/home/chatbot/sdg-ethiopia-chatbot/venv/bin"
ExecStart=/home/chatbot/sdg-ethiopia-chatbot/venv/bin/python telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

#### Option 2: Render.com (Separate)

Add to `render.yaml`:

```yaml
  - type: background
    name: telegram-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python telegram_bot.py
    envVars:
      - key: GOOGLE_API_KEY
        sync: false
      - key: TELEGRAM_BOT_TOKEN
        sync: false
```

---

## 👥 Sharing with ESS Advisors

### Create Professional Documentation Package:

#### 1️⃣ Access Information Document

Create `ESS_ADVISOR_GUIDE.pdf`:

```markdown
# SDG Ethiopia Chatbot - Access Guide

## 🌐 Web Interface
**URL:** https://your-app.streamlit.app
**Access:** Open link in any browser
**Works on:** Desktop, Mobile, Tablet

## 📱 Telegram Bot
**Username:** @your_bot_username
**Link:** https://t.me/your_bot_username
**Setup:**
1. Click link above or search in Telegram
2. Press "Start"
3. Ask your question!

## 💡 Example Questions:
- What is Ethiopia's poverty rate in 2024?
- Show education enrollment trends
- Latest child mortality statistics
- Access to electricity in rural areas

## 📊 Data Sources:
- UN SDG Database (11,346 documents)
- World Bank API (real-time)
- ESS Website (live data)

## 📞 Support:
Contact: Yonas Abiyu Ghion
Email: your.email@example.com
Phone: +251-XXX-XXX-XXX
```

#### 2️⃣ Email Template

```
Subject: SDG Ethiopia Chatbot - Now Available 24/7

Dear [Advisor Name],

I'm pleased to share the SDG Ethiopia Chatbot, now deployed and available 24/7 for your use.

🔗 Access Links:
━━━━━━━━━━━━━━━━━
Web Interface: https://your-app.streamlit.app
Telegram Bot: https://t.me/your_bot_username

📊 Features:
━━━━━━━━━━━━━━━━━
✅ Real-time data from UN, World Bank, and ESS
✅ 11,346+ verified data points
✅ Natural language queries
✅ Mobile-friendly interface
✅ Available 24/7

💡 Try asking:
━━━━━━━━━━━━━━━━━
"What is Ethiopia's current poverty rate?"
"Show education enrollment trends since 2015"
"Latest child mortality statistics"

The system provides instant, evidence-based insights backed by official data sources.

Attached: User Guide (PDF)

Best regards,
Yonas Abiyu Ghion
Data Science Student, Bahir Dar University
```

#### 3️⃣ Create QR Codes

For easy mobile access:

1. **Web QR Code:** https://qr-code-generator.com
   - Enter: Your app URL
   - Download QR code
   
2. **Telegram QR Code:**
   - Enter: `https://t.me/your_bot_username`
   - Download QR code

Print and distribute!

---

## 🔐 Security Best Practices

### 1. Protect API Keys
```python
# Never commit .env or secrets.toml to GitHub
# Use environment variables
# Rotate keys regularly
```

### 2. Rate Limiting
Consider adding to `app.py`:
```python
import streamlit as st
from datetime import datetime, timedelta

# Simple rate limiting
if 'last_request' not in st.session_state:
    st.session_state.last_request = datetime.now()

time_since_last = datetime.now() - st.session_state.last_request
if time_since_last < timedelta(seconds=2):
    st.warning("Please wait a moment between requests.")
    st.stop()

st.session_state.last_request = datetime.now()
```

### 3. Usage Analytics
Add Google Analytics or Plausible to track usage.

---

## 📈 Monitoring & Maintenance

### Monitor Your App:

#### Streamlit Cloud:
- Dashboard: https://share.streamlit.io
- View logs, metrics, errors
- Auto-restarts on crash

#### Server Deployment:
```bash
# Check status
sudo systemctl status sdg-chatbot
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u sdg-chatbot -f
sudo journalctl -u telegram-bot -f

# Restart if needed
sudo systemctl restart sdg-chatbot
```

### Update Deployment:

```bash
# Pull latest changes
git pull origin main

# Restart services
sudo systemctl restart sdg-chatbot
sudo systemctl restart telegram-bot
```

---

## 💰 Cost Estimates

| Option | Free Tier | Paid Tier | Best For |
|--------|-----------|-----------|----------|
| **Streamlit Cloud** | Unlimited | - | Web only |
| **Render.com** | 750 hours/month | $7/month | Web + Bot |
| **PythonAnywhere** | Limited | $5/month | Testing |
| **ESS Server** | FREE | Maintenance | Production |

### Recommended Setup:
- **Web:** Streamlit Cloud (FREE)
- **Telegram:** Render.com (FREE tier)
- **Total Cost:** $0/month 🎉

---

## ✅ Deployment Checklist

### Pre-Deployment:
- [ ] Test locally (web + telegram bot)
- [ ] Update `requirements.txt`
- [ ] Create `.gitignore` (exclude secrets)
- [ ] Add documentation
- [ ] Test with sample questions

### Deployment:
- [ ] Push to GitHub
- [ ] Deploy web app (Streamlit Cloud recommended)
- [ ] Deploy telegram bot
- [ ] Add environment variables
- [ ] Test deployed version

### Post-Deployment:
- [ ] Create access guide for advisors
- [ ] Generate QR codes
- [ ] Send access information email
- [ ] Monitor logs for errors
- [ ] Collect feedback

---

## 🆘 Troubleshooting

### App Won't Start
**Check:**
1. All files uploaded correctly
2. `requirements.txt` complete
3. Environment variables set
4. Logs for error messages

### Slow Performance
**Solutions:**
1. Use caching (`@st.cache_resource`)
2. Reduce `n_results` in queries
3. Optimize image sizes
4. Use CDN for assets

### API Quota Exceeded
**Solutions:**
1. Upgrade Google API plan
2. Implement request caching
3. Add rate limiting
4. Use multiple API keys

---

## 📞 Next Steps

1. **Choose deployment option** (Streamlit Cloud recommended)
2. **Follow deployment guide** (5-10 minutes)
3. **Test thoroughly** (ask various questions)
4. **Create advisor guide** (use template above)
5. **Share with ESS team** (email + QR codes)
6. **Collect feedback** (iterate and improve)

---

## 🎉 Congratulations!

Your SDG Ethiopia Chatbot is now ready for production! 🇪🇹

**Deployed by:** Yonas Abiyu Ghion
**Institution:** Bahir Dar University
**Program:** Data Science (3rd Year)
**Date:** January 2027

---

**Questions or issues?**
Check `docs/TROUBLESHOOTING.md` or contact support.
