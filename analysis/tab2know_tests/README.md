# Extracting with tab2know

tab2know uses a java jar file **tab2know_java_extractor.jar** to extract figures (using tab2know and PDFFigures2) written in scala.

## Usage

First download java executor from github repo.

```console
$ ./download_extractor_tab2know.sh
```

Then run extractor. It will launch a java instance for each chunk of data in dataset.
Execute:

```console
$ ./run_java_on_papers.sh
```

This might take some time depending on your CPU.

FAQ: *OutOfMemory* java exception:
The dataset is splitted into chunks of 25 pdfs.
Consider splitting it in more chunks (e.g. of 12 pdfs).
The bash script will automatically process all chunks folder it finds.

Finally, call python script to compare to groundtruth and show a heatmap.

```console
$ python3 show_results_tab2know.py
```

This will also save the figure in../results/tab2know_on_DATASET_PDFS_50.png

You have succesfully replicated tab2know extractor results.

## Description

The download_extractor_tab2know.sh script will:
- download the tab2know java extractor.

Then the run_java_on_papers.sh script will:
- Create the *out_tab2know* folder where results will be placed
- run the java extarctor one time for each *papers_chunkX* inside DATASET/chunks/*

Finally the show_results_tab2know.py script will:
- Find each table saved in out_tab2know/csv for each pdf
- Match them to groundtruth
- plot a heatmap, show and save to ../results/tab2know_on_DATASET_PDFS_50