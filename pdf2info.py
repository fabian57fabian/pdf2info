import tabula
import logging
logging.getLogger('tabula').setLevel(logging.CRITICAL)
import os


def extract_from_pdf(src_doc: str, out_folder: str) -> (bool, int):
    """
    Given a pdf filename, extracts tables saving them as csv in output dir.
    :param src_doc:
    :param out_folder:
    :return: tuple(bool, int) Extraction result and number of tables extracted.
    """
    if not os.path.exists(src_doc):
        logging.error("Input pdf does not exist: " + str(src_doc))
        return False, 0
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    file_name = os.path.basename(src_doc)
    logging.info("processing " + file_name)

    # Tabula:
    try:
        tables = tabula.read_pdf(src_doc, pages="all")
    except Exception as e:
        logging.error("Skipping because error opening: "+str(e))
        return False, 0
    logging.debug("Found {} tables with tabula".format(len(tables)))
    for i, table in enumerate(tables):
        out_path = os.path.join(out_folder, "{}_{}.csv".format(file_name[:-4], i))
        table.to_csv(out_path)
    return True, len(tables)


def extract_from_dir(src_dir, out_folder) -> (int, int, int):
    """
    Given a folder, extracts all tables in out dir from all *.pdf files.
    :param src_dir:
    :param out_folder:
    :return: Total tables extracted, # of pdfs with errors on read, total pdf analyzed
    """
    if not os.path.exists(src_dir):
        logging.error("Input dir does not exist: " + str(src_dir))
        return False
    total_tables, errored_pdfs, tot_pdf = 0, 0, 0
    for file in os.listdir(src_dir):
        if file.endswith(".pdf"):
            tot_pdf += 1
            fn = os.path.join(src_dir, file)
            res, num = extract_from_pdf(fn, out_folder)
            if res: total_tables += num
            if not res: errored_pdfs += 1
    return total_tables, errored_pdfs, tot_pdf
