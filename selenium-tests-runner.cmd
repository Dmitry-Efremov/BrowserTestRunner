set python=%~dp0vendors\python\python.exe
WHERE python.exe
IF %ERRORLEVEL% EQU 0 set python="python.exe"

%python% %~dp0selenium-tests-runner.py %*
rem pause
