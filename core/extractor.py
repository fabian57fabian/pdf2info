import tabula
import logging
logging.getLogger('tabula').setLevel(logging.CRITICAL)

def extract_tables(filename):
    return tabula.read_pdf(filename, pages="all", multiple_tables=True)

