# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pdfminer.high_level;
from pdfminer.layout import *;
import sqlite3

# %%
def convertPDF(pdf_name):
    # global pages
    # global table
    pages = list(pdfminer.high_level.extract_pages(pdf_name, laparams=LAParams(line_margin=0.0001)))

    rows = extractRows(pages)
    tables = rowsToTables(rows)
    return tables

# %%
class RawRow:
    def __init__(self, y, items=[]):
        self.y = y
        self.items = items
    
    def __str__(self):
        return "Row at " + str(self.y) + ": " + str(self.items)


def get_cleaned_text(element):
    return element.get_text().splitlines()[0].strip()


def extractRows(pages):
    def insertToRow(rows, item, ypos):
        matchingRow = None
        for group in rows:
            if group.y == ypos:
                matchingRow = group
                break
        if matchingRow == None:
            rows.append(RawRow(ypos, [item]))
        else:
            matchingRow.items.append(item)

    offset = 0
    rows = []
    for page in pages:
        offset += page.height
        for element in page:
            if isinstance(element, LTText):
                text = get_cleaned_text(element)
                if text:
                    insertToRow(rows, element, offset - element.y1)

    return sorted(rows, key=lambda r: r.y)

# %%
class Table:
    def __init__(self, title, date, columns_x=[], headers = []):
        self.title = title
        self.date = date
        self.columns_x = columns_x
        self.headers = headers
        self.rows = []

    def insertRowItems(self, items):
        row = {}
        for element in items:
            matchingColumnIndex = min(range(0, len(self.columns_x)), key=lambda i: abs(
                self.columns_x[i] - element.x0))
            row[self.headers[matchingColumnIndex]] = get_cleaned_text(element)
        
        self.rows.append(row)
        return row

    def __str__(self):
        row_strings = [",".join([key + "=" + row[key] for key in row]) for row in self.rows]
        return "Table: "+  " Date: " +  "\n" + "\n".join(row_strings)
    # table.title
def rowsToTables(rows):
    i = 0
    titles = []
    tables = []
    currentTable = None

    for row in rows:
        if len(row.items) == 1:
            text = get_cleaned_text(row.items[0])
            currentTable = None
            titles.append(text)
        if len(row.items) > 1:
            if currentTable:
                currentTable.insertRowItems(row.items)
            else:
                title = min(titles, key=len)
                date = titles[-1].replace(".", "-").strip("modifrMODIFR").strip()
                titles = []
                column_positions = list(map(lambda e: e.x0, row.items))
                column_titles = list(map(lambda e: get_cleaned_text(e), row.items))
                currentTable = Table(title, date, column_positions, column_titles)
                tables.append(currentTable)

    return tables


# %%
# convertPDF("getpdf.php.pdf", "C:\\Users\\Per\\Documents\\whgonline-random-zeug\\Django_Projekte\\Vertretungsplan\\db.sqlite3")