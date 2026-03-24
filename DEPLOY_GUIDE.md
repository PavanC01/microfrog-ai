# MicroFrog — Deployment Guide (Render.com)

## Your Project Files

microfrog-backend/
├── app.py              ← Python backend (Flask server)
├── requirements.txt    ← Python packages
├── Procfile            ← Tells Render how to start
└── static/
    └── index.html      ← Your MicroFrog chat interface

---

## Step 1 — Create a GitHub Account
Go to https://github.com and sign up (free).

## Step 2 — Upload Your Project to GitHub
1. Click the "+" button → "New repository"
2. Name it: microfrog-ai
3. Set to Public
4. Click "Create repository"
5. Upload all your files (app.py, requirements.txt, Procfile, static/index.html)

## Step 3 — Create a Render Account
Go to https://render.com and sign up with GitHub (free).

## Step 4 — Deploy on Render
1. Click "New +" → "Web Service"
2. Connect your GitHub repo: microfrog-ai
3. Fill in these settings:
   - Name: microfrog-ai
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
4. Click "Advanced" → "Add Environment Variable"
   - Key:   HF_TOKEN
   - Value: (paste your HuggingFace token here)
5. Click "Create Web Service"

## Step 5 — Get Your HuggingFace Token
1. Go to https://huggingface.co/settings/tokens
2. Click "New token" → Read access → Copy it
3. Paste it as HF_TOKEN in Render (Step 4)

## Step 6 — Your MicroFrog is Live!
After ~2 minutes, Render gives you a URL like:
   https://microfrog-ai.onrender.com

Share this with anyone — MicroFrog is now live for the world! 🚀

---

## Upgrading Later
- Add more features → edit app.py → push to GitHub → Render auto-deploys
- Custom domain → Render Settings → Custom Domains (free)
- More AI models → change HF_API_URL in app.py
