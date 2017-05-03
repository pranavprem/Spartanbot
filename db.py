
from pymongo import MongoClient
import os




class spartandb(object):
    def __init__(self):
        self.client = MongoClient(os.environ["MONGODB_URI"])
        self.db = self.client.heroku_jrt9gnq3

    def insert(self,data):
        self.db.greensheet.insert_one(data)

    def read(self):
        ret_obj = []
        for obj in self.db.greensheet.find():
            ret_obj.append(obj)
        return ret_obj


    def insert_object(self,keyword):
        try:
            key_array = self.db.objects.find().next()
            key_array["objects"].append(keyword)
            self.db.objects.save(key_array)
        except StopIteration:
            key_array = []
            key_array.append(keyword)
            self.db.objects.insert_one({"objects":key_array})


    def insert_subject(self,keyword):
        try:
            key_array = self.db.subjects.find().next()
            key_array["subjects"].append(keyword)
            self.db.subjects.save(key_array)
        except StopIteration:
            key_array = []
            key_array.append(keyword)
            self.db.subjects.insert_one({"subjects":key_array})


    def get_subjects(self):
        keywords = []
        for obj in self.db.subjects.find():
            keywords = obj["subjects"]
        return keywords

    def get_objects(self):
        keywords = []
        for obj in self.db.objects.find():
            keywords = obj["objects"]
        return keywords
