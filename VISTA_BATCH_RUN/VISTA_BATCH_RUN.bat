@echo off
SET VISTA_VERSION=VISTA_8-5-0
cd..
cd..
set Route_Dir=%CD%\

cd %Route_Dir%\tools\vista\install\VISTA_9-0-0\system
set PATH=%CD%;%PATH%

dir /b  %Route_Dir:~0,2%\fmsa-ver\VISTA_BATCH_RUN\TP_LIST\*.py > %Route_Dir:~0,2%\fmsa-ver\VISTA_BATCH_RUN\scripFilesList.txt
timeout /t 1
set file= %Route_Dir%\fmsa-ver\VISTA_BATCH_RUN\scripFilesList.txt
set scriptStatus= %Route_Dir:~0,2%\fmsa-ver\VISTA_BATCH_RUN\scriptRunningStatus.txt
set /a cnt=0
for /f %%C in ('Find /V /C "" ^< %file%') do set cnt=%%C
echo 
echo The No.of Script Files are: %cnt%
echo
echo 
echo EXECUTING THE SCRIPT FILES
echo off
for /l %%X in (1,1,%cnt%-2) do (call :subroutine "%%G")
GOTO :eof
:subroutine
start KillVista.exe
timeout /t 2
start vista_gui.exe %Route_Dir%\fmsa-ver\VISTA_BATCH_RUN\batchEnvUtl.py
timeout /t 4
set /a flg=0
:while1
if %flg% == 0 (
	for /f "delims=" %%x in (%scriptStatus%) do set flg=%%x
    goto :while1
)
start KillVista.exe
timeout /t 3
GOTO :eof
del %Route_Dir:~0,2%\fmsa-ver\VISTA_BATCH_RUN\scripFilesList.txt
del %Route_Dir:~0,2%\fmsa-ver\VISTA_BATCH_RUN\scriptRunningStatus.txt
exit

