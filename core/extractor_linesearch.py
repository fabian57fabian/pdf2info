from typing import Optional, List
import tempfile
import logging
import os

import pandas as pd

import pdfbox

from core.analyze_pdfminer import find_pdfminer_interesting_lines

p = None

def read_and_delete_file(path) -> Optional[List[str]]:
    try:
        with open(path, 'r') as file:
            return file.read().splitlines()
    except Exception as e:
        logging.error("Got error while reading: " + str(e))
        return None

def str_has_digit(l: str):
    return l.replace('+','').replace('-','').replace('.','').replace(' ','').replace(')','').replace('(','').replace(',','').replace('%','').replace('±','').isdigit()

def find_numbers_in_line(line):
    line_words = line.split(' ')
    digits_elements = [l for l in line_words if str_has_digit(l)]
    return line_words, digits_elements

def extract_tables(path):
    global p
    tmp_fn = tempfile.NamedTemporaryFile().name + ".txt"
    if p is None:
        p = pdfbox.PDFBox()
    p.extract_text(path, output_path=tmp_fn)
    text = read_and_delete_file(tmp_fn)

    # Get intereting words by analyzing html
    interesting_words = find_pdfminer_interesting_lines(path)

    tables = []
    remaining_text = []
    # Iterate thru text
    for i in range(len(text)):
        remaining_text.append(i)
        # if we arrive at a line starting with "Table X", it is the caption.
        curr_line = text[i].lower()
        #if "table" in curr_line.lower():
        #    a = 4
        arrived_at_table = False
        arrived_at_table = curr_line.startswith("table") or curr_line.startswith('tab.')

        if not arrived_at_table:
            words_found = sum([1 for w in interesting_words if w in curr_line])
            if words_found > 0:
                arrived_at_table = True

        if arrived_at_table:
            logging.debug("Found one table with pdfBOX")
            current_table = []

            # iterate from i backwards max 50 lies
            last_added = True
            for table_is_before in [True, False]:
                for k in range(1, min(i, 50)):
                    next_index = i-k if table_is_before else i+k
                    if next_index in remaining_text:
                        remaining_text.remove(next_index)
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
                    if digits > 0 and not line_has_digits:
                        line_has_digits = str_has_digit(line_words[-1])
                    if line_has_digits:
                        # line with digits
                        current_table.insert(0, line)
                        added = True

                    if not added and k == 1:
                        # last line before table
                        current_table.insert(0, line)
                        added = True

                    if not added and not last_added:
                        current_table.insert(0, line) # insert just this one
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    path = "../analysis/DATASET/chunks/papers_chunk_1/2211.09259.pdf"
    tables = extract_tables(path)
    if tables is not None:
        for t in tables:
            print(t)
