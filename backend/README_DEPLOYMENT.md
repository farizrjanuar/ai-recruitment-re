# Backend Deployment Files

This directory contains all necessary files for deploying the AI Recruitment System backend to various platforms.

## Deployment Files Overview

### 1. `Procfile`
- **Purpose**: Heroku/Render deployment configuration
- **Usage**: Automatically detected by Render.com
- **Content**: Defines the web process command using Gunicorn

### 2. `render.yaml`
- **Purpose**: Render.com Blueprint configuration
- **Usage**: One-click deployment on Render
- **Features**:
  - Automatic web service setup
  - PostgreSQL database provisioning
  - Environment variable configuration
  - Health check configuration

### 3. `railway.json`
- **Purpose**: Railway.app deployment configuration
- **Usage**: Automatic deployment on Railway
- **Features**:
  - Build and start commands
  - Health check configuration
  - Restart policy

### 4. `gunicorn_config.py`
- **Purpose**: Gunicorn production server configuration
- **Usage**: Referenced by Gunicorn when starting
- **Features**:
  - Worker process configuration
  - Logging setup
  - Timeout settings
  - Port binding

### 5. `.env.example`
- **Purpose**: Template for environment variables
- **Usage**: Copy to `.env` and fill in values
- **Contains**: All required environment variables with examples

## Quick Start

### Deploy to Render.com

1. Push code to GitHub
2. Connect repository to Render
3. Use Blueprint with `render.yaml`
4. Set environment variables
5. Deploy!

### Deploy to Railway.app

1. Push code to GitHub
2. Connect repository to Railway
3. Railway auto-detects `railway.json`
4. Add PostgreSQL database
5. Deploy!

## Environment Variables Required

```bash
FLASK_ENV=production
SECRET_KEY=<generate-random-key>
JWT_SECRET_KEY=<generate-random-key>
DATABASE_URL=<provided-by-platform>
MAX_FILE_SIZE=5242880
UPLOAD_FOLDER=/tmp/uploads
CORS_ORIGINS=https://your-frontend.vercel.app
```

## Generate Secret Keys

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Health Check Endpoint

The application includes a health check endpoint at `/health` that returns:

```json
{
  "status": "healthy",
  "message": "AI Recruitment System API is running"
}
```

This is used by hosting platforms to monitor service health.

## Production Server

The application uses **Gunicorn** as the production WSGI server:

- **Workers**: 2 (configurable via `GUNICORN_WORKERS` env var)
- **Timeout**: 120 seconds
- **Binding**: `0.0.0.0:$PORT`

## Database

- **Development**: SQLite (`sqlite:///recruitment.db`)
- **Production**: PostgreSQL (provided by Render/Railway)

The application automatically creates tables on first run.

## File Storage

- **Development**: Local `uploads/` directory
- **Production**: `/tmp/uploads` (ephemeral storage)

Note: Uploaded CVs are processed and then data is stored in database. Original files can be deleted after processing.

## Monitoring

### Render.com
- View logs: Dashboard → Service → Logs
- View metrics: Dashboard → Service → Metrics

### Railway.app
- View logs: Dashboard → Service → Deployments → Logs
- Monitor usage: Dashboard → Usage

## Troubleshooting

### Service won't start
- Check build logs for errors
- Verify all dependencies installed
- Ensure spaCy model downloaded

### Database connection fails
- Verify `DATABASE_URL` is set
- Check database is running
- Ensure `psycopg2-binary` installed

### spaCy model not found
- Ensure build command includes: `python -m spacy download en_core_web_sm`
- Check build logs

### CORS errors
- Update `CORS_ORIGINS` with frontend URL
- Restart service after updating

## Support

For detailed deployment instructions, see:
- [DEPLOYMENT.md](../DEPLOYMENT.md) - Complete deployment guide
- [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) - Deployment checklist

## Platform Documentation

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Gunicorn Docs](https://docs.gunicorn.org)
