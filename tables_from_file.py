from core.pdf2info import extract_from_pdf
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
    parser = argparse.ArgumentParser(description='Extracts tables from a pdf.')
    parser.add_argument('--file', type=str, help='PDF file to process')
    parser.add_argument('--out', type=str, default='./', help='Out folder')
    parser.add_argument('--log-console', action='store_true', default=False, help='if logging to console instead of logging file')
    args = parser.parse_args()

    init_logging(logging.INFO, None if args.log_console else "result.log")

    src_file = args.file
    out_file = args.out
    res, tables = extract_from_pdf(src_file, out_file)
    logging.info("Result: {} ".format(res))
    if res: logging.info("tables extracted: {}".format(len(tables)))
