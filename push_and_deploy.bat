@echo off
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🚨 CRITICAL: READ THIS BEFORE DEPLOYING 🚨                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo You MUST set Python version in Render Dashboard FIRST!
echo.
echo 1. Go to: https://dashboard.render.com/web/srv-d7g8g01kh4rs73ebmjeg
echo 2. Click "Settings" tab
echo 3. Add Environment Variable:
echo    Key: PYTHON_VERSION
echo    Value: 3.11
echo 4. Click "Save Changes"
echo.
echo ════════════════════════════════════════════════════════════
echo.
set /p confirm="Have you set PYTHON_VERSION=3.11 in Render? (y/n): "

if /i "%confirm%" NEQ "y" (
    echo.
    echo ❌ Please set PYTHON_VERSION first, then run this script again.
    echo See CRITICAL_RENDER_SETUP.md for instructions.
    pause
    exit /b
)

echo.
echo ✅ Great! Now pushing changes to GitHub...
echo.

git add .
git commit -m "Simplify requirements for Python 3.11 compatibility"
git push

echo.
echo ✅ Changes pushed!
echo.
echo 🔄 Now go to Render Dashboard and click:
echo    "Manual Deploy" → "Deploy latest commit"
echo.
echo ⏱️  Deployment should complete in ~2 minutes
echo.
pause
