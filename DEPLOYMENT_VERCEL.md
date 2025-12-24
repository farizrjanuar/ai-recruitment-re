# 🚀 Deployment Guide - Vercel + Railway

## Arsitektur Deployment
- **Frontend**: Vercel (React App)
- **Backend**: Railway (Flask API + PostgreSQL)
- **Database**: PostgreSQL di Railway

---

## 📋 Langkah 1: Deploy Backend ke Railway

### 1.1 Install Railway CLI
```bash
npm i -g @railway/cli
```

### 1.2 Login ke Railway
```bash
railway login
```

### 1.3 Deploy Backend
```bash
cd backend
railway init
railway up
```

### 1.4 Tambah Database PostgreSQL
Di Railway Dashboard:
1. Klik project Anda
2. Klik "New" → "Database" → "Add PostgreSQL"
3. Database akan auto-connect

### 1.5 Set Environment Variables
Di Railway Dashboard → Variables:
```env
FLASK_ENV=production
SECRET_KEY=<generate-random-32-chars>
JWT_SECRET_KEY=<generate-random-32-chars>
DATABASE_URL=<auto-from-postgresql>
CORS_ORIGINS=https://your-app.vercel.app
MAX_FILE_SIZE=5242880
UPLOAD_FOLDER=/tmp/uploads
```

### 1.6 Configure Railway Settings
Railway Dashboard → Settings:
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

### 1.7 Get Backend URL
Setelah deploy sukses, copy URL backend Anda (misal: `https://your-app.railway.app`)

---

## 📋 Langkah 2: Deploy Frontend ke Vercel

### 2.1 Install Vercel CLI
```bash
npm i -g vercel
```

### 2.2 Login ke Vercel
```bash
vercel login
```

### 2.3 Deploy Frontend
Dari root project:
```bash
vercel
```

Ikuti prompt:
- Set up and deploy? **Y**
- Which scope? **Pilih account Anda**
- Link to existing project? **N**
- Project name? **ai-recruitment** (atau nama lain)
- In which directory is your code located? **./** (root)
- Want to override settings? **Y**
- Build Command: **npm run build**
- Output Directory: **build**
- Development Command: **npm start**

### 2.4 Set Environment Variables
```bash
vercel env add REACT_APP_API_URL
```
Masukkan URL backend Railway: `https://your-app.railway.app`

Atau via Vercel Dashboard:
1. Buka project di Vercel Dashboard
2. Settings → Environment Variables
3. Tambahkan:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://your-app.railway.app`
   - **Environment**: Production, Preview, Development

### 2.5 Redeploy dengan Environment Variable
```bash
vercel --prod
```

---

## 📋 Langkah 3: Update CORS di Backend

Setelah frontend deployed, update CORS_ORIGINS di Railway:

1. Copy URL Vercel Anda (misal: `https://ai-recruitment.vercel.app`)
2. Railway Dashboard → Variables
3. Update `CORS_ORIGINS` dengan URL Vercel Anda
4. Railway akan auto-redeploy

---

## ✅ Testing Deployment

### Test Backend
```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Test Frontend
1. Buka URL Vercel: `https://your-app.vercel.app`
2. Test login/register
3. Test upload CV
4. Test create job
5. Test matching

---

## 🔧 Troubleshooting

### Frontend tidak bisa connect ke Backend
**Masalah**: CORS error atau network error

**Solusi**:
1. Pastikan `REACT_APP_API_URL` di Vercel sudah benar
2. Pastikan `CORS_ORIGINS` di Railway include URL Vercel
3. Redeploy frontend: `vercel --prod`
4. Clear browser cache

### Backend error 500
**Masalah**: Database connection atau dependency error

**Solusi**:
1. Check Railway logs: `railway logs`
2. Pastikan DATABASE_URL sudah set
3. Pastikan spaCy model terinstall di build command
4. Check environment variables lengkap

### File upload tidak work
**Masalah**: Storage di serverless

**Solusi**:
Railway sudah handle file upload dengan `/tmp/uploads`. Jika masih error:
1. Check `UPLOAD_FOLDER` environment variable
2. Pastikan folder permissions OK
3. Consider external storage (AWS S3, Cloudinary) untuk production

---

## 🎯 Quick Deploy Commands

### Deploy Backend (Railway)
```bash
cd backend
railway up
```

### Deploy Frontend (Vercel)
```bash
vercel --prod
```

### View Logs
```bash
# Backend logs
railway logs

# Frontend logs  
vercel logs
```

---

## 💰 Cost Estimate

### Railway (Backend + Database)
- **Free Tier**: $5 credit/month
- **Hobby**: $5/month unlimited

### Vercel (Frontend)
- **Hobby**: Free untuk personal projects
- **Pro**: $20/month jika butuh lebih

**Total**: Bisa **GRATIS** untuk testing, ~$5-10/month untuk production

---

## 🔗 Useful Links

- Railway Dashboard: https://railway.app/dashboard
- Vercel Dashboard: https://vercel.com/dashboard
- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs

---

## 📝 Notes

1. **Database Persistence**: Railway PostgreSQL persistent secara default
2. **Auto Deploy**: Keduanya support auto-deploy dari GitHub
3. **Custom Domain**: Bisa add custom domain di keduanya (gratis)
4. **SSL**: Auto HTTPS di keduanya

---

## 🚀 Next Steps After Deployment

1. Setup custom domain (optional)
2. Configure monitoring & alerts
3. Setup backup schedule untuk database
4. Add error tracking (Sentry)
5. Setup CI/CD dengan GitHub Actions
