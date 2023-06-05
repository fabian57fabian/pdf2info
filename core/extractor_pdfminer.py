import io
import logging

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def load_text_maually_pdfminer(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)



    fp.close()
    device.close()
    text = retstr.getvalue()
    retstr.close()
    return text


def extract_tables(path):
    from pprint import pprint
    from io import StringIO
    import re
    from pdfminer.high_level import extract_text_to_fp
    from pdfminer.layout import LAParams
    from lxml import html
    ID_LEFT_BORDER = 56
    ID_RIGHT_BORDER = 156
    QTY_LEFT_BORDER = 355
    QTY_RIGHT_BORDER = 455
    # Read PDF file and convert it to HTML
    output = StringIO()
    with open(path, 'rb') as pdf_file:
        extract_text_to_fp(pdf_file, output, laparams=LAParams(), output_type='html', codec=None)
    raw_html = output.getvalue()
    # Extract all DIV tags
    tree = html.fromstring(raw_html)
    divs = tree.xpath('.//div')
    # Sort and filter DIV tags
    filtered_divs = {'ID': [], 'Qty': []}
    for div in divs:
        # extract styles from a tag
        div_style = div.get('style')
        # print(div_style)
        # position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:292px; top:1157px; width:27px; height:12px;
        # get left position
        try:
            left = re.findall(r'left:([0-9]+)px', div_style)[0]
        except IndexError:
            continue
        # div contains ID if div's left position between ID_LEFT_BORDER and ID_RIGHT_BORDER
        if ID_LEFT_BORDER < int(left) < ID_RIGHT_BORDER:
            filtered_divs['ID'].append(div.text_content().strip('\n'))
        # div contains Quantity if div's left position between QTY_LEFT_BORDER and QTY_RIGHT_BORDER
        if QTY_LEFT_BORDER < int(left) < QTY_RIGHT_BORDER:
            filtered_divs['Qty'].append(div.text_content().strip('\n'))
    # Merge and clear lists with data
    data = []
    for row in zip(filtered_divs['ID'], filtered_divs['Qty']):
        if 'ID' in row[0]:
            continue
        data_row = {'ID': row[0].split(' ')[0], 'Quantity': row[1]}
        data.append(data_row)
    data = [d for d in data if len(d) > 1]
    return data



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    path = "../analysis/DATASET/chunks/papers_chunk_1/2211.09388.pdf"
    tables = extract_tables(path)
    if tables is not None:
        print(tables)