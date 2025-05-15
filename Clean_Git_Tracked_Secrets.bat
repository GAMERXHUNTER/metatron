
@echo off
echo 🧹 Cleaning Git-tracked sensitive folders and files...

REM Remove tracked folders
git rm -r --cached Vault
git rm -r --cached Logs
git rm -r --cached Outputs
git rm -r --cached exports

REM Remove tracked databases and artifacts
git rm --cached *.db
git rm --cached *.sqlite

echo ✅ Done. Now commit and push with:
echo git add .
echo git commit -m "🧹 Removed sensitive vault data from repo"
echo git push

pause
