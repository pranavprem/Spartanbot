import db
from PyDictionary import PyDictionary


class sentence_engine(object):

    def __init__(self):
        self.dbclient = db.spartandb()
        self.dictionary = PyDictionary()
        

    def analyze(self, sentence):
        ret_dict={}
        pre_keywords = self.dbclient.get_keywords()
        keywords = []
        for word in sentence.split(" "):
            if word in pre_keywords:
                keywords.append(word)
                keywords.append(self.dictionary.synonym(word))
            
        ret_dict["keywords"] = keywords
        ret_dict["sentence"] = sentence
        return ret_dict 
                        