#!/bin/bash

# Define your main Python script file
MAIN_SCRIPT="scraper-ui.py"

# List additional Python files (if any)
ADDITIONAL_FILES="scraper_csv.py onvo.py"

# Define the output directory
OUTPUT_DIR="dist"

# Function to build Windows executable
build_windows_executable() {
    echo "Building Windows executable"
    wine pyinstaller.exe --onefile --name=onvo_ws_windows.exe --distpath="$OUTPUT_DIR/windows" "$MAIN_SCRIPT" $ADDITIONAL_FILES
}

# Function to build macOS application bundle
build_macos_bundle() {
    echo "Building macOS application bundle"
    pyinstaller --onefile --name=OnvoWSMacOS --distpath="$OUTPUT_DIR/macos" "$MAIN_SCRIPT" $ADDITIONAL_FILES
}

# Function to build Linux executable
build_linux_executable() {
    echo "Building Linux executable"
    pyinstaller --onefile --name=onvo_ws_linux --distpath="$OUTPUT_DIR/linux" "$MAIN_SCRIPT" $ADDITIONAL_FILES
}

# Build executables for different platforms
build_windows_executable
build_macos_bundle
build_linux_executable
