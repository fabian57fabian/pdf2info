#/bin/bash

rm out_tab2know -r
mkdir out_tab2know
mkdir out_tab2know/csv/
mkdir out_tab2know/images/
mkdir out_tab2know/json/

MAIN_DIR="../DATASET_PDFS_50/chunks/"

for dir in "${MAIN_DIR}"*/; do
  echo "Extractinh from  ${dir}"
  java -jar tab2know-extractor.jar \
  --pdf "${dir}" \
  --csv out_tab2know/csv/ \
  --img out_tab2know/images/ \
  --json out_tab2know/json/
done