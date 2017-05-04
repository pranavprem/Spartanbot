import db
from PyDictionary import PyDictionary


class sentence_engine(object):

    def __init__(self):
        self.dbclient = db.spartandb()
        self.dictionary = PyDictionary()


    def analyze(self, sentence):
        ret_dict = {}
        lowercase_sen = sentence.lower()
        pre_subjects = self.dbclient.get_subjects()
        pre_objects = self.dbclient.get_objects()
        keywords = []

        for word in pre_subjects:
            if word.lower() in lowercase_sen:
                keywords.append(word.lower())

        for word in pre_objects:
            if word.lower() in lowercase_sen:
                keywords.append(word.lower())
                if self.dictionary.synonym(word) is not None:
                    for synonyms in self.dictionary.synonym(word):
                        keywords.append(synonyms.lower())

        ret_dict["keywords"] = keywords
        ret_dict["sentence"] = sentence
        return ret_dict
                        