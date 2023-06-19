#/bin/bash

echo "Downloading DATASET_PDFS"
wget https://github.com/fabian57fabian/pdf2info/releases/download/papers_v3/DATASET_100_v2.zip
unzip DATASET_100_v2.zip -d DATASET
rm DATASET_100_v2.zip