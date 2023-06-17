import logging
import os


def load_groundtruth(path:str):
    gth = {}
    with open(path, 'r') as file:
        for l in file.readlines():
            splitted = l.strip().split(',')
            if len(splitted) < 2:
                logging.warning("Error in gth file {}".format(file))
            fn = splitted[0]
            if splitted[1] == '' or splitted[1] == "_NO_TABLES_":
                gth[fn] = []
            else:
                keys = splitted[1].split('|')
                gth[fn] = keys
    return gth


def _csv_contains_a_key(fn: str, keys: list) -> str:
    if not os.path.exists(fn):
        logging.warning(f"Given csv file does not exist. Skipping {fn}")
        return None
    with open(fn, 'r') as file:
        for l in file.readlines():
            for k in keys:
                if k in l:
                    return k
    return None


def check_results(csv_folder:str, groundtruth:dict, split_char='-') ->(list, list):
    gth = groundtruth.copy()
    files_percentage_ok = []
    results = {}
    i = 1
    for k,v in gth.items():
        results[k] = []
    # Loads all output pdfs from a folder after tables extraction. Format '[PDF_NAME]_Table[table_index].csv'
    for file_tablex in os.listdir(csv_folder):
        if file_tablex.endswith(".csv"):
            f_orig = file_tablex.split(split_char)[0]+".pdf"
            if f_orig not in results: results[f_orig] = []
            results[f_orig].append(file_tablex)
    # Find Precision
    TP = 0
    FP = 0
    FN = 0
    for f_orig, tables_names in results.items():
        logging.info("{}: {}".format(i, f_orig))
        i += 1
        gth_tables = len(gth[f_orig])
        this_TP = 0
        this_FP = 0
        for table_filename in tables_names:
            try:
                if f_orig not in gth:
                    logging.warning("File {} not in groundtruth table!".format(f_orig))
                    continue
                if gth_tables > 0:
                    fn = os.path.join(csv_folder, table_filename)
                    key_found = _csv_contains_a_key(fn, gth[f_orig])
                    if key_found is not None:
                        this_TP += 1
                        gth[f_orig].remove(key_found)
                    else:
                        this_FP += 1
            except Exception as e:
                logging.warning("Unable to complete check on file {}: {}".format(f_orig, str(e)))
        TP += this_TP
        FP += this_FP
        if gth_tables == 0:
            files_percentage_ok.append(100.0)
        else:
            acc = float(this_TP)/gth_tables*100
            files_percentage_ok.append(acc)
            FN += gth_tables - this_TP
    TN = 0 # if no table, ok but no other info.
    return TP, TN, FP, FN, files_percentage_ok




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    csv_folder="../../analysis/csv_extracted"
    gth = load_groundtruth("../../analysis/DATASET_PDFS_50/GROUNDTRUTH_DATASET.csv")
    check_results(csv_folder, gth, split_char='_')
