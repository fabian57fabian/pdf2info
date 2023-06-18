import logging
import os
import shutil


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


def _csv_contains_a_key(fn: str, keys: list) -> (str, float):
    if not os.path.exists(fn):
        logging.warning(f"Given csv file does not exist. Skipping {fn}")
        return None, 0.0
    max_common = 0
    max_key = None
    with open(fn, 'r') as file:
        lines = [l.rstrip() for l in file.readlines()]
        for k_table in keys:
            found_ks = 0
            subkeys = k_table.split("^^^")
            for k in subkeys:
                for l in lines:
                    if k in l:
                        found_ks += 1
                        break
            if found_ks > max_common:
                max_common = found_ks / len(subkeys)
                max_key = k_table
    return max_key, max_common


def check_results(csv_folder:str, groundtruth:dict, split_char='-') ->(int, int, int, int, list, list):
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
    PRECISONS_IOU = []
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
                    key_found, precision = _csv_contains_a_key(fn, gth[f_orig])
                    if key_found is not None:
                        this_TP += 1
                        gth[f_orig].remove(key_found)
                        PRECISONS_IOU.append(precision)
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
    return TP, TN, FP, FN, PRECISONS_IOU, files_percentage_ok




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    # write results
    csv_folder="tmp_test"
    if os.path.exists(csv_folder):
        shutil.rmtree(csv_folder)
    os.mkdir(csv_folder)
    # write groundtruth
    with open("test_GTH.csv", 'w') as file:
        file.write("2211.09613.pdf,Slow fading^^^23.82^^^26.79^^^33.56^^^20 dB|Train SNR^^^44.87^^^44.65^^^45.74^^^15 dB")
    # write full table 1
    with open("tmp_test/2211.09613_Table1.csv", 'w') as file:
        file.write("Channel model,0 dB,5 dB,10 dB,15 dB,20 dB\nAWGN,23.82,27.44,30.57,32.63,33.56\nSlow fading,22.46,25.07,26.79,27.62,27.92")
    # write table 2 without last column
    with open("tmp_test/2211.09613_Table2.csv", 'w') as file:
        file.write("Trains SNR,0 dB,5 dB,10 dB,15 dB\n0 dB,44.87,45.38,45.50,45.65\nSlow fading,35.84,41.78,44.65,45.87")

    gth = load_groundtruth("test_GTH.csv")
    res = check_results(csv_folder, gth, split_char='_')

    logging.info("res: {}".format(res))

    os.remove("test_GTH.csv")
    os.remove("tmp_test/2211.09613_Table1.csv")
    os.remove("tmp_test/2211.09613_Table2.csv")
    shutil.rmtree(csv_folder)
