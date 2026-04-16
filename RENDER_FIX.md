# 🔧 Render Deployment Fix

## Problem
Render can't find `requirements.txt` because it's in the `backend/` folder.

## ✅ Solution (Choose One)

### Option 1: Set Root Directory (Recommended)

1. Go to Render Dashboard: https://dashboard.render.com
2. Select your service: **forecastiq-backend**
3. Go to **Settings** tab
4. Find **Root Directory** section
5. Click **"Edit"**
6. Enter: `backend`
7. Click **"Save Changes"**
8. Render will automatically redeploy

**Build Command:** `pip install -r requirements.txt`
**Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Option 2: Use Root-Level Files (Already Done)

I've created root-level files that redirect to backend:
- ✅ `Procfile` - Points to backend
- ✅ `requirements.txt` - Includes backend/requirements.txt
- ✅ `runtime.txt` - Python version

Now push these changes:

```bash
git add .
git commit -m "Fix: Add root-level deployment files for Render"
git push
```

Render will auto-deploy with the new files.

## 🚀 After Fix

Your deployment should succeed and you'll see:
```
✅ Build succeeded
✅ Deploy live at https://forecastiq-backend.onrender.com
```

## ⚠️ Important: Upload Pre-trained Models

After deployment succeeds, you need to upload the pre-trained models:

### Method 1: Train on Render (Recommended)

1. Go to Render Dashboard
2. Click **Shell** tab
3. Run:
```bash
cd /opt/render/project/src
pip install -r training_requirements.txt
python train_models.py
```

### Method 2: Upload Manually

1. Train models locally:
```bash
python train_models.py
```

2. Upload `backend/models/*.pkl` files to Render using Shell or SFTP

## 🧪 Test Deployment

After deployment succeeds:

1. Visit: https://forecastiq-backend.onrender.com/docs
2. Test signup endpoint
3. Test login endpoint

## 📝 Environment Variables

Make sure these are set in Render:

- `MONGO_URI` - Your MongoDB connection string
- `MONGO_DB_NAME` - forecastiq
- `SECRET_KEY` - Your secret key (32+ characters)
- `ENVIRONMENT` - production

## 🔄 Redeploy

If you need to manually redeploy:
1. Go to Render Dashboard
2. Click **Manual Deploy** → **Deploy latest commit**

---

**Your backend should now deploy successfully!** 🎉
