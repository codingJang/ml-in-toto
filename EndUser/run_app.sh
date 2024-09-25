#!/bin/bash
# Change the working directory to the directory of the shell script
cd "$(dirname "$0")"

# Run the dist/app/app binary
./dist/app/app
