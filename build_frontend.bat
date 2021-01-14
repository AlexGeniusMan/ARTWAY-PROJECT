cd ./frontend
git reset --hard HEAD~1
git pull origin main
npm install
npm run-script build
cd ..