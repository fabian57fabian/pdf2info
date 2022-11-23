from core.pdf2info import extract_from_dir
import logging
import argparse


def init_logging(lvl, fn):
    if fn is None:
        logging.basicConfig(
            level=lvl,
            format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'
        )
    else:
        logging.basicConfig(
            filename='result.log',
            level=lvl,
            format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts tables from pdfs inside a directory.')
    parser.add_argument('--dir', type=str, required=True, help='Directory with PDFs')
    parser.add_argument('--out', type=str, default='./', help='Out folder')
    parser.add_argument('--log-console', action='store_true', default=False, help='if logging to console instead of logging file')
    args = parser.parse_args()

    init_logging(logging.INFO, None if args.log_console else "result.log")

    src_dir = args.dir
    out_folder = args.out
    total_tables, errored_pdfs, tot_pdf = extract_from_dir(src_dir, out_folder)
    logging.info("pdfs with errors: {}/{} ".format(errored_pdfs, tot_pdf))
    logging.info("tables extracted: {}".format(total_tables))
