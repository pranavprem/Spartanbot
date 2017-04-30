
from pymongo import MongoClient
import os




class spartandb(object):
    def __init__(self):
        self.client = MongoClient(os.environ["MONGODB_URI"])
<<<<<<< HEAD
        self.db = self.client.SpartanData

    def insert(self,data):
        self.db.greensheet.insert_one(data)

=======
        self.db = self.client.SpartanData     
    
    def insert(self,data):
        self.db.greensheet.insert_one(data)
    
>>>>>>> d9095c460ef31f254aa521e0574b993e06800e55
    def read(self):
        ret_obj = []
        for obj in self.db.greensheet.find():
            ret_obj.append(obj)
        return ret_obj
<<<<<<< HEAD

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
=======
    
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
>>>>>>> d9095c460ef31f254aa521e0574b993e06800e55
