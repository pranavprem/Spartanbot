
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
    def insert_subjects(self,data):
        self.db.subjects.insert_one(data)
    def get_subjects(self):
        ret_sub = []
        for sub in self.db.greensheet.find():
            ret_sub.append(sub)
        return ret_sub
    def insert_objects(self,data):
        self.db.obj.insert_one(data)
    def get_objects(self):
        ret_ob=[]
        for ob in self.db.greensheet.find():
            ret_ob.append(ob)
        return ret_ob