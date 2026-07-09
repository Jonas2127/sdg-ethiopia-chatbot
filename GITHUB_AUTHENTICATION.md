# 🔐 GitHub Authentication Guide

You need to authenticate with GitHub to push your code. Here are **2 EASY OPTIONS**:

---

## ✅ **OPTION 1: Use GitHub Desktop (EASIEST - RECOMMENDED)**

### **Download and Install:**
1. Go to: **https://desktop.github.com/**
2. Download and install GitHub Desktop
3. Open it and **sign in with your GitHub account**

### **Publish Your Repository:**
1. In GitHub Desktop, click: **File** → **Add Local Repository**
2. Browse to: `C:\Users\HP\.vscode\Documents\ESSproject 2\sdg-ethiopia-chatbot`
3. Click: **Add Repository**
4. Click: **Publish repository** button
5. Make sure **"Keep this code private"** is UNCHECKED (we need it public for Streamlit)
6. Click: **Publish repository**

### **Done! ✅**
Your code is now on GitHub at: **https://github.com/Jonas2127/sdg-ethiopia-chatbot**

---

## ✅ **OPTION 2: Use Personal Access Token (Command Line)**

If you prefer command line, follow these steps:

### **Step 1: Create Personal Access Token**

1. Go to: **https://github.com/settings/tokens**
2. Click: **"Generate new token"** → **"Generate new token (classic)"**
3. Fill in:
   - **Note**: `SDG Chatbot Deployment`
   - **Expiration**: 90 days
   - **Select scopes**: Check ✅ **repo** (this will check all sub-boxes)
4. Scroll down, click: **"Generate token"**
5. **IMPORTANT**: Copy the token (starts with `ghp_...`) - you won't see it again!

### **Step 2: Push with Token**

Open Command Prompt in your project folder and run:

```bash
git push -u https://ghp_YOUR_TOKEN_HERE@github.com/Jonas2127/sdg-ethiopia-chatbot.git main
```

Replace `ghp_YOUR_TOKEN_HERE` with the token you copied.

---

## 🎯 **Which Option Should You Choose?**

| Option | Difficulty | Time | Best For |
|--------|-----------|------|----------|
| **GitHub Desktop** | ⭐ Very Easy | 5 min | Beginners |
| **Access Token** | ⭐⭐ Medium | 5 min | Advanced users |

**RECOMMENDATION: Use GitHub Desktop - it's much easier!**

---

## ✅ **After You Push the Code**

Once your code is on GitHub, you can verify by:
1. Going to: **https://github.com/Jonas2127/sdg-ethiopia-chatbot**
2. You should see all your files there!

**Then tell me: "Code is on GitHub"** and we'll proceed to deploy on Streamlit Cloud!

---

## 🆘 **Having Issues?**

**Problem**: "Repository not found"
**Solution**: Make sure you created the repository at https://github.com/new with name `sdg-ethiopia-chatbot`

**Problem**: "Authentication failed"
**Solution**: Use GitHub Desktop (Option 1) - much easier!

**Problem**: GitHub Desktop not opening repository
**Solution**: Make sure the folder path is correct: 
`C:\Users\HP\.vscode\Documents\ESSproject 2\sdg-ethiopia-chatbot`

---

## 📞 **Need Help?**

Tell me:
1. Which option you chose (GitHub Desktop or Token)
2. What error message you see (if any)

I'll help you fix it! 🚀
