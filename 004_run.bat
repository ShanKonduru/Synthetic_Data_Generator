@echo off
REM --- Batch file to run Python data generation scripts ---

REM Set the title for the command prompt window
title Python Data Generator

REM Display a message indicating what's happening
echo.
echo Running Python Class-Based Data Generator...
echo ------------------------------------------
python main_class_based.py

echo.
echo ------------------------------------------
echo Running Python JSON-Based Data Generator...
echo ------------------------------------------
python main_json_based.py

echo.
echo ------------------------------------------
echo All Python scripts have finished.
echo Press any key to close this window...
pause > NUL