import db
from PyDictionary import PyDictionary
import nltk
nltk.data.path.append("./nltk_data")



class sentence_engine(object):

    def __init__(self):
        self.dbclient = db.spartandb()
        self.dictionary = PyDictionary()
        self.lemmatizer = nltk.stem.WordNetLemmatizer()


    def analyze(self, sentence):
        ret_dict = {}
        lowercase_sen = sentence.lower()
        lowercase_sen_tok = [word.lower() for word in nltk.tokenize.word_tokenize(lowercase_sen)]
        lowercase_sen_lem = [self.lemmatizer.lemmatize(word) for word in lowercase_sen_tok]
        pre_subjects = self.dbclient.get_subjects()
        pre_objects = self.dbclient.get_objects()
        keywords = []

        for word in pre_subjects:
            if word.lower() in lowercase_sen:
                keywords.append(word.lower())

        for word in lowercase_sen_lem:
            if word.lower() in pre_objects:
                keywords.append(word.lower())
                if self.dictionary.synonym(word) is not None:
                    for synonyms in self.dictionary.synonym(word):
                        keywords.append(synonyms.lower())

        ret_dict["keywords"] = list(set(keywords))
        ret_dict["sentence"] = sentence
        return ret_dict
