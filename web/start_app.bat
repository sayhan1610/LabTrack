@echo off
echo These steps are for fun and are absolutely useless. Spam the space bar to speed up the process.
echo Starting app...
timeout 3 >nul
echo Scanning directory...
timeout 2 >nul
tree
timeout 3 >nul
type index.html
type script.js
type styles.css
echo Finished reading directory. Starting server...
timeout 3 >nul
python app.py
pause