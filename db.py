
from pymongo import MongoClient
import os




class spartandb(object):
    
    def __init__(self):
        self.client = MongoClient(os.environ["MONGODB_URI"])
        self.db = self.client.SpartanData     
    
    def insert(self,data):
        self.db.greensheet.insert_one(data)
    
    def read(self):
        ret_obj=[]
        for obj in self.db.greensheet.find():
            ret_obj.append(obj)
        return ret_obj
    
    def insert_keyword(self,keyword):
        try:
            key_array = self.db.keywords.find().next()
            key_array["keywords"].append(keyword)
            self.db.keywords.save(key_array)
        except StopIteration:
            key_array=[]
            key_array.append(keyword)
            self.db.keywords.insert_one({"keywords":key_array})

    def get_keywords(self):
        keywords = []
        for obj in self.db.keywords.find():
            keywords.append(obj["keywords"])
        return keywords