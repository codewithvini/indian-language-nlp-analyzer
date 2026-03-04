# 🚀 Deployment Guide - Render.com

## Prerequisites
- GitHub account (you already have this connected)
- Render account (create free at [render.com](https://render.com))

---

## 📦 Step-by-Step Deployment on Render

### Step 1: Push Your Code to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit your code
git commit -m "Initial commit - Indian Language NLP Analyzer"

# Create a new repository on GitHub (via GitHub website)
# Then connect it:
git remote add origin https://github.com/YOUR_USERNAME/indian-language-nlp-analyzer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. Click **"New +"** button → Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository: **`indian-language-nlp-analyzer`**
5. Configure the service:

   **Basic Settings:**
   - **Name:** `indian-language-nlp-analyzer`
   - **Region:** Select closest to you (e.g., Singapore, Oregon)
   - **Branch:** `main`
   - **Root Directory:** Leave empty
   - **Runtime:** `Python 3`

   **Build Settings:**
   - **Build Command:**
     ```
     pip install -r requirements.txt && python -m nltk.downloader punkt averaged_perceptron_tagger maxent_ne_chunker words
     ```
   - **Start Command:**
     ```
     gunicorn analyzer:app
     ```

   **Instance Type:**
   - Select **"Free"** (0$/month)

6. Click **"Create Web Service"**

### Step 3: Wait for Deployment

- Render will automatically:
  - Install Python dependencies
  - Download NLTK data
  - Start your Flask application
- Deployment takes 3-5 minutes
- You'll see live logs in the dashboard

### Step 4: Access Your Live Website

Once deployed, Render provides a URL like:
```
https://indian-language-nlp-analyzer.onrender.com
```

**Your website is now LIVE! 🎉**

---

## ⚠️ Important Notes

### Free Tier Limitations:
- Service **spins down after 15 minutes of inactivity**
- First request after inactivity takes **30-60 seconds** to wake up
- 750 hours/month free (sufficient for most projects)

### To Keep Service Always Active (Optional):
- Upgrade to paid plan ($7/month)
- Or use a ping service like [UptimeRobot](https://uptimerobot.com) to ping your site every 14 minutes

---

## 🔧 Alternative: Manual Configuration

If render.yaml doesn't auto-detect, use these settings:

**Environment Variables:**
```
PYTHON_VERSION=3.12.3
```

**Build Command:**
```bash
pip install -r requirements.txt && python -m nltk.downloader punkt averaged_perceptron_tagger maxent_ne_chunker words
```

**Start Command:**
```bash
gunicorn analyzer:app
```

---

## 🐛 Troubleshooting

### Issue: Build fails with "Module not found"
**Solution:** Check requirements.txt has all dependencies

### Issue: NLTK data not found
**Solution:** Ensure build command includes NLTK downloader

### Issue: Application timeout
**Solution:** Free tier has cold starts, wait 60 seconds on first load

### Issue: CORS errors
**Solution:** Already configured in analyzer.py with Flask-CORS

---

## 📱 Test Your Deployment

1. Open your Render URL
2. Enter test text: "This is amazing! मुझे यह पसंद है"
3. Click "Analyze Text"
4. Verify all features work:
   - ✅ Language detection
   - ✅ Sentiment analysis
   - ✅ Key terms extraction
   - ✅ Word cloud generation
   - ✅ Text statistics

---

## 🔄 Update Your Deployed Site

Whenever you make code changes:

```bash
git add .
git commit -m "Update: your changes description"
git push origin main
```

Render will **automatically redeploy** within 2-3 minutes!

---

## 📊 Monitor Your Application

**Render Dashboard provides:**
- Live logs
- CPU/Memory usage
- Request metrics
- Deployment history

---

## 🎓 For Your Project Report

**Deployment Details:**
- **Platform:** Render.com
- **Type:** Cloud-based Web Service
- **Runtime:** Python 3.12 + Gunicorn WSGI server
- **URL:** https://your-app-name.onrender.com
- **Auto-Deploy:** Enabled via GitHub integration
- **Scaling:** Horizontal scaling available (paid tier)

---

## 💡 Need Help?

- **Render Docs:** https://render.com/docs
- **Render Community:** https://community.render.com
- **Your Logs:** Check Render dashboard → Your service → Logs tab

---

Good luck with your deployment! 🚀
