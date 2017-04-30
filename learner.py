import db-collection
from docx import Document
from docx.shared import Inches

class read_file(object):

	def __init__(self):
		self.document = Document("/cmpe273-greensheet.docx")
		self.i = 0
		self.insert = db-collection.create_collection()
		
	def read():
		for table in self.document.tables:
			self.i = 0
			while(self.i < len(table.rows)):
				self.insert.insertCollection("%s for %s is %s" % (table.cell(i,0).text.encode('utf-8'), table.cell(i,1).text.encode('utf-8'), table.cell(i,2).text.encode('utf-8')))
				self.i = self.i + 1
		
		for paragraph in self.document.paragraphs:
			if (paragraph.text.startswith(":")):
				self.insert.insertCollection(paragraph.text.encode('utf-8').replace(":", ""))
			elif (" ** " in paragraph.text):
				self.insert.insertCollection(paragraph.text.encode('utf-8').replace("**", "is"))
			else :
				self.insert.insertCollection(paragraph.text.encode('utf-8'))