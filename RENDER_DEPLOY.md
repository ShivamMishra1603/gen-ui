# Deploy GenUI to Render

This guide will help you deploy GenUI to Render in just a few simple steps!

## Prerequisites

1. **GitHub Account** with your GenUI code pushed
2. **Render Account** (free at [render.com](https://render.com))
3. **Google AI API Key** ([Get one here](https://makersuite.google.com/app/apikey))

## 🚀 Simple Deployment Steps

### Option 1: One-Click Deploy (Recommended)

1. **Push your code to GitHub** (if not already done)
2. **Go to Render** and sign in
3. **Create New Web Service**:
   - Connect your GitHub repository
   - Select the backend folder: `backend`
   - Render will automatically detect Python and use our settings

### Option 2: Manual Setup

#### Step 1: Deploy Backend

1. In Render Dashboard, click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `genui-backend`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. **Add Environment Variables**:
   - `GOOGLE_API_KEY`: Your actual Google AI API key
   - `FLASK_ENV`: `production`
   - `UI_GENERATION_PROMPT`: (Use the default from env_example.txt)

5. Click **"Create Web Service"**

#### Step 2: Deploy Frontend

1. Create another **"Static Site"**
2. Configure:
   - **Name**: `genui-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`

3. **Add Environment Variable**:
   - `REACT_APP_API_URL`: `https://YOUR-BACKEND-URL.onrender.com`
   - (Replace with your actual backend URL from Step 1)

4. Click **"Create Static Site"**

## 🎉 That's It!

Your GenUI app will be live at:
- **Frontend**: `https://YOUR-FRONTEND-URL.onrender.com`
- **Backend API**: `https://YOUR-BACKEND-URL.onrender.com`

## 🔧 Configuration Notes

### Backend Environment Variables
```
GOOGLE_API_KEY=your_actual_api_key_here
FLASK_ENV=production
UI_GENERATION_PROMPT=You are an expert front-end web developer...
```

### Frontend Environment Variables
```
REACT_APP_API_URL=https://your-backend-url.onrender.com
```

## 🚨 Important Notes

1. **Free Tier**: Render free tier services sleep after 15 minutes of inactivity
2. **Cold Starts**: First request after sleep takes ~30 seconds to wake up
3. **API Key**: Keep your Google AI API key secure in environment variables
4. **CORS**: Already configured in the backend for cross-origin requests

## 🛠️ Troubleshooting

**Build Failures:**
- Check the build logs in Render dashboard
- Ensure all environment variables are set correctly

**API Errors:**
- Verify your Google AI API key is valid
- Check backend logs for detailed error messages

**Frontend can't reach backend:**
- Verify `REACT_APP_API_URL` points to your backend service
- Ensure both services are deployed and running

## 📊 Monitoring

Your app includes built-in endpoints:
- **Health Check**: `https://your-backend.onrender.com/health`
- **Metrics**: `https://your-backend.onrender.com/metrics`

---

**🎯 Pro Tip**: For production use, consider upgrading to Render's paid tier for always-on services and better performance!
