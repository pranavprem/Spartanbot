import db_collection
from docx import Document
from docx.shared import Inches
import os

class learner(object):

	def __init__(self):
		self.document = Document(os.path.join(os.getcwd(),"cmpe273-greensheet.docx"))
		self.insert = db_collection.db_collection()

	def read(self):
		for table in self.document.tables:
			i = 0
			while(i < len(table.rows)):
				self.insert.insertCollection("%s for %s is %s" % (table.cell(i, 0).text.encode('utf-8'),
				 table.cell(i, 1).text.encode('utf-8'), table.cell(i, 2).text.encode('utf-8')))
				i = i + 1

		for paragraph in self.document.paragraphs:
			self.insert.insertCollection(paragraph.text.encode('utf-8'))