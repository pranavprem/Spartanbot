"""Store one remembered sentence after the bot asks for a better answer."""

import db
import sentence_engine


class db_collection(object):
    def __init__(self, dbclient=None, engine=None):
        self.dbclient = dbclient if dbclient is not None else db.spartandb()
        if engine is None:
            engine = sentence_engine.sentence_engine(dbclient=self.dbclient)
        self.engine = engine

    def insertCollection(self, sentence):
        try:
            ret_dict = self.engine.analyze(sentence)
        except LookupError:
            ret_dict = {"keywords": [], "sentence": sentence}
        self.dbclient.insert(ret_dict)
