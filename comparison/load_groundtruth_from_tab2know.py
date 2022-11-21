import sys
sys.path.insert(0, "../")
from core.analysis.results_loader import load_results_from_csv


if __name__ == '__main__':
    folder_csv = "out_tab2know/csv"
    out_result = "tab2know_results.csv"
    tables_out, total_tables = load_results_from_csv(folder_csv)
    print("Total tables: {}".format(total_tables))
    with open(out_result, 'w') as file:
        file.write("pdf,figures")
        for k, v in tables_out.items():
            file.write("\n{},{}".format(k, v))
