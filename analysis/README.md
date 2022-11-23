# Extracting with pdf2info

We will be using pdf2info extractor and then checking results.

## Usage

From analysis folder:

```console
$ ./download_test_files.sh
```

This might take some minutes. 
When all necessary dataset and scripts are downloaded, execute:

```console
$ python3 execute_pdf2info_on_DATASET_50.py
```

This might take some time depending on your CPU.

Finally, call python script to count extracted figures:

```console
$ python3 load_results_from_pdf2info.py
```

This will create the  *pdf2info_results.csv*.
This should be similar to pdf2info_results_PAPER_TEST_200.csv.

You have succesfully extracted tables with pdf2info.

## Description

The download_test_files.sh script will:
- download the dataset having 200 pdfs from a release published on pdf2info repository.

Then the execute_pdf2info_on_PAPERS_TEST_200.py script will:
- Create the *csv_extracted* folder where results will be placed
- run pdf2info one time for each *papers_chunkX* folder.

Finally the load_results.from_pdf2info.py script will:
- Count the figures created in csv_extracted/csv for each pdf
- Print the total amount of figures retrieved
- save a *pdf2info_results.csv* file containing figures count per pdf.