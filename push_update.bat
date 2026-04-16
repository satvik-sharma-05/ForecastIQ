@echo off
echo 🐍 Pushing Python 3.11 compatibility update...
echo.

git add .
git commit -m "Update: Python 3.11.9 with latest compatible packages"
git push

echo.
echo ✅ Changes pushed to GitHub!
echo 🔄 Render will auto-deploy with Python 3.11.9
echo ⚡ Deployment should be much faster now!
echo.
echo Check deployment status at:
echo https://dashboard.render.com/web/srv-d7g8g01kh4rs73ebmjeg
echo.
echo After deployment, retrain models in Render Shell:
echo   pip install -r training_requirements.txt
echo   python train_models.py
pause
