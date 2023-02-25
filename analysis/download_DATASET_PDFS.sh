#/bin/bash

echo "Downloading DATASET_PDFS"
wget https://github.com/fabian57fabian/pdf2info/releases/download/papers_v2/DATASET_PDFS_100.zip
unzip DATASET_PDFS_100.zip -d DATASET
rm DATASET_PDFS_100.zip