import os


def load(csv_path) -> (dict, int):
    tables_out = {}
    total_tables = 0
    for file in os.listdir(csv_path):
        if file.endswith(".csv"):
            # file format is [pdf_name]-Table[table_number].csv
            splat = file.split('-')
            if len(splat) >= 2:
                pdf_name = splat[0] + ".pdf"
                if pdf_name not in tables_out:
                    tables_out[pdf_name] = 0
                table_description = splat[1]
                if table_description.startswith("Table"):
                    tables_out[pdf_name] += 1
                    total_tables += 1
    return tables_out, total_tables


if __name__ == '__main__':
    folder_csv = "../../out_tab2know/csv"
    out_result = "tab2know_results.csv"
    tables_out, total_tables = load(folder_csv)
    print("Total tables: {}".format(total_tables))
    with open(out_result, 'w') as file:
        file.write("pdf,figures")
        for k, v in tables_out.items():
            file.write("\n{},{}".format(k, v))
