@echo off
echo 🚀 Pushing ForecastIQ to GitHub...
echo.

REM Initialize git if not already initialized
if not exist .git (
    echo 📦 Initializing git repository...
    git init
)

REM Add all files
echo 📝 Adding files...
git add .

REM Commit
echo 💾 Committing changes...
git commit -m "Initial commit: ForecastIQ - ML Forecasting Platform"

REM Set main branch
echo 🌿 Setting main branch...
git branch -M main

REM Add remote
echo 🔗 Adding remote origin...
git remote add origin https://github.com/satvik-sharma-05/ForecastIQ.git 2>nul || git remote set-url origin https://github.com/satvik-sharma-05/ForecastIQ.git

REM Push to GitHub
echo ⬆️  Pushing to GitHub...
git push -u origin main

echo.
echo ✅ Successfully pushed to GitHub!
echo 🔗 Repository: https://github.com/satvik-sharma-05/ForecastIQ
echo.
echo Next steps:
echo 1. Deploy backend to Render.com
echo 2. Deploy frontend to Vercel.com
echo 3. See DEPLOYMENT.md for details
pause
