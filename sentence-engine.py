import db
from PyDictionary import PyDictionary


class sentence_engine(object):

    def __init__(self):
        dbclient = db.spartandb()
        dictionary = PyDictionary()
        

    def analyze(self, sentence):
        ret_dict={}
        pre_objects = dbclient.get_objects()
        pre_subjects = dbclient.get_subjects()
        objects = []
        subjects = []
        for word in sentence.split(" "):
            if word in pre_objects:
                objects.append(word)
                objects.append(dictionary.synonym(word))
            if word in pre_subjects:
                subjects.append(word)
                subjects.append(dictionary.synonym(word))
        
        ret_dict["objects"] = objects
        ret_dict["subjects"] = subjects
        ret_dict["sentence"] = sentence
        return ret_dict 
                        