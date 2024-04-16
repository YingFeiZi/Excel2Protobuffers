@echo off
cd /d %~dp1
echo %cd%
pyinstaller --onefile --windowed --hidden-import google.protobuf --paths %cd% -F %1 -i %~dp0/icon.ico
pause