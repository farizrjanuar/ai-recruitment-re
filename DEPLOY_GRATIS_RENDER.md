# 🆓 Deploy GRATIS ke Render.com

## ✅ Kenapa Render?
- 100% GRATIS (no credit card)
- PostgreSQL database included
- Auto SSL/HTTPS
- Sudah ada config `render.yaml`

---

## 🚀 Langkah Deploy (5 Menit)

### 1️⃣ Push Code ke GitHub

```bash
cd /Users/farizrjanuar/Comproj/ai-recruitment-re

# Check status
git status

# Add semua file baru (deployment configs)
git add .

# Commit
git commit -m "Add deployment configs for Render and Vercel"

# Push ke GitHub
git push origin master
```

### 2️⃣ Deploy Backend ke Render

1. **Buka [render.com](https://render.com)** dan sign up (GRATIS, no credit card)
2. Klik **"New"** → **"Blueprint"**
3. **Connect GitHub** dan pilih repository `ai-recruitment-re`
4. Render akan detect `render.yaml` dan auto-setup:
   - Web Service (Backend)
   - PostgreSQL Database
   - Environment Variables
5. Klik **"Apply"**
6. Tunggu ~5-10 menit untuk build

✅ Backend URL: `https://ai-recruitment-backend.onrender.com`

### 3️⃣ Deploy Frontend ke Vercel

```bash
# Install Vercel CLI (if not installed)
npm i -g vercel

# Login (GRATIS)
vercel login

# Deploy
cd /Users/farizrjanuar/Comproj/ai-recruitment-re
vercel
```

Ikuti prompt:
- Set up and deploy? **Y**
- Which scope? Pilih account
- Link to existing? **N**
- Project name? **ai-recruitment**
- Directory? **./**
- Override settings? **Y**
  - Build: **npm run build**
  - Output: **build**

Setelah deploy, set environment variable:

```bash
# Set API URL
vercel env add REACT_APP_API_URL production

# Paste Render backend URL
# https://ai-recruitment-backend.onrender.com

# Redeploy
vercel --prod
```

✅ Frontend URL: `https://ai-recruitment.vercel.app`

### 4️⃣ Update CORS di Render

1. Buka [Render Dashboard](https://dashboard.render.com)
2. Pilih service **ai-recruitment-backend**
3. Klik **Environment** tab
4. Update `CORS_ORIGINS`:
   ```
   https://ai-recruitment.vercel.app,http://localhost:3000
   ```
5. Save (akan auto-redeploy)

---

## ✅ Done! Aplikasi LIVE & GRATIS!

- **Frontend**: https://ai-recruitment.vercel.app
- **Backend**: https://ai-recruitment-backend.onrender.com

---

## 📋 Render Free Tier Limits

- ✅ 750 jam/bulan (25 hari)
- ✅ PostgreSQL 1GB storage
- ✅ 100GB bandwidth/bulan
- ✅ Unlimited requests
- ⚠️ Sleep after 15 min inactive (wake up ~30 sec)

**Solusi Sleep Issue:**
- Gunakan uptime monitor gratis (UptimeRobot.com)
- Ping backend setiap 10 menit
- Atau upgrade ke Render Starter ($7/bulan) untuk no sleep

---

## 🔄 Update Setelah Deploy

### Update Backend
```bash
git add .
git commit -m "Update backend"
git push origin master
# Render auto-deploy!
```

### Update Frontend
```bash
git add .
git commit -m "Update frontend"
git push origin master
# Vercel auto-deploy!
```

Keduanya support **auto-deploy from GitHub**!

---

## 💡 Tips Render Free Tier

1. **Keep Awake**: Setup UptimeRobot untuk ping setiap 10 menit
2. **Database Backup**: Export database berkala via pgAdmin
3. **Logs**: Check logs di Render dashboard jika ada error
4. **Custom Domain**: Bisa add domain gratis di Render

---

## 🆘 Troubleshooting

### Backend Sleep
**Problem**: App tidak respond

**Solution**: 
- Tunggu 30 detik (wake up time)
- Atau setup UptimeRobot untuk keep alive
- Atau upgrade ke Starter plan ($7/month)

### Build Failed
**Problem**: Build error di Render

**Solution**:
1. Check logs di Render dashboard
2. Pastikan `requirements.txt` lengkap
3. Pastikan Python version compatible (3.11)

### Database Connection Error
**Problem**: Backend tidak connect ke database

**Solution**:
- DATABASE_URL auto-generated oleh Render
- Check environment variables di dashboard
- Restart service

---

## 🎯 Cost: $0/month

Benar-benar GRATIS untuk:
- Backend + Database (Render)
- Frontend (Vercel)
- SSL/HTTPS
- Custom domain

**Total: $0** 🎉
