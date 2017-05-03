import sentence_engine
import db

class db_collection(object):

	def __init__(self):
		self.dbclient = db.spartandb()
		self.engine = sentence_engine.sentence_engine()

	def insertCollection(self, sentence):
		ret_dict = {}
		ret_dict = self.engine.analyze(sentence)
		self.dbclient.insert(ret_dict)