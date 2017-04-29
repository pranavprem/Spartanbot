import sentence-engine
import db

class create_collection(object):

	def __init__(self):
		self.dbclient = db.spartandb()
		self.engine = sentence-engine.sentence_engine()

	def insertCollection(self, sentence):
		ret_dict = {}
		ret_dict = self.engine.analyze(sentence)		
		self.dbclient.insert(ret_dict)