# ForecastIQ - Deployment Guide

## 🚀 Free Deployment Options

### Backend Deployment (Render.com - Free Tier)

1. **Create Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   ```
   Name: forecastiq-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Set Environment Variables**
   - Go to "Environment" tab
   - Add:
     - `MONGO_URI` = your MongoDB Atlas connection string
     - `MONGO_DB_NAME` = forecastiq
     - `SECRET_KEY` = generate a secure random string (32+ chars)
     - `ENVIRONMENT` = production

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy the URL (e.g., `https://forecastiq-backend.onrender.com`)

### Frontend Deployment (Vercel - Free Tier)

1. **Update API URL**
   - Create `frontend/.env.production`:
   ```env
   VITE_API_URL=https://your-backend-url.onrender.com/api
   ```

2. **Update axios.js**
   ```javascript
   const api = axios.create({
     baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
   });
   ```

3. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub
   - Click "New Project"
   - Import your repository
   - Configure:
     ```
     Framework Preset: Vite
     Root Directory: frontend
     Build Command: npm run build
     Output Directory: dist
     ```
   - Add Environment Variable:
     - `VITE_API_URL` = your backend URL + /api
   - Click "Deploy"

4. **Update CORS in Backend**
   - Add your Vercel URL to CORS origins in `backend/main.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:5173",
           "https://your-app.vercel.app",  # Add this
       ],
       ...
   )
   ```

### Database (MongoDB Atlas - Free Tier)

1. **Create Cluster**
   - Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Sign up for free
   - Create a free M0 cluster

2. **Configure Access**
   - Database Access → Add User (username/password)
   - Network Access → Add IP Address → Allow Access from Anywhere (0.0.0.0/0)

3. **Get Connection String**
   - Click "Connect" → "Connect your application"
   - Copy connection string
   - Replace `<password>` with your password

## 🔧 Pre-Deployment Checklist

### Backend
- [ ] All dependencies in `requirements.txt`
- [ ] Environment variables configured
- [ ] CORS origins updated with frontend URL
- [ ] MongoDB connection string ready
- [ ] Pre-trained models in `backend/models/` directory
- [ ] `Procfile` exists
- [ ] Test locally: `python main.py`

### Frontend
- [ ] API URL updated in `.env.production`
- [ ] Build succeeds: `npm run build`
- [ ] No console errors
- [ ] All routes work
- [ ] Authentication flow tested

### Database
- [ ] MongoDB Atlas cluster created
- [ ] Database user created
- [ ] IP whitelist configured
- [ ] Connection string tested

## 📦 Build Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run build
npm run preview  # Test production build
```

## 🧪 Testing Deployment

1. **Test Backend**
   ```bash
   curl https://your-backend.onrender.com/api/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123","name":"Test User"}'
   ```

2. **Test Frontend**
   - Visit your Vercel URL
   - Sign up
   - Upload dataset
   - Run forecast
   - Check all features work

## ⚡ Performance Tips

1. **Backend (Render)**
   - Free tier sleeps after 15 min inactivity
   - First request after sleep takes ~30 seconds
   - Consider upgrading to paid tier for production

2. **Frontend (Vercel)**
   - Automatic CDN distribution
   - Edge caching enabled
   - Fast global performance

3. **Database (MongoDB Atlas)**
   - Free tier: 512 MB storage
   - Shared cluster
   - Sufficient for demo/portfolio

## 🔒 Security Checklist

- [ ] Strong SECRET_KEY (32+ random characters)
- [ ] MongoDB user has strong password
- [ ] CORS origins restricted to your domains
- [ ] Environment variables not committed to Git
- [ ] `.env` in `.gitignore`
- [ ] HTTPS enabled (automatic on Render/Vercel)

## 🐛 Troubleshooting

### Backend Issues

**Problem:** 502 Bad Gateway
- Check Render logs
- Verify environment variables
- Check MongoDB connection

**Problem:** Module not found
- Ensure all dependencies in `requirements.txt`
- Check Python version matches `runtime.txt`

### Frontend Issues

**Problem:** API calls fail
- Check CORS configuration
- Verify API URL in environment variables
- Check browser console for errors

**Problem:** Build fails
- Run `npm run build` locally
- Check for TypeScript/ESLint errors
- Verify all dependencies installed

### Database Issues

**Problem:** Connection timeout
- Check IP whitelist (0.0.0.0/0 for all IPs)
- Verify connection string format
- Check database user credentials

## 📊 Monitoring

### Backend Logs (Render)
- Dashboard → Your Service → Logs
- Real-time log streaming
- Error tracking

### Frontend Analytics (Vercel)
- Dashboard → Your Project → Analytics
- Page views, performance metrics
- Error tracking

## 💰 Cost Breakdown

| Service | Free Tier | Limits |
|---------|-----------|--------|
| Render | ✅ Yes | 750 hrs/month, sleeps after 15 min |
| Vercel | ✅ Yes | 100 GB bandwidth, unlimited sites |
| MongoDB Atlas | ✅ Yes | 512 MB storage, shared cluster |

**Total Cost: $0/month** 🎉

## 🔄 Continuous Deployment

Both Render and Vercel support automatic deployments:
- Push to `main` branch → Auto-deploy
- Pull requests → Preview deployments
- Rollback to previous versions

## 📝 Environment Variables Summary

### Backend (.env)
```env
MONGO_URI=mongodb+srv://...
MONGO_DB_NAME=forecastiq
SECRET_KEY=your-secret-key
ENVIRONMENT=production
```

### Frontend (.env.production)
```env
VITE_API_URL=https://your-backend.onrender.com/api
```

## 🎯 Post-Deployment

1. **Test All Features**
   - Authentication (signup/login)
   - Dataset upload
   - Forecast generation
   - Model comparison
   - Insights viewing

2. **Share Your Project**
   - Add URLs to README
   - Update portfolio
   - Share on LinkedIn/Twitter

3. **Monitor Performance**
   - Check logs regularly
   - Monitor error rates
   - Track user feedback

---

**Deployment Time:** ~30 minutes
**Cost:** Free
**Difficulty:** Easy

Good luck with your deployment! 🚀
