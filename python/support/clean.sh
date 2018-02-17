find . -maxdepth 1 -type d -name "pcg*" | xargs -r rm -rf
find build -type f | xargs -r rm
