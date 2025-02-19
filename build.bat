@echo off
nuitka --mingw64 --onefile --standalone --remove-output --output-dir=dist --follow-imports --output-filename=WSL.exe main.py && nuitka --mingw64 --onefile --standalone --remove-output --windows-console-mode=disable --output-dir=dist --follow-imports --output-filename=WSL_init.exe init.py
pause