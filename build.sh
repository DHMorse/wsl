#!/bin/bash

# Build the main executable
python -m nuitka --onefile --standalone --remove-output --output-dir=dist --follow-imports --output-filename=myWSL src/search.py

# Build the init executable
python -m nuitka --onefile --standalone --remove-output --output-dir=dist --follow-imports --output-filename=WSL_init src/main.py

# Wait for user input before closing
read -p "Press Enter to continue..." 