# Deployment Checklist

Use this checklist to ensure smooth deployment of the AI Recruitment System.

## Pre-Deployment

### Backend Preparation

- [ ] All code committed and pushed to GitHub
- [ ] `requirements.txt` includes all dependencies (including `gunicorn` and `psycopg2-binary`)
- [ ] `render.yaml` or `railway.json` configured
- [ ] `Procfile` created for Render
- [ ] `.env.example` updated with all required variables
- [ ] Health check endpoint (`/health`) working locally
- [ ] spaCy model downloads successfully
- [ ] Database migrations tested locally

### Frontend Preparation

- [ ] All code committed and pushed to GitHub
- [ ] `vercel.json` configured
- [ ] `.env.example` created with `REACT_APP_API_URL`
- [ ] Build succeeds locally (`npm run build`)
- [ ] No hardcoded API URLs in code
- [ ] All routes work with React Router

## Backend Deployment

### Render.com

- [ ] Render account created
- [ ] GitHub repository connected
- [ ] Web service created (or Blueprint applied)
- [ ] PostgreSQL database created
- [ ] Environment variables configured:
  - [ ] `FLASK_ENV=production`
  - [ ] `SECRET_KEY` (generated)
  - [ ] `JWT_SECRET_KEY` (generated)
  - [ ] `DATABASE_URL` (from database)
  - [ ] `MAX_FILE_SIZE=5242880`
  - [ ] `UPLOAD_FOLDER=/tmp/uploads`
  - [ ] `CORS_ORIGINS` (will update after frontend deployment)
- [ ] Build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- [ ] Start command: `gunicorn app:app`
- [ ] Service deployed successfully
- [ ] Health check endpoint accessible
- [ ] API root endpoint returns correct response

### Railway.app (Alternative)

- [ ] Railway account created
- [ ] GitHub repository connected
- [ ] Service created
- [ ] PostgreSQL database added
- [ ] Environment variables configured (same as Render)
- [ ] Build and start commands configured
- [ ] Domain generated
- [ ] Service deployed successfully
- [ ] Health check endpoint accessible

## Frontend Deployment

### Vercel

- [ ] Vercel account created
- [ ] GitHub repository connected
- [ ] Project imported
- [ ] Framework preset: Create React App
- [ ] Environment variable configured:
  - [ ] `REACT_APP_API_URL` (backend URL from Render/Railway)
- [ ] Deployment successful
- [ ] Application loads correctly
- [ ] All routes accessible

## Post-Deployment

### Backend Configuration

- [ ] Update `CORS_ORIGINS` with Vercel URL
- [ ] Redeploy backend service
- [ ] Test CORS by making API call from frontend
- [ ] Verify database connection
- [ ] Check logs for errors

### Frontend Configuration

- [ ] Test login functionality
- [ ] Test CV upload
- [ ] Test job creation
- [ ] Test matching functionality
- [ ] Test dashboard
- [ ] Check browser console for errors

### Testing

- [ ] Register new user account
- [ ] Login with credentials
- [ ] Upload sample CV (PDF)
- [ ] Upload sample CV (DOCX)
- [ ] Create job position
- [ ] Calculate matches
- [ ] View candidate details
- [ ] View job details
- [ ] Check dashboard statistics
- [ ] Test on mobile device
- [ ] Test on different browsers

### Monitoring Setup

- [ ] Check backend logs (Render/Railway)
- [ ] Check frontend logs (Vercel)
- [ ] Monitor database usage
- [ ] Set up error tracking (optional)
- [ ] Document deployment URLs

## URLs to Document

```
Backend URL: ___________________________________
Frontend URL: ___________________________________
Database URL: ___________________________________
Admin Email: ___________________________________
```

## Common Issues Checklist

If something doesn't work:

- [ ] Check all environment variables are set
- [ ] Verify CORS_ORIGINS includes frontend URL
- [ ] Check backend logs for errors
- [ ] Verify database connection
- [ ] Test health endpoint directly
- [ ] Clear browser cache
- [ ] Check API URL in frontend has no trailing slash
- [ ] Verify spaCy model downloaded successfully
- [ ] Check file upload folder permissions

## Rollback Plan

If deployment fails:

1. [ ] Revert to previous GitHub commit
2. [ ] Redeploy from Render/Railway/Vercel dashboard
3. [ ] Check logs for specific errors
4. [ ] Fix issues locally and test
5. [ ] Commit and push fixes
6. [ ] Redeploy

## Success Criteria

Deployment is successful when:

- [ ] Backend health endpoint returns 200 OK
- [ ] Frontend loads without errors
- [ ] User can register and login
- [ ] CV upload and parsing works
- [ ] Job creation works
- [ ] Matching calculation works
- [ ] Dashboard displays data
- [ ] No CORS errors in browser console
- [ ] No 500 errors in backend logs

---

**Deployment Date**: _______________
**Deployed By**: _______________
**Notes**: _______________________________________________
