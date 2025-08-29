# 🐳 Docker Deployment Guide

## Quick Start

1. **Setup Environment**
   ```bash
   cp docker.env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

2. **Build and Run**
   ```bash
   docker-compose up --build
   ```

3. **Access Application**
   - **Main App**: http://localhost
   - **API Health**: http://localhost/health
   - **API Metrics**: http://localhost/metrics
   - **Direct Backend**: http://localhost:5001 (if needed)

## Architecture

```
[User Browser] → [Nginx:80] → [React App (Static Files)]
                      ↓
                [Flask API:5001] → [Gemini API]
```

## Commands

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Shell into containers
docker-compose exec backend bash
docker-compose exec frontend sh
```

## Services

- **frontend**: React app served by Nginx on port 80
- **backend**: Flask API on port 5001
- **Logs**: Persisted in `./backend/logs/`

## Production Notes

- Frontend is optimized production build
- Gzip compression enabled
- Health checks configured
- Log persistence via volumes
- Automatic restart policies
