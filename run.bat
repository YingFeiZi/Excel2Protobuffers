@echo off

if exist "../Python3.11.7" (
"../Python3.11.7/python" generator.py %1
) else (
python" generator.py %1
)

if %errorlevel%==0 (
    exit
) else (
    echo Error: %errorlevel%: %1
    pause
)