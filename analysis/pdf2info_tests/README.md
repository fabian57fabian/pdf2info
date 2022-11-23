# Extracting with pdf2info

We will be using pdf2info extractor and then checking results.

## Usage

Make sure to have the dataset in upper folder (e.g. DATASET_PDFS_50)

Run the extarctor. It will launch the extarction on multipl cores.
Execute.

```console
$ python3 execute_pdf2info_on_DATASET_50.py
```

This might take some time depending on your CPU.

Finally, call python script to compare to groundtruth and show a heatmap.

```console
$ python3 show_results_pdf2info.py
```

This will also save the figure in../results/pdf2info_on_DATASET_PDFS_50.png

You have succesfully extracted tables with pdf2info.

## Description

The execute_pdf2info_on_DATASET_50.py script will:
- Create the csv_extracted folder
- Run table extraction on multiple cores.
- Save all tables in csv_extracted

Finally the show_results_tab2know.py script will:
- Find each table saved in out_tab2know/csv for each pdf
- Match them to groundtruth
- plot a heatmap, show and save to ../results/pdf2info_on_DATASET_PDFS_50