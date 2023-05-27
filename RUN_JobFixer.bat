@echo off
rem Executes python script: JobFixer.py
rem This batch script accepts a single optional argument that is passed as a target directory when present.
set arg1=%1

rem Tests run on Windows 10 and examples:
rem python JobFixer.py -h
rem python JobFixer.py -d "D:\HobbyTime\Documents\FreeCAD_Files\Forum\candl" --s "_fixed"
rem python JobFixer.py -i "D:\HobbyTime\Documents\FreeCAD_Files\Forum\darrylb123\square.FCStd" -o "D:\HobbyTime\Documents\FreeCAD_Files\Forum\darrylb123\square_fixed.FCStd"
rem python JobFixer.py -i "D:\HobbyTime\Documents\FreeCAD_Files\Forum\darrylb123\square.fcstd"
rem python JobFixer.py --s "_fixed"
rem python JobFixer.py -d "%arg1%"
rem python JobFixer.py -i "test.FCStd" -o "test_21.FCStd"

@echo on
python JobFixer.py -d "%arg1%"

pause
