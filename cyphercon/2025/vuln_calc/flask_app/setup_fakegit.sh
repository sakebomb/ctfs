#!/bin/bash

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Create a temporary directory for the repository
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Initialize a git repository
git init

# Create the flag file
echo "flag{GitIsWeirdAintIt}" > flag.txt

# Configure git
git config user.email "root@example.com"
git config user.name "root"

# Add and commit the flag
git add flag.txt
git commit -m "Add flag"

# Copy the .git directory to fakegit
rm -rf "$SCRIPT_DIR/fakegit"
mkdir -p "$SCRIPT_DIR/fakegit"
cp -r .git/. "$SCRIPT_DIR/fakegit/"

# Clean up
cd "$SCRIPT_DIR"
rm -rf "$TEMP_DIR" 