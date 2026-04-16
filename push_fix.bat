@echo off
echo 🔧 Pushing Render deployment fix...
echo.

git add .
git commit -m "Fix: Add root-level deployment files for Render"
git push

echo.
echo ✅ Changes pushed to GitHub!
echo 🔄 Render will auto-deploy in a few moments...
echo.
echo Check deployment status at:
echo https://dashboard.render.com/web/srv-d7g8g01kh4rs73ebmjeg
pause
