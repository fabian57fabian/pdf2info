import os
import shutil
import sys
import logging
import argparse
sys.path.insert(0, "../../")
from core.pdf2info import extract_from_dir, extract_from_pdf, extraction_methods_names
from core.multicore_computing import execute_parallel


def _execute_pdf2info_on_chunk(files_list: list, index, extra_args):
    out_folder, method_used = extra_args
    if len(files_list) == 0:
        logging.warning("0 files to process. skipping")
        return
    counter = 0
    total_files = len(files_list)
    logging.log(logging.DEBUG + 1, "{}: {:.2f}%".format(index, counter / total_files * 100))
    for fn in files_list:
        res, num = extract_from_pdf(fn, out_folder, method_used=method_used)
        counter += 1
        logging.log(logging.DEBUG + 1, "{}: {:.2f}%".format(index, counter / total_files * 100))
    logging.info("{}: Completed {} files".format(index, total_files))


def execute_extraction_with_method(method_used, PARALLEL:bool=True):
    chunks_path = "../DATASET/chunks"
    out_folder = "csv_extracted"
    if os.path.exists(out_folder): shutil.rmtree(out_folder)
    if PARALLEL:
        logging.info("Starting Parallel extraction using " + method_used)
        all_pdfs = []
        for folder in os.listdir(chunks_path):
            if folder.startswith("papers_chunk"):
                logging.debug("Processing {}".format(folder))
                src_dir = os.path.join(chunks_path, folder)
                for file in os.listdir(src_dir):
                    if file.endswith('.pdf'):
                        all_pdfs.append(os.path.join(src_dir, file))
        execute_parallel(all_pdfs, function_for_chunk=_execute_pdf2info_on_chunk, extra_args=(out_folder, method_used))
    else:
        logging.info("Starting Sequential extraction using " + method_used)
        for folder in os.listdir(chunks_path):
            if folder.startswith("papers_chunk"):
                logging.debug("Processing {}".format(folder))
                src_dir = os.path.join(chunks_path, folder)
                total_tables, errored_pdfs, tot_pdf = extract_from_dir(src_dir, out_folder)
                logging.info("pdfs with errors: {}/{} ".format(errored_pdfs, tot_pdf))
                logging.info("tables extracted: {}".format(total_tables))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG+1,
        format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    parser = argparse.ArgumentParser(description='Extracts tables from pdfs inside a directory.')
    parser.add_argument('--method', type=str, default='tabula', help='Method to use', choices=extraction_methods_names())
    args = parser.parse_args()
    PARALLEL = True
    method_used = args.method
    execute_extraction_with_method(method_used, PARALLEL)