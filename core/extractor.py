from core.extractor_linesearch import extract_tables as ex_linesearch
from core.extractor_tabula import extract_tables as ex_tabula
from core.extractor_camelot import extract_tables as ex_camelot
import logging


def extraction_methods_names() -> list:
    return ['tabula', 'camelot', 'linesearch', 'tabula_and_linesearch', 'tab2know']


def method_from_name(name: str):

    def tabula_and_linesearch(filename) -> list:
        tabs1 = ex_tabula(filename)
        tabs2 = ex_linesearch(filename)
        # merge and remove duplicates
        tabs = tabs1 + tabs2
        return tabs

    if name == 'tabula':
        return ex_tabula
    elif name == 'camelot':
        return ex_camelot
    elif name == 'tab2know':
        raise Exception("MEthod not implemented here")
    elif name == 'linesearch':
        return ex_linesearch
    elif name == 'tabula_and_linesearch':
        return extract_tables_joined
    else:
        raise Exception("Wrong method given: {}".format(name))


def extract_tables_joined(filename: str):
    tables = []
    tabs1 = ex_tabula(filename)
    tabs2 = ex_linesearch(filename)
    # merge and remove duplicates
    tables = [ *tabs1, *tabs2]
    return tables


def extract_tables(filename:str, method_used='tabula_and_linesearch'):
    method_to_use = method_from_name(method_used)
    tables = method_to_use(filename)
    return tables


