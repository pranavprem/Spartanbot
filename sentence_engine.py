import db
from PyDictionary import PyDictionary


class sentence_engine(object):

    def __init__(self):
        self.dbclient = db.spartandb()
        self.dictionary = PyDictionary()
        

    def analyze(self, sentence):
        ret_dict={}
        lowercase_sen = sentence.lower()
        pre_subjects = self.dbclient.get_subjects()
        pre_objects = self.dbclient.get_objects()
        keywords = []

        for word in lowercase_sen.split(" "):
            if word in pre_subjects:
                keywords.append(word)
            if word in pre_objects:
                keywords.append(word)
                if self.dictionary.synonym(word):
                    for synonyms in self.dictionary.synonym(word):
                        keywords.append(synonyms.lower())
                
            
        ret_dict["keywords"] = keywords
        ret_dict["sentence"] = sentence
        return ret_dict 
                        