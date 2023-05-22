import tabula
from core.extractor_pdfbox import load_tables_manually
import logging
logging.getLogger('tabula').setLevel(logging.CRITICAL)


def remove_double_tables(tables1, tables2):
    # TODO: make an algorythm and optimizie
    return tables1 + tables2


def extract_tables(filename):
    tables_tabula = tabula.read_pdf(filename, pages="all", multiple_tables=True)
    tables_pdfbox_manual = load_tables_manually(filename)
    res_tables = remove_double_tables(tables_tabula, tables_pdfbox_manual)
    return res_tables


