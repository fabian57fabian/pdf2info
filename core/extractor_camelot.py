import camelot
import logging
logging.getLogger('camelot').setLevel(logging.CRITICAL)


def extract_tables(filename):
    tables_camelot = camelot.read_pdf(filename, pages="all")
    return [t.df for t in tables_camelot]
