import tabula
import logging
logging.getLogger('tabula').setLevel(logging.CRITICAL)


def extract_tables(filename):
    tables_tabula = tabula.read_pdf(filename, pages="all", multiple_tables=True)
    return tables_tabula


