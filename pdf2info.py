import camelot
import tabula

import os


def extract_from_pdf(src_doc: str, out_folder: str) -> bool:
    if not os.path.exists(src_doc):
        print("Input pdf does not exist: " + str(src_doc))
        return False
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    file_name = os.path.basename(src_doc)
    print("processing " + file_name)

    # Camelot:
    tables = camelot.read_pdf(src_doc)
    print("Found {} tables with camelot".format(len(tables)))
    for i, table in enumerate(tables):
        out_path = os.path.join(out_folder, "{}_{}.csv".format(file_name[:-4], i))
        table.to_csv(out_path)

    if len(tables) == 0:
        # Tabula:
        tables = tabula.read_pdf(src_doc, pages="all")
        print("Found {} tables with tabula".format(len(tables)))
        for i, table in enumerate(tables):
            out_path = os.path.join(out_folder, "{}_{}.csv".format(file_name[:-4], i))
            table.to_csv(out_path)

    return False


if __name__ == '__main__':
    src_doc = "../Papers/ICPR2022_GeVi.pdf"
    out_folder = "out"
    extract_from_pdf(src_doc, out_folder)
