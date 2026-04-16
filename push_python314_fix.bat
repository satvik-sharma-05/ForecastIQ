@echo off
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🐍 Python 3.14 Compatibility Fix                         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo This will make your app work with Python 3.14!
echo.
echo ════════════════════════════════════════════════════════════
echo STEP 1: Pushing changes to GitHub...
echo ════════════════════════════════════════════════════════════
echo.

git add .
git commit -m "Python 3.14 compatibility: use pre-built wheels"
git push

echo.
echo ✅ Changes pushed!
echo.
echo ════════════════════════════════════════════════════════════
echo STEP 2: Update Render Build Command
echo ════════════════════════════════════════════════════════════
echo.
echo Go to: https://dashboard.render.com/web/srv-d7g8g01kh4rs73ebmjeg
echo.
echo 1. Click "Settings" tab
echo 2. Find "Build Command" section
echo 3. Click "Edit"
echo 4. Replace with:
echo.
echo    pip install --upgrade pip setuptools wheel ^&^& pip install --prefer-binary --no-cache-dir -r requirements.txt
echo.
echo 5. Click "Save Changes"
echo 6. Click "Manual Deploy" - "Deploy latest commit"
echo.
echo ════════════════════════════════════════════════════════════
echo.
echo See PYTHON314_FIX.md for detailed instructions
echo.
pause
