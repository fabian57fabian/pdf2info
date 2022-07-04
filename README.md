# pdf2info

Pdf2info is a simple table extractor library using tabula.

## How to use

Place all your necessary PDFs in a single dicrectory, then call process_folder.py script:

```console
$ python process_folder.py --dir=path/to/your/dir --out=path/to/out/folder
```

This will create one csv file per table.

Logging can be read in **results.log** file. If need to check console live log, add **--log-console** param:

```console
$ python process_folder.py --dir=path/to/your/dir --out=path/to/out/folder --log-console
```