brew upgrade
brew services run postgresql@15
uvicorn app.main:app --reload &
sleep 7200
pkill -f uvicorn
brew services stop postgresql@15