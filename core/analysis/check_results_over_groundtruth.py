import logging
import os


def load_groundtruth(path:str):
    gth = {}
    with open(path, 'r') as file:
        for l in file.readlines():
            splitted = l.strip().split(',')
            if len(splitted) < 3:
                logging.warning("Error in gth file {}".format(file))
            fn = splitted[0]
            if splitted[1] == '' or splitted[1] == "_NO_TABLES_":
                gth[fn] = []
            else:
                keys = splitted[1].split('|')
                gth[fn] = keys
    return gth


def check_results(csv_folder:str, groundtruth:dict, split_char='-') ->(list, list):
    res = []
    res_percentage = []
    results = {}
    i = 1
    for k,v in groundtruth.items():
        results[k] = []
    for file_tablex in os.listdir(csv_folder):
        if file_tablex.endswith(".csv"):
            f_orig = file_tablex.split(split_char)[0]+".pdf"
            if f_orig not in results: results[f_orig] = []
            results[f_orig].append(file_tablex)
    for f_orig, tables_names in results.items():
        logging.info("{}: {}".format(i, f_orig))
        i += 1
        found = 0
        gth_tables = len(groundtruth[f_orig])
        for table_filename in tables_names:
            try:
                if f_orig not in groundtruth:
                    logging.warning("File {} not in groundtruth table!".format(f_orig))
                else:
                    keys:list = [k for k in groundtruth[f_orig]]
                    if gth_tables> 0:
                        with open(os.path.join(csv_folder, table_filename), 'r') as file:
                            for l in file.readlines():
                                for k in keys:
                                    if k in l:
                                        keys.remove(k)
                                        found += 1
                                        break
            except Exception as e:
                logging.warning("Unable to complete check on file {}: {}".format(file_tablex, str(e)))
        res.append(found)
        if gth_tables== 0:
            res_percentage.append(100.0)
        else:
            res_percentage.append(float(found)/gth_tables*100)
    return res, res_percentage




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    csv_folder="../../analysis/csv_extracted"
    gth = load_groundtruth("../../analysis/DATASET_PDFS_50/GROUNDTRUTH_DATASET.csv")
    check_results(csv_folder, gth, split_char='_')
