# 🎯 Checklist Persiapan Deploy ke Render

## ✅ Yang Sudah Siap:
- [x] `render.yaml` configuration file
- [x] `requirements.txt` dengan gunicorn & psycopg2-binary
- [x] Flask app dengan health check endpoint
- [x] Database models siap untuk PostgreSQL

## 📋 Yang Perlu Disiapkan Sekarang:

### 1️⃣ Akun & Setup Awal

**Yang Anda Butuhkan:**
- ✅ Akun GitHub (sudah ada)
- 📧 Email untuk sign up Render (GRATIS, no credit card)
- 🔗 Repository sudah di GitHub

---

## 🚀 Langkah-langkah Persiapan

### Step 1: Commit & Push Code ke GitHub

```bash
cd /Users/farizrjanuar/Comproj/ai-recruitment-re

# Add semua file baru
git add .

# Commit dengan pesan jelas
git commit -m "Add deployment configs for Render"

# Push ke GitHub
git push origin master
```

### Step 2: Pastikan File Penting Ada

Cek apakah file ini ada di project:
- ✅ `/backend/render.yaml` - Konfigurasi deployment
- ✅ `/backend/requirements.txt` - Python dependencies
- ✅ `/backend/app.py` - Flask application
- ✅ `/backend/Procfile` - Gunicorn command (optional, render.yaml lebih prioritas)

### Step 3: Siapkan Informasi Ini

Anda akan diminta input saat deploy:

1. **Repository GitHub**: `farizrjanuar/ai-recruitment-re`
2. **Branch**: `master`
3. **Root Directory**: Kosongkan (render.yaml sudah handle)

---

## 🔐 Environment Variables yang Akan Di-Generate Otomatis

Render akan auto-generate dari `render.yaml`:
- ✅ `SECRET_KEY` - Random secure key
- ✅ `JWT_SECRET_KEY` - Random JWT key
- ✅ `DATABASE_URL` - Connection string dari PostgreSQL
- ✅ `FLASK_ENV` - production
- ✅ `MAX_FILE_SIZE` - 5242880 (5MB)
- ✅ `UPLOAD_FOLDER` - /tmp/uploads

**Yang Perlu Anda Set Manual Nanti:**
- `CORS_ORIGINS` - Setelah frontend deployed

---

## 📝 Langkah Deploy di Render.com

### 1. Sign Up Render
1. Buka https://render.com
2. Klik "Get Started for Free"
3. Sign up dengan GitHub (recommended)
4. Authorize Render to access GitHub

### 2. Deploy via Blueprint
1. Klik "New +" → "Blueprint"
2. Connect repository: `ai-recruitment-re`
3. Render akan detect `render.yaml` ✅
4. Review config (sudah benar)
5. Klik "Apply"

### 3. Tunggu Build
- Backend build: ~8-15 menit (download spaCy model)
- Database provision: ~2-3 menit
- Total: ~15-20 menit untuk pertama kali

### 4. Get Backend URL
Setelah deploy sukses:
1. Dashboard → Services → `ai-recruitment-backend`
2. Copy URL (contoh: `https://ai-recruitment-backend.onrender.com`)
3. Test: `https://your-url/health`

---

## 🎨 Deploy Frontend ke Vercel

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Login & Deploy
```bash
cd /Users/farizrjanuar/Comproj/ai-recruitment-re

# Login
vercel login

# Deploy
vercel
```

### 3. Set Environment Variable
```bash
# Add API URL
vercel env add REACT_APP_API_URL production
# Paste: https://your-backend-url.onrender.com

# Redeploy
vercel --prod
```

### 4. Get Frontend URL
Copy URL Vercel (contoh: `https://ai-recruitment.vercel.app`)

---

## 🔄 Update CORS di Render

1. Render Dashboard → `ai-recruitment-backend`
2. Environment tab
3. Edit `CORS_ORIGINS`
4. Value: `https://your-vercel-url.vercel.app,http://localhost:3000`
5. Save (auto redeploy)

---

## ✅ Testing Checklist

Setelah deploy, test semua fitur:

### Backend Health Check
```bash
curl https://your-backend-url.onrender.com/health
```
Expected:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Frontend Testing
1. ✅ Buka frontend URL di browser
2. ✅ Register akun baru
3. ✅ Login
4. ✅ Upload CV (test file upload)
5. ✅ Create Job Position
6. ✅ View matching results
7. ✅ Delete operations

---

## 🐛 Common Issues & Solutions

### Issue 1: Build Failed - spaCy Download Error
**Solution**: Render akan retry otomatis, tunggu 2-3 menit

### Issue 2: Database Connection Error
**Solution**: 
- Check DATABASE_URL di environment variables
- Pastikan PostgreSQL service running

### Issue 3: CORS Error di Frontend
**Solution**:
- Update CORS_ORIGINS dengan URL Vercel yang benar
- Format: `https://exact-url.vercel.app` (no trailing slash)

### Issue 4: Backend Sleep (Free Tier)
**Solution**:
- Normal untuk free tier (sleep after 15 min)
- Wake up time: ~30 seconds
- Setup UptimeRobot untuk keep alive (optional)

---

## 📊 Expected Timeline

| Step | Time |
|------|------|
| Commit & Push | 2 min |
| Sign up Render | 3 min |
| Deploy Backend (first time) | 15-20 min |
| Deploy Frontend | 3-5 min |
| Update CORS | 2 min |
| Testing | 5-10 min |
| **TOTAL** | **30-40 min** |

---

## 🎯 Ready to Deploy?

Anda siap deploy jika:
- ✅ Code sudah di-commit & push ke GitHub
- ✅ Akun Render sudah dibuat
- ✅ Akun Vercel sudah dibuat
- ✅ Punya waktu 30-40 menit

---

## 🆘 Need Help?

Jika stuck di step manapun:
1. Check Render logs: Dashboard → Service → Logs
2. Check browser console untuk frontend errors
3. Test backend endpoint dengan `curl` atau Postman

---

## 📝 Quick Commands Summary

```bash
# 1. Commit & Push
git add .
git commit -m "Add deployment configs"
git push origin master

# 2. Deploy Frontend
vercel login
vercel
vercel env add REACT_APP_API_URL production
vercel --prod

# 3. Test Backend
curl https://your-backend-url.onrender.com/health

# 4. View Logs (if issues)
# Check Render dashboard logs
```

---

**🎉 Siap mulai deploy? Ketik "ya" jika semua checklist sudah ✅**
