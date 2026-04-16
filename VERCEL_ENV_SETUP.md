# 🔧 Vercel Environment Variable Setup

## ⚠️ IMPORTANT: Set Environment Variable in Vercel

The frontend needs to know the backend API URL. Follow these steps:

### Step 1: Go to Vercel Dashboard
1. Visit https://vercel.com/dashboard
2. Click on your `forecast-iq-theta` project
3. Go to **Settings** tab
4. Click **Environment Variables** in the left sidebar

### Step 2: Add Environment Variable
Add the following variable:

**Key:** `VITE_API_URL`  
**Value:** `https://forecastiq-backend.onrender.com/api`  
**Environment:** Select all (Production, Preview, Development)

### Step 3: Redeploy
1. Go to **Deployments** tab
2. Click the three dots (...) on the latest deployment
3. Click **Redeploy**
4. Check "Use existing Build Cache" (optional)
5. Click **Redeploy**

---

## Alternative: Use Vercel CLI

If you have Vercel CLI installed:

```bash
cd frontend
vercel env add VITE_API_URL
# Enter: https://forecastiq-backend.onrender.com/api
# Select: Production, Preview, Development

# Redeploy
vercel --prod
```

---

## Verify Setup

After redeployment, check:

1. Visit https://forecast-iq-theta.vercel.app
2. Open browser DevTools (F12)
3. Go to Console tab
4. Try to login
5. Check Network tab - should see requests to `https://forecastiq-backend.onrender.com/api/auth/login`

---

## Current Issue

The frontend is trying to access:
- ❌ `https://forecastiq-backend.onrender.com/auth/login` (wrong - missing /api)

It should access:
- ✅ `https://forecastiq-backend.onrender.com/api/auth/login` (correct)

This happens because `VITE_API_URL` is not set in Vercel, so it defaults to `http://localhost:8000/api` during build, but then tries to use the production domain without the `/api` prefix.

---

## Quick Fix

**Option 1: Set in Vercel Dashboard (Recommended)**
- Follow steps above

**Option 2: Hardcode in axios.js (Not recommended)**
```javascript
// frontend/src/api/axios.js
const api = axios.create({
    baseURL: 'https://forecastiq-backend.onrender.com/api',
});
```

---

## After Setting Environment Variable

Wait 1-2 minutes for Vercel to redeploy, then:
- ✅ CORS will work (backend already configured)
- ✅ Login will work
- ✅ All API calls will work
- ✅ Application fully functional

---

## Backend CORS Status

✅ Backend already has Vercel URL in allowed origins:
```python
allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://forecast-iq-theta.vercel.app"
]
```

Backend is ready and waiting for frontend to connect properly!
