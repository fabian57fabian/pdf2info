from core.extractor_linesearch import extract_tables as ex_linesearch
from core.extractor_tabula import extract_tables as ex_tabula
from core.extractor_camelot import extract_tables as ex_camelot
import logging


def extraction_methods_names() -> list:
    return ['tabula', 'camelot', 'linesearch', 'tab2know']


def method_from_name(name: str):
    if name == 'tabula':
        return ex_tabula
    elif name == 'camelot':
        return ex_camelot
    elif name == 'tab2know':
        raise Exception("MEthod not implemented here")
    elif name == 'linesearch':
        return ex_linesearch
    elif name == 'all':
        return extract_tables_all
    else:
        raise Exception("Wrong method given: {}".format(name))


def extract_tables_all(filename: str):
    tables = []
    for method_name in extraction_methods_names():
        method_to_use = method_from_name(method_name)
        tables_out = method_to_use(filename)
        # remove_double_tables
        tables += tables_out
    return tables


def extract_tables(filename:str, method_used='all'):
    method_to_use = method_from_name(method_used)
    tables = method_to_use(filename)
    return tables


