# Push to GitHub - Quick Guide

## 🚀 Automated Push (Easiest)

### Windows
```bash
push_to_github.bat
```

### Linux/Mac
```bash
chmod +x push_to_github.sh
./push_to_github.sh
```

## 📝 Manual Push

```bash
# 1. Initialize git (if not already done)
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit: ForecastIQ - ML Forecasting Platform"

# 4. Set main branch
git branch -M main

# 5. Add remote
git remote add origin https://github.com/satvik-sharma-05/ForecastIQ.git

# 6. Push to GitHub
git push -u origin main
```

## ⚠️ If Remote Already Exists

```bash
# Update remote URL
git remote set-url origin https://github.com/satvik-sharma-05/ForecastIQ.git

# Then push
git push -u origin main
```

## 🔄 Subsequent Pushes

After the first push, use:

```bash
git add .
git commit -m "Your commit message"
git push
```

## 📋 What Gets Pushed

✅ Included:
- All source code (backend, frontend)
- Documentation (README, DEPLOYMENT, etc.)
- Configuration files
- Sample data
- Training scripts
- License

❌ Excluded (via .gitignore):
- .env files (secrets)
- node_modules/
- __pycache__/
- uploads/
- dist/
- Virtual environments

## ✅ After Pushing

1. Visit: https://github.com/satvik-sharma-05/ForecastIQ
2. Add repository description
3. Add topics/tags
4. Enable Issues
5. Add website URL (after deployment)

## 🚀 Next Steps

1. ✅ Push to GitHub
2. 📦 Deploy backend to Render
3. 🌐 Deploy frontend to Vercel
4. 🔗 Update URLs in README

See **DEPLOYMENT.md** for deployment guide.

---

**Repository:** https://github.com/satvik-sharma-05/ForecastIQ
