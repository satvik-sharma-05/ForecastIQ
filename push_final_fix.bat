@echo off
echo 🔧 Pushing final Python version fix...
echo.

git add .
git commit -m "Fix: Add render.yaml and flexible package versions for Python 3.11"
git push

echo.
echo ✅ Changes pushed!
echo.
echo 🎯 IMPORTANT: Set Python version in Render Dashboard
echo.
echo 1. Go to: https://dashboard.render.com/web/srv-d7g8g01kh4rs73ebmjeg
echo 2. Click Settings tab
echo 3. Add Environment Variable:
echo    Key: PYTHON_VERSION
echo    Value: 3.11.9
echo 4. Click Save Changes
echo 5. Click Manual Deploy - Deploy latest commit
echo.
echo See RENDER_PYTHON_FIX.md for detailed instructions
pause
