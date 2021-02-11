timeout /T 15

set worldpath=..\..\worlds
set qbpath=.\world

rd /s /Q %worldpath%
md %worldpath%
xcopy %qbpath% %worldpath% /E /H

timeout /T 1
cd ..\..\..\MCModDllExe\
start debug.bat