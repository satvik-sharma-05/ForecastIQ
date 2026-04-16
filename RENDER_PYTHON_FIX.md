# 🔧 Fix Python Version on Render

## Problem
Render is using Python 3.14.3 (default) which doesn't have pre-built wheels for pandas, causing very slow builds.

## ✅ Solution: Set Python Version in Render Dashboard

### Step 1: Go to Render Dashboard
1. Visit: https://dashboard.render.com/web/srv-d7g8g01kh4rs73ebmjeg
2. Click on **Settings** tab

### Step 2: Set Python Version
1. Scroll to **Environment** section
2. Click **Add Environment Variable**
3. Add:
   - **Key:** `PYTHON_VERSION`
   - **Value:** `3.11.9`
4. Click **Save Changes**

### Step 3: Redeploy
1. Go to **Manual Deploy** section
2. Click **Deploy latest commit**
3. Wait for deployment (~2 minutes)

## Alternative: Use render.yaml (Automatic)

I've created a `render.yaml` file that automatically configures Python 3.11.9.

Push it to GitHub:
```bash
git add render.yaml
git commit -m "Add render.yaml for Python 3.11.9"
git push
```

Render will automatically detect and use this configuration.

## ✅ Updated Requirements

I've also updated `requirements.txt` to use flexible version ranges:
- This allows pip to find the best available pre-built wheels
- Works with both Python 3.11 and 3.14
- Much faster installation

## 🚀 Push Changes

```bash
git add .
git commit -m "Fix: Use flexible package versions and render.yaml"
git push
```

## 📊 Expected Results

**Before:**
- Python 3.14.3 (default)
- Building pandas from source
- 10+ minutes build time
- Often times out

**After:**
- Python 3.11.9 (specified)
- Pre-built wheels
- 1-2 minutes build time
- Reliable deployment

## 🎯 Quick Fix Steps

1. **Push changes:**
   ```bash
   git add .
   git commit -m "Fix: Add render.yaml and flexible package versions"
   git push
   ```

2. **Set Python version in Render:**
   - Dashboard → Settings → Environment Variables
   - Add: `PYTHON_VERSION` = `3.11.9`
   - Save

3. **Redeploy:**
   - Manual Deploy → Deploy latest commit

## ✅ Verification

After deployment:
1. Check logs for: `Using Python version 3.11.9`
2. Build should complete in ~2 minutes
3. Visit: https://forecastiq-backend.onrender.com/docs

---

**This will fix the slow build issue!** 🎉
