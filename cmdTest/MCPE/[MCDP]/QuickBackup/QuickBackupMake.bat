timeout /T 15

set worldpath=..\..\worlds
set qbpath=.\world

rd /s /Q %qbpath%
md %qbpath%
xcopy %worldpath% %qbpath% /E /H

pause
::timeout /T 1
::cd ..\..\..\MCModDllExe\
::start debug.bat