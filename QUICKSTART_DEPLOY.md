# 🚀 Quick Deploy to Vercel + Railway

## Prasyarat
- Akun GitHub (sudah ada ✓)
- Akun Vercel (gratis): https://vercel.com/signup
- Akun Railway (gratis): https://railway.app

---

## 🎯 Deploy Cepat (5 Menit)

### 1️⃣ Deploy Backend (Railway)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy backend
cd backend
railway init
railway up
```

Tunggu sampai selesai, lalu:
1. Buka Railway Dashboard
2. Add PostgreSQL database: "New" → "Database" → "PostgreSQL"
3. Generate secret keys:
   ```bash
   python generate_secrets.py
   ```
4. Set Environment Variables di Railway Dashboard:
   ```
   FLASK_ENV=production
   SECRET_KEY=<dari generate_secrets.py>
   JWT_SECRET_KEY=<dari generate_secrets.py>
   CORS_ORIGINS=https://your-app.vercel.app
   MAX_FILE_SIZE=5242880
   UPLOAD_FOLDER=/tmp/uploads
   ```
5. Copy URL backend Railway (contoh: `https://your-app.railway.app`)

### 2️⃣ Deploy Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy (dari root project)
cd ..
vercel
```

Ikuti prompt, lalu:
1. Set environment variable:
   ```bash
   vercel env add REACT_APP_API_URL
   # Paste Railway URL: https://your-app.railway.app
   ```
2. Deploy production:
   ```bash
   vercel --prod
   ```

### 3️⃣ Update CORS

Setelah Vercel deploy:
1. Copy URL Vercel (contoh: `https://ai-recruitment.vercel.app`)
2. Update `CORS_ORIGINS` di Railway dengan URL Vercel
3. Railway akan auto-redeploy

---

## ✅ Selesai!

Frontend: https://your-app.vercel.app
Backend: https://your-app.railway.app

---

## 📖 Full Guide

Lihat `DEPLOYMENT_VERCEL.md` untuk panduan lengkap dan troubleshooting.

---

## 🔄 Update Setelah Deploy

### Update Backend
```bash
cd backend
git push  # Atau railway up
```

### Update Frontend
```bash
git push  # Atau vercel --prod
```

Railway dan Vercel support auto-deploy dari GitHub!
