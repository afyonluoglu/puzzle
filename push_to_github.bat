git rm -r --cached src/saves/
git add .
git commit -m "Güncellemeler yapıldı"
git push
#gitignore’da tanımlanmasına rağmen push edilenleri kaldır
git rm --cached -r  src/data/__pycache__ src/game/__pycache__ src/utils/__pycache__
git commit -m "Remove __pycache__ directories from repository completely"
git push
