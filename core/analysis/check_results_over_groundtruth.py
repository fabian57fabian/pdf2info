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
            #num not considered
            if splitted[2] == '':
                gth[fn] = []
            else:
                keys = splitted[2].split('|')
                gth[fn] = keys
    return gth


def check_results(csv_folder:str, groundtruth:dict) ->(list, list):
    res = []
    res_percentage = []
    for file_tablex in os.listdir(csv_folder):
        if file_tablex.endswith(".csv"):
            f_orig = file_tablex.split('_')[0]+".pdf"
            filename = os.path.join(csv_folder, file_tablex)
            found = 0
            gth_tables = 0
            try:
                keys:list = groundtruth[f_orig].copy()
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
                logging.warning("Unable to complete check on file {}: {}".format(file, str(e)))
            res.append(found)
            res_percentage.append(100.0 if gth_tables== 0 else float(found)/gth_tables)
    return res, res_percentage




if __name__ == '__main__':
    csv_folder="../../analysis/csv_extracted"
    gth = load_groundtruth("../../analysis/GROUNDTRUTH_TEST_200.csv")
    check_results(csv_folder, gth)
