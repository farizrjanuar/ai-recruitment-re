# Deployment Guide - AI Recruitment System

This guide provides step-by-step instructions for deploying the AI Recruitment System to production using free hosting services.

## Table of Contents

1. [Backend Deployment (Render.com)](#backend-deployment-rendercom)
2. [Backend Deployment (Railway.app)](#backend-deployment-railwayapp)
3. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
4. [Environment Variables Setup](#environment-variables-setup)
5. [Post-Deployment Configuration](#post-deployment-configuration)
6. [Troubleshooting](#troubleshooting)

---

## Backend Deployment (Render.com)

Render.com offers a free tier with 750 hours/month, perfect for this application.

### Prerequisites

- GitHub account
- Render.com account (sign up at https://render.com)
- Your code pushed to a GitHub repository

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### Step 2: Deploy Backend

#### Option A: Using render.yaml (Recommended)

1. Ensure `render.yaml` exists in your `backend/` directory
2. Go to Render Dashboard
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml`
6. Click "Apply" to create services

#### Option B: Manual Setup

1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `ai-recruitment-backend`
   - **Region**: Oregon (or closest to you)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python -m spacy download en_core_web_sm
     ```
   - **Start Command**: 
     ```bash
     gunicorn app:app
     ```
   - **Plan**: Free

5. Click "Advanced" and add environment variables (see [Environment Variables](#backend-environment-variables))

6. Click "Create Web Service"

### Step 3: Create PostgreSQL Database

1. In Render Dashboard, click "New +" → "PostgreSQL"
2. Configure:
   - **Name**: `ai-recruitment-db`
   - **Database**: `recruitment`
   - **User**: `recruitment_user`
   - **Region**: Same as web service
   - **Plan**: Free

3. Click "Create Database"

4. Copy the "Internal Database URL" from the database info page

5. Go back to your web service → "Environment"

6. Add/Update environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL

7. Save changes (service will redeploy automatically)

### Step 4: Verify Deployment

1. Wait for deployment to complete (5-10 minutes)
2. Click on your service URL (e.g., `https://ai-recruitment-backend.onrender.com`)
3. You should see: `{"name": "AI Recruitment System API", "version": "1.0.0", "status": "active"}`
4. Test health check: `https://your-service.onrender.com/health`

### Important Notes for Render Free Tier

- **Cold Starts**: Service sleeps after 15 minutes of inactivity. First request after sleep takes ~30 seconds.
- **Database Expiry**: Free PostgreSQL expires after 90 days. Backup your data regularly.
- **Hours Limit**: 750 hours/month (enough for 1 service running 24/7)

---

## Backend Deployment (Railway.app)

Railway offers $5 free credit per month with no sleep time.

### Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign up with your GitHub account
3. Authorize Railway to access your repositories

### Step 2: Deploy Backend

#### Option A: Using railway.json (Recommended)

1. Ensure `railway.json` exists in your `backend/` directory
2. Go to Railway Dashboard
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will detect `railway.json` and configure automatically
6. Click "Deploy"

#### Option B: Manual Setup

1. Go to Railway Dashboard
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and create a service
5. Click on the service to configure:
   - **Root Directory**: `backend`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python -m spacy download en_core_web_sm
     ```
   - **Start Command**: 
     ```bash
     gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
     ```

6. Add environment variables (see [Environment Variables](#backend-environment-variables))

### Step 3: Add PostgreSQL Database

1. In your project, click "New" → "Database" → "Add PostgreSQL"
2. Railway automatically creates a database and sets `DATABASE_URL`
3. No additional configuration needed!

### Step 4: Verify Deployment

1. Click "Settings" → "Generate Domain" to get a public URL
2. Visit your URL (e.g., `https://your-app.up.railway.app`)
3. You should see the API welcome message
4. Test health check: `https://your-app.up.railway.app/health`

### Important Notes for Railway Free Tier

- **Credit Limit**: $5/month free credit
- **No Sleep**: Service runs continuously (no cold starts)
- **Usage Monitoring**: Monitor usage in dashboard to stay within free tier
- **Execution Time**: Limit: 500 hours/month

---

## Frontend Deployment (Vercel)

Vercel offers unlimited deployments and 100GB bandwidth/month for free.

### Prerequisites

- GitHub account
- Vercel account (sign up at https://vercel.com)
- Backend deployed and URL available

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Sign up with your GitHub account
3. Authorize Vercel to access your repositories

### Step 2: Deploy Frontend

1. Go to Vercel Dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Create React App (auto-detected)
   - **Root Directory**: `./` (leave as root)
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `build` (auto-detected)

5. Add environment variable:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: Your backend URL (e.g., `https://ai-recruitment-backend.onrender.com` or `https://your-app.up.railway.app`)

6. Click "Deploy"

### Step 3: Verify Deployment

1. Wait for deployment to complete (2-3 minutes)
2. Vercel will provide a URL (e.g., `https://your-app.vercel.app`)
3. Visit the URL and test the application
4. Try logging in and uploading a CV

### Step 4: Configure Custom Domain (Optional)

1. In Vercel project settings, go to "Domains"
2. Add your custom domain
3. Follow DNS configuration instructions
4. Vercel provides automatic HTTPS

### Important Notes for Vercel Free Tier

- **Unlimited Deployments**: No limit on number of deployments
- **Bandwidth**: 100GB/month
- **Build Time**: 100 hours/month
- **Automatic HTTPS**: SSL certificates included

---

## Environment Variables Setup

### Backend Environment Variables

Required environment variables for backend deployment:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `FLASK_ENV` | Flask environment | `production` |
| `SECRET_KEY` | Flask secret key (generate random) | `your-random-secret-key-here` |
| `JWT_SECRET_KEY` | JWT signing key (generate random) | `your-jwt-secret-key-here` |
| `DATABASE_URL` | PostgreSQL connection string | Auto-provided by Render/Railway |
| `MAX_FILE_SIZE` | Max upload size in bytes | `5242880` (5MB) |
| `UPLOAD_FOLDER` | Upload directory | `/tmp/uploads` |
| `CORS_ORIGINS` | Allowed frontend origins | `https://your-app.vercel.app` |
| `PORT` | Server port | Auto-provided by platform |

#### Generating Secret Keys

Use Python to generate secure random keys:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Run this twice to generate both `SECRET_KEY` and `JWT_SECRET_KEY`.

### Frontend Environment Variables

Required environment variables for frontend deployment:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `REACT_APP_API_URL` | Backend API URL | `https://ai-recruitment-backend.onrender.com` |

---

## Post-Deployment Configuration

### 1. Update CORS Origins

After deploying frontend, update backend CORS settings:

1. Go to your backend service (Render/Railway)
2. Update `CORS_ORIGINS` environment variable with your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
   ```
3. Save and redeploy

### 2. Create Admin User

After first deployment, create an admin user:

1. Access your backend service shell/console (if available)
2. Or create a temporary script to add admin user
3. Or use the `/api/auth/register` endpoint with role "Admin"

### 3. Test Complete Workflow

1. Visit your frontend URL
2. Register a new account
3. Log in
4. Upload a sample CV
5. Create a job position
6. Check matching results
7. View dashboard analytics

### 4. Monitor Application

**Render:**
- View logs in Render Dashboard → Your Service → Logs
- Monitor metrics in Metrics tab

**Railway:**
- View logs in Railway Dashboard → Your Service → Deployments → Logs
- Monitor usage in Usage tab

**Vercel:**
- View deployment logs in Vercel Dashboard → Your Project → Deployments
- Monitor analytics in Analytics tab

---

## Troubleshooting

### Backend Issues

#### Issue: Service won't start

**Symptoms**: Deployment fails or service crashes immediately

**Solutions**:
1. Check build logs for errors
2. Verify all dependencies in `requirements.txt`
3. Ensure spaCy model downloads successfully:
   ```bash
   python -m spacy download en_core_web_sm
   ```
4. Check environment variables are set correctly
5. Verify `DATABASE_URL` is properly formatted

#### Issue: Database connection fails

**Symptoms**: 500 errors, "database connection" errors in logs

**Solutions**:
1. Verify `DATABASE_URL` environment variable is set
2. Check database is running (Render/Railway dashboard)
3. Ensure `psycopg2-binary` is in `requirements.txt`
4. For Render: Use "Internal Database URL" not "External"
5. Check database credentials are correct

#### Issue: Cold start takes too long (Render)

**Symptoms**: First request after inactivity times out

**Solutions**:
1. This is expected behavior on Render free tier
2. Consider upgrading to paid tier for always-on service
3. Or switch to Railway (no sleep on free tier)
4. Implement a ping service to keep it warm (not recommended for free tier)

#### Issue: spaCy model not found

**Symptoms**: "Can't find model 'en_core_web_sm'" error

**Solutions**:
1. Ensure build command includes:
   ```bash
   python -m spacy download en_core_web_sm
   ```
2. Check build logs to verify model downloaded
3. Try adding to `requirements.txt`:
   ```
   https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
   ```

#### Issue: File upload fails

**Symptoms**: 500 error when uploading CV

**Solutions**:
1. Verify `UPLOAD_FOLDER` is set to `/tmp/uploads`
2. Check `MAX_FILE_SIZE` is set correctly
3. Ensure file size is under 5MB
4. Check file format is PDF, DOCX, or TXT
5. Review backend logs for specific error

#### Issue: CORS errors

**Symptoms**: "CORS policy" errors in browser console

**Solutions**:
1. Verify `CORS_ORIGINS` includes your Vercel URL
2. Ensure no trailing slash in URLs
3. Check both HTTP and HTTPS if testing locally
4. Restart backend service after updating CORS settings

### Frontend Issues

#### Issue: API calls fail

**Symptoms**: Network errors, 404 errors

**Solutions**:
1. Verify `REACT_APP_API_URL` is set correctly
2. Ensure backend URL has no trailing slash
3. Check backend is running and accessible
4. Test backend health endpoint directly
5. Check browser console for specific errors

#### Issue: Build fails on Vercel

**Symptoms**: Deployment fails during build

**Solutions**:
1. Check build logs in Vercel dashboard
2. Verify all dependencies in `package.json`
3. Test build locally: `npm run build`
4. Check for TypeScript errors if using TS
5. Ensure no environment-specific code in build

#### Issue: Environment variables not working

**Symptoms**: API URL is undefined or incorrect

**Solutions**:
1. Verify variable name starts with `REACT_APP_`
2. Redeploy after adding environment variables
3. Check variable is set in Vercel project settings
4. Clear cache and redeploy
5. Check variable value has no quotes or extra spaces

#### Issue: Routing doesn't work (404 on refresh)

**Symptoms**: Page refresh returns 404

**Solutions**:
1. Verify `vercel.json` exists with rewrites configuration
2. Ensure rewrites section includes:
   ```json
   "rewrites": [{"source": "/(.*)", "destination": "/index.html"}]
   ```
3. Redeploy after adding `vercel.json`

### Database Issues

#### Issue: Database expires (Render)

**Symptoms**: Database stops working after 90 days

**Solutions**:
1. Render free PostgreSQL expires after 90 days
2. Backup data before expiry
3. Create new database and restore data
4. Or upgrade to paid tier for persistent database
5. Or switch to Railway (no expiry on free tier)

#### Issue: Database connection limit reached

**Symptoms**: "too many connections" error

**Solutions**:
1. Reduce number of Gunicorn workers
2. Implement connection pooling
3. Close database connections properly
4. Check for connection leaks in code
5. Upgrade to paid tier for more connections

### Performance Issues

#### Issue: Slow CV processing

**Symptoms**: Upload takes longer than 10 seconds

**Solutions**:
1. Check file size (should be under 5MB)
2. Verify spaCy model is loaded correctly
3. Check server resources (RAM, CPU)
4. Consider upgrading to paid tier for more resources
5. Optimize ML processing code

#### Issue: High memory usage

**Symptoms**: Service crashes with out-of-memory errors

**Solutions**:
1. Reduce number of Gunicorn workers
2. Use smaller spaCy model (en_core_web_sm)
3. Implement lazy loading for ML models
4. Clear temporary files after processing
5. Upgrade to paid tier for more RAM

---

## Monitoring and Maintenance

### Regular Tasks

1. **Monitor Usage** (Weekly)
   - Check Render/Railway credit usage
   - Monitor Vercel bandwidth usage
   - Review error logs

2. **Backup Database** (Weekly)
   - Export database to local backup
   - Store backups securely
   - Test restore process

3. **Update Dependencies** (Monthly)
   - Check for security updates
   - Update Python packages
   - Update npm packages
   - Test thoroughly before deploying

4. **Clean Up Data** (Monthly)
   - Delete old CV files
   - Archive old candidates
   - Clean up test data

### Scaling Considerations

When you outgrow free tier:

1. **Backend**: Upgrade Render/Railway to paid tier
   - More RAM and CPU
   - No sleep time (Render)
   - More database storage
   - Better performance

2. **Frontend**: Vercel free tier is usually sufficient
   - Upgrade if you exceed 100GB bandwidth
   - Or need advanced features

3. **Database**: Consider managed PostgreSQL
   - AWS RDS
   - Google Cloud SQL
   - DigitalOcean Managed Databases

---

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Vercel Documentation](https://vercel.com/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org)

---

## Support

If you encounter issues not covered in this guide:

1. Check application logs in your hosting dashboard
2. Review GitHub issues for similar problems
3. Consult hosting platform documentation
4. Contact support (Render, Railway, Vercel all have free support)

---

**Last Updated**: November 2025
