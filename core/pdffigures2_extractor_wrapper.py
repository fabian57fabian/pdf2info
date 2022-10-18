import os

from datasets import datasets
import extractors
import argparse
from time import time


def main():
    parser = argparse.ArgumentParser(description='Time a figure extractor')
    #parser.add_argument("extractor", choices=list(extractors.EXTRACTORS.keys()), help="Name of the extractor to test")
    parser.add_argument("--dataset", help="Name of the extractor to test")
    args = parser.parse_args()

    extr = 'pdffigures2'
    write_figures = True
    verbose = False
    dataset_path = args.dataset
    if not os.path.exists(dataset_path):
        print("NOOOOO")
        return
    extractor = extractors.get_extractor(extr)

    filenames = [os.path.join(dataset_path, f) for f in os.listdir(dataset_path)]
    #filenames = [f.replace("\\", "/") for f in filenames]
    extractor.time(filenames, write_figures, verbose=verbose).print("Done")


if __name__ == '__main__':
    main()