#!/bin/bash

# Create the data directory if it doesn't exist
mkdir -p ./data/MNIST/raw/

# List of mirrors
mirrors=(
    "http://yann.lecun.com/exdb/mnist/"
    "https://ossci-datasets.s3.amazonaws.com/mnist/"
)

# Function to download a file from the list of mirrors
download_with_fallback() {
    local file_name=$1
    local destination="./data/MNIST/raw/$file_name"

    # Check if the file already exists
    if [[ -f "$destination" ]]; then
        echo "${file_name} already exists, skipping download."
        return 0
    fi

    for mirror in "${mirrors[@]}"; do
        echo "Attempting to download ${file_name} from ${mirror}"
        curl -fSL "${mirror}${file_name}" -o "${destination}"
        if [[ $? -eq 0 ]]; then
            echo "Downloaded ${file_name} successfully from ${mirror}"
            return 0
        else
            echo "Failed to download ${file_name} from ${mirror}, trying next mirror..."
        fi
    done

    echo "Error: Failed to download ${file_name} from all mirrors."
    exit 1
}

# List of files to download
files=(
    "train-images-idx3-ubyte.gz"
    "train-labels-idx1-ubyte.gz"
    "t10k-images-idx3-ubyte.gz"
    "t10k-labels-idx1-ubyte.gz"
)

# Download each file with fallback mirrors and extract
for file in "${files[@]}"; do
    download_with_fallback "$file"
    echo "Unzipping ${file}..."
    gunzip -k -f "./data/MNIST/raw/$file"  # Unzip the file, -k option keeps the original .gz file
done

echo "All files downloaded and unzipped to ./data/MNIST/raw/"
