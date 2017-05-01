import db
from PyDictionary import PyDictionary


class sentence_engine(object):

    def __init__(self):
        self.dbclient = db.spartandb()
        self.dictionary = PyDictionary()
        

    def analyze(self, sentence):
        ret_dict={}
        #lowercase_sen = sentence.lower()
        pre_subjects = self.dbclient.get_subjects()
        pre_objects = self.dbclient.get_objects()
        subjects = []
        objects = []
        for word in sentence.split(" "):
            if word.lower() in pre_subjects:
                subjects.append(word)
            if word.lower() in pre_objects:
                objects.append(self.dictionary.synonym(word))
            
        ret_dict["subjects"] = subjects
        ret_dict["objects"] = objects
        ret_dict["sentence"] = sentence
        return ret_dict 
                        