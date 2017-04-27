import db
from PyDictionary import PyDictionary


class sentence_engine(object):

    def __init__(self):
        self.dbclient = db.spartandb()
        self.dictionary = PyDictionary()
        

    def analyze(self, sentence):
        ret_dict={}
        pre_objects = self.dbclient.get_objects()
        pre_subjects = self.dbclient.get_subjects()
        objects = []
        subjects = []
        for word in sentence.split(" "):
            if word in pre_objects:
                objects.append(word)
                objects.append(self.dictionary.synonym(word))
            if word in pre_subjects:
                subjects.append(word)
                subjects.append(self.dictionary.synonym(word))
        
        ret_dict["objects"] = objects
        ret_dict["subjects"] = subjects
        ret_dict["sentence"] = sentence
        return ret_dict 
                        