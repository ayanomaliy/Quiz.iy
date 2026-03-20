@echo off
py -m PyInstaller --onefile --name quiziy main.py
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
pause