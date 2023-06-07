import os
import shutil
import sys
import logging
import argparse
sys.path.insert(0, "../../")
from core.pdf2info import extraction_methods_names
from analysis.pdf2info_tests.execute_pdf2info_on_DATASET import execute_extraction_with_method
from analysis.pdf2info_tests.show_results_pdf2info import create_plots_results

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    all_methods = extraction_methods_names() + ['all']
    for method_used in all_methods:
        logging.info("Extracting with {}".format(method_used))
        execute_extraction_with_method(method_used, PARALLEL=True)
        create_plots_results(method_used, show_fig=False)