@echo off
echo.
echo -  Testing - Automated! -
echo -- - - - - - - - - - - -- 
echo.

set /p fld="Enter folder name (enter for current dir): "
IF NOT DEFINED fld (SET fld=".")
echo Folder= %fld%

SET ORIGINAL=%CD%
chdir %fld%

echo -- - - - - - - - - - - -- 
echo.
:loop
echo.
echo - Starting Logs script
echo "GettingLogs" "%ORIGINAL%\makeCase_getLogs.bat" %fld%
start "GettingLogs" "%ORIGINAL%\makeCase_getLogs.bat" %fld%

echo.
echo - Starting video capture on device!
adb shell input tap 1876 1247

timeout /t 10

echo.
echo - Ending video capture on device!
adb shell input tap 1277 1267

echo.
echo - Stopping Logs!
taskkill /F /T /fi "WINDOWTITLE eq GettingLogs *"

echo.
echo - Gettting new video...
echo -
adb pull sdcard/DCIM/Camera

echo.
echo - Removing fetched images/videos from device... 

adb shell rm -rf sdcard/DCIM/Camera
echo Fetched and cleaned!

echo.
echo - Moving file and cleaning up.
move Camera\* .
rd /q Camera

echo.
echo - Renaming files...
python "%ORIGINAL%\makeCase_rename.py" "" VID mp4

echo.
echo - Case Done!
echo.
echo -- - - - - - - - - - - -- 
echo.
choice /m Again
if not errorlevel 2 goto :loop

echo -------------------------------
echo Thanks for using Marty's script.
timeout 3
