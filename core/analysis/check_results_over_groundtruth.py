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


def check_results(csv_folder:str, groundtruth:dict) ->(list, list):
    res = []
    res_percentage = []
    i = 1
    for file_tablex in os.listdir(csv_folder):
        logging.info("{}: {}".format(i, file_tablex))
        i+=1
        if file_tablex.endswith(".csv"):
            f_orig = file_tablex.split('_')[0]+".pdf"
            filename = os.path.join(csv_folder, file_tablex)
            found = 0
            gth_tables = 0
            try:
                if f_orig not in groundtruth:
                    logging.warning("File {} not in groundtruth table!".format(f_orig))
                else:
                    keys:list = [k for k in groundtruth[f_orig]]
                    gth_tables = len(keys)
                    if gth_tables> 0:
                        with open(filename, 'r') as file:
                            for l in file.readlines():
                                for k in keys:
                                    if k in l:
                                        keys.remove(k)
                                        found += 1
                                        break
            except Exception as e:
                logging.warning("Unable to complete check on file {}: {}".format(file_tablex, str(e)))
            res.append(found)
            res_percentage.append(100.0 if gth_tables== 0 else float(found)/gth_tables*100)
    return res, res_percentage




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    csv_folder="../../analysis/csv_extracted"
    gth = load_groundtruth("../../analysis/DATASET_PDFS_50/GROUNDTRUTH_DATASET.csv")
    check_results(csv_folder, gth)
