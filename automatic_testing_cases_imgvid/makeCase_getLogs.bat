@echo off

:: chdir %1

echo.
setlocal

:: set /p FILTER="Enter logs filter (for grep): "
IF NOT DEFINED FILTER (SET FILTER=Gain:ExpTime)
echo FILTER= %FILTER%

set N=0
set FILENAME=case%N%.log
:loop
set /a N+=1
set FILENAME=case%N%.log
if exist %FILENAME% goto :loop

echo Setting the size of the log ring buffer.
adb logcat -G 100M

echo Creating log at %FILENAME% with filter %FILTER% 
adb logcat | grep %FILTER% > %FILENAME%

endlocal
