import os


def load_results_from_csv(csv_path, split_char='-') -> (dict, int):
    tables_out = {}
    total_tables = 0
    for file in os.listdir(csv_path):
        if file.endswith(".csv"):
            # file format is [pdf_name]-Table[table_number].csv
            splat = file.split(split_char)
            if len(splat) >= 2:
                pdf_name = splat[0] + ".pdf"
                if pdf_name not in tables_out:
                    tables_out[pdf_name] = 0
                table_description = splat[1]
                if table_description.startswith("Table"):
                    tables_out[pdf_name] += 1
                    total_tables += 1
    return tables_out, total_tables