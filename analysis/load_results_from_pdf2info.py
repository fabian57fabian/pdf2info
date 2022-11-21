import sys
sys.path.insert(0, "../")
from core.analysis.results_loader import load_results_from_csv


if __name__ == '__main__':
    folder_csv = "csv_extracted"
    out_result = "pdf2info_results.csv"
    tables_out, total_tables = load_results_from_csv(folder_csv, split_char='_')
    print("Total tables: {}".format(total_tables))
    with open(out_result, 'w') as file:
        file.write("pdf,figures")
        for k, v in tables_out.items():
            file.write("\n{},{}".format(k, v))
