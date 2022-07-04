from pdf2info import extract_from_dir
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dir', type=str, help='Directory with PDFs')
    parser.add_argument('--out', type=str, help='Out directory')
    args = parser.parse_args()

    src_dir = args.dir
    out_folder = args.out
    total_tables, errored_pdfs, tot_pdf = extract_from_dir(src_dir, out_folder)
    print("pdfs with errors: {}/{} ".format(errored_pdfs, tot_pdf))
    print("tables extracted: {}".format(total_tables))
