"""Read the CMPE 273 greensheet into the knowledge store.

Tables are three columns and become ``"<field> for <subject> is <value>"``.
A paragraph that starts with ``:`` drops the colons. A paragraph that
contains `` ** `` turns that marker into the word "is".
"""

import os

from docx import Document

_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DOCUMENT = os.path.join(_ROOT, "cmpe273-greensheet.docx")


class learner(object):
    def __init__(self, document_path=None, inserter=None):
        path = document_path or DEFAULT_DOCUMENT
        self.document = Document(path)
        if inserter is not None:
            self.insert = inserter
        else:
            from db_collection import db_collection

            self.insert = db_collection()

    def read(self):
        for table in self.document.tables:
            for row_index in range(len(table.rows)):
                sentence = "%s for %s is %s" % (
                    table.cell(row_index, 0).text,
                    table.cell(row_index, 1).text,
                    table.cell(row_index, 2).text,
                )
                self.insert.insertCollection(sentence)

        for paragraph in self.document.paragraphs:
            text = paragraph.text
            if text.startswith(":"):
                self.insert.insertCollection(text.replace(":", ""))
            elif " ** " in text:
                self.insert.insertCollection(text.replace("**", "is"))
            else:
                self.insert.insertCollection(text)
