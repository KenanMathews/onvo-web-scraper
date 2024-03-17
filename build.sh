#!/bin/bash

# Define your main Python script file
MAIN_SCRIPT="scraper-ui.py"

# List additional Python files (if any)
ADDITIONAL_FILES="scraper-ui.py scraper_csv.py basketball_reference_web_scraper/parsers/players_advanced_season_totals.py basketball_reference_web_scraper/parsers/__init__.py basketball_reference_web_scraper/parsers/positions.py basketball_reference_web_scraper/parsers/players_season_totals.py basketball_reference_web_scraper/parsers/box_scores/teams.py basketball_reference_web_scraper/parsers/box_scores/__init__.py basketball_reference_web_scraper/parsers/box_scores/games.py basketball_reference_web_scraper/parsers/box_scores/players.py basketball_reference_web_scraper/parsers/schedule.py basketball_reference_web_scraper/http_client.py basketball_reference_web_scraper/client.py basketball_reference_web_scraper/json_encoders.py basketball_reference_web_scraper/__init__.py basketball_reference_web_scraper/errors.py basketball_reference_web_scraper/utilities.py basketball_reference_web_scraper/data.py basketball_reference_web_scraper/output.py onvo.py integkey.py"

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
