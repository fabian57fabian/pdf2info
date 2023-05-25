from typing import Optional, List
import pdfbox
import tempfile
import pandas as pd
import logging
import os

p = None

def read_and_delete_file(path) -> Optional[List[str]]:
    try:
        with open(path, 'r') as file:
            return file.read().splitlines()
    except Exception as e:
        logging.error("Got error while reading: " + str(e))
        return None

def find_numbers_in_line(line):
    line_words = line.split(' ')
    digits_elements = [l for l in line_words if l.replace('.','',1).replace('%','').replace('±','').isdigit()]
    return line_words, digits_elements

def load_tables_manually(path):
    global p
    tmp_fn = tempfile.NamedTemporaryFile().name + ".txt"
    if p is None:
        p = pdfbox.PDFBox()
    p.extract_text(path, output_path=tmp_fn)
    text = read_and_delete_file(tmp_fn)

    tables = []

    # Iterate thru text
    for i in range(len(text)):
        # if we arrive at a line starting with "Table X", it is the caption.
        curr_line = text[i].lower()
        #if "table" in curr_line.lower():
        #    a = 4
        if curr_line.startswith("table") or curr_line.startswith('tab.'):
            logging.debug("Found one table with pdfBOX")
            current_table = []

            # iterate from i backwards max 50 lies
            last_added = True
            for table_is_before in [True, False]:
                for k in range(1, min(i, 50)):
                    next_index = i-k if table_is_before else i+k
                    if next_index < 0 or next_index >= len(text):
                        break
                    line = text[next_index]
                    # a new table arrived
                    if line.startswith("table") or line.startswith('tab.'):
                        break
                    line_words, digits_elements = find_numbers_in_line(line)
                    added = False
                    # we are inside table if at least 1/3 of words are numbers
                    # we also allow one line skip and first line above table
                    words, digits = len(line_words), len(digits_elements)
                    line_has_digits = False
                    if digits > 1:
                        if words == 2 and digits >= 1:
                            line_has_digits = True
                        if words == 3 and digits >= 1:
                            line_has_digits = True
                        if words == 4 and digits >= 1:
                            line_has_digits = True
                        else:
                            line_has_digits = digits >= words // 3 or digits >= 2
                    if line_has_digits:
                        # line with digits
                        current_table.insert(0, line)
                        added = True

                    if not added and k == 1:
                        # last line before table
                        current_table.insert(0, line)
                        added = True

                    if not added and not last_added:
                        break

                    if not added:
                        current_table.insert(0, line)
                        last_added = False
                if len(current_table) > 1:
                    current_table = [l.replace(' ', ',') for l in current_table]
                    max_cols = max([line.count(',') for line in current_table])
                    for line in current_table:
                        line_commas = line.count(',')
                        if line_commas < max_cols:
                            for _ in range(max_cols-line_commas):
                                line += ','
                    tab = pd.DataFrame(current_table)
                    tables.append(tab)
    return tables


# results
#tabula: 							-> 64.41 %
#manual 'Table X' + digit					-> 67.75 %
#manual 'Table X' + float					-> 70.99 %
#manual 'Table X' + 'Tab. X' + float				-> 72.67 %
#manual 'Table X' + 'Tab. X' + least 3 numbs + float		-> 73.00 %
#manual 'Table X' + 'Tab. X' + least 2 numbs + 2,3 elements + float		-> 73.17 %
#manual 'Table X' + 'Tab. X' + backwards + least 2 numbs + 2,3 elements + float		-> 75.09 %

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    path = "../analysis/DATASET/chunks/papers_chunk_1/2211.09259.pdf"
    tables = load_tables_manually(path)
    if tables is not None:
        for t in tables:
            print(t)
