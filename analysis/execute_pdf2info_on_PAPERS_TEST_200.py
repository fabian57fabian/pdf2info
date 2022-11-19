import os
import sys
import logging
sys.path.insert(0, "../")
from core.pdf2info import extract_from_dir


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(process)d-%(levelname)s-%(message)s',
        datefmt='%H:%M:%S'
    )
    chunks_path = "./"
    out_folder = "csv_extracted"
    for folder in os.listdir(chunks_path):
        if folder.startswith("papers_chunk"):
            print("Processing {}".format(folder))
            src_dir = os.path.join(chunks_path, folder)
            total_tables, errored_pdfs, tot_pdf = extract_from_dir(src_dir, out_folder)
            logging.info("pdfs with errors: {}/{} ".format(errored_pdfs, tot_pdf))
            logging.info("tables extracted: {}".format(total_tables))