from core.extractor_linesearch import extract_tables as ex_linesearch
from core.extractor_tabula import extract_tables as ex_tabula
from core.extractor_camelot import extract_tables as ex_camelot
import logging


def extraction_methods_names() -> list:
    return ['tabula', 'camelot', 'linesearch', 'tabula_and_linesearch', 'camelot_and_linesearch', 'tab2know']


def method_from_name(name: str):
    if name == 'tabula':
        return ex_tabula
    elif name == 'camelot':
        return ex_camelot
    elif name == 'tab2know':
        raise Exception("MEthod not implemented here")
    elif name == 'linesearch':
        return ex_linesearch
    elif name == 'tabula_and_linesearch':
        return lambda filename: merge_tables(ex_tabula(filename), ex_linesearch(filename))
    elif name == 'camelot_and_linesearch':
        return lambda filename: merge_tables(ex_camelot(filename), ex_linesearch(filename))
    else:
        raise Exception("Wrong method given: {}".format(name))


def find_matching_table(tab, tabs:list):
    """
    Given a table (pandas Dataframe) and a list of tables, try to find if table is contained in list.
    MAy return None
    :param tab:
    :param tabs:
    :return:
    """
    thresh = .5
    for t in tabs:
        equal_cells = 0
        for (columnName, columnData) in t.items():
            for el in columnData.values:
                if el in tab:
                    equal_cells += 1
        if equal_cells / tab.size >= thresh:
            return t
    return None


def merge_tables(tabs1, tabs2):
    tables = []
    # merge and remove duplicates
    for tab_ls in tabs2:
        table_found = find_matching_table(tab_ls, tabs1)
        if table_found is None:
            # found new table, good
            tables.append(tab_ls)
        else:
            # decide between tabula table and linesearch table
            if table_found.size > tab_ls.size:
                tables.append(table_found)
                #tabs1.remove(table_found)
            else:
                tables.append(tab_ls)
    if len(tabs1) > 0:
        tables = tables + tabs1
    return tables


def extract_tables(filename:str, method_used='tabula_and_linesearch'):
    method_to_use = method_from_name(method_used)
    tables = method_to_use(filename)
    return tables


