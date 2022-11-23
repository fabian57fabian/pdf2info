#/bin/bash

rm tab2know_java_extractor.zip # remove zipped lib
echo "Downloading tab2know_java_extractor"

wget https://github.com/fabian57fabian/pdf2info/releases/download/extractor/tab2know_java_extractor.zip
unzip tab2know_java_extractor.zip
rm tab2know_java_extractor.zip # remove zipped lib
rm run_java_on_papers.sh # useless