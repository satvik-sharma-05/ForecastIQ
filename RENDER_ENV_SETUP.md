# 🔧 Render Environment Variables Setup

## ⚠️ CRITICAL: Set These Environment Variables in Render

Your backend needs these environment variables to work. Follow these steps:

### Step 1: Go to Render Dashboard
1. Visit https://dashboard.render.com
2. Click on your `forecastiq-backend` service
3. Go to **Environment** tab in the left sidebar

### Step 2: Add Environment Variables

Add these 4 variables:

#### 1. MONGO_URI
**Key:** `MONGO_URI`  
**Value:** Your MongoDB connection string  
Example: `mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0`

#### 2. MONGO_DB_NAME
**Key:** `MONGO_DB_NAME`  
**Value:** `forecastiq`

#### 3. SECRET_KEY
**Key:** `SECRET_KEY`  
**Value:** A secure random string (min 32 characters)  
Example: `your-super-secret-jwt-key-min-32-chars-long-12345678`

#### 4. ENVIRONMENT
**Key:** `ENVIRONMENT`  
**Value:** `production`

### Step 3: Save and Redeploy

1. Click **Save Changes**
2. Render will automatically redeploy your service
3. Wait 2-3 minutes for deployment to complete

---

## How to Get MongoDB URI

If you don't have MongoDB Atlas set up:

1. Go to https://cloud.mongodb.com
2. Sign up / Log in
3. Create a free M0 cluster
4. Click **Connect** → **Connect your application**
5. Copy the connection string
6. Replace `<password>` with your database password
7. Use this as your `MONGO_URI`

---

## Generate Secure SECRET_KEY

Run this in your terminal:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Or use this online: https://generate-secret.vercel.app/32

---

## Current Error

The backend is crashing because:
```
AttributeError: 'Settings' object has no attribute 'ACCESS_TOKEN_EXPIRE_MINUTES'
```

This happens when environment variables are not set in Render.

---

## After Setting Variables

Once you set all 4 environment variables:
- ✅ Backend will start successfully
- ✅ MongoDB will connect
- ✅ JWT authentication will work
- ✅ Login/Signup will work
- ✅ All API endpoints will work

---

## Verify Setup

After deployment completes:

1. Check Render logs - should see:
   ```
   ✅ Connected to MongoDB
   ✅ Loaded Linear Regression model
   ✅ Loaded Random Forest model
   ```

2. Visit https://forecastiq-backend.onrender.com/docs
   - Should see API documentation (not 404)

3. Try login at https://forecast-iq-theta.vercel.app
   - Should work without errors

---

## Quick Checklist

- [ ] Set MONGO_URI in Render
- [ ] Set MONGO_DB_NAME in Render
- [ ] Set SECRET_KEY in Render
- [ ] Set ENVIRONMENT in Render
- [ ] Save changes
- [ ] Wait for auto-redeploy (2-3 min)
- [ ] Check logs for success messages
- [ ] Test login on frontend

---

## Need Help?

If you don't have MongoDB credentials:
1. I can help you set up MongoDB Atlas
2. Or you can use a local MongoDB for testing

If you need a SECRET_KEY:
1. Use the Python command above
2. Or just use: `my-super-secret-jwt-key-for-forecastiq-production-2024`
