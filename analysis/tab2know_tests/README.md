# Extracting with tab2know

tab2know uses a java jar file **tab2know_java_extractor.jar** to extract figures (using tab2know and PDFFigures2) written in scala.

## Usage

From comparison filder:

```console
$ ./download_test_files.sh
```

This might take some minutes. 
When all necessary dataset and scripts are downloaded, execute:

```console
$ ./run_java_on_papers.sh
```

This might take some time depending on your CPU.

FAQ: *OutOfMemory* java exception:
The dataset is splitted into 4 chunks of 50 pdfs.
Consider splitting it in 8 chunks of 25 pdfs and change run_java_on_papers.sh by adding more calls to the java jar (check that script for example). 

Finally, call python script to count extracted figures:

```console
$ python3 load_groundtruth_from_tab2know.py
```

This will create the  *tab2know_results.csv*.
This should be similar to tab2know_results_PAPER_TEST_200.csv.

You have succesfully replicated tab2know extractor results.

## Description

The download_test_files.sh script will:
- download the dataset having 200 pdfs from a release published on pdf2info repository.
- download the tab2know java extractor (and a script to directly launch it with all paths set)

Then the run_java_on_papers.sh script will:
- Create the *out_tab2know* folder where results will be placed
- run the java extarctor one time for each *papers_chunkX* folder.

Finally the load_groundtruth_from_tab2know.py script will:
- Count the figures created in out_tab2know/csv for each pdf
- Print the total amount of figures retrieved
- save a *tab2know_results.csv* file containing figures count per pdf.