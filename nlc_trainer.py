"""
this module gives training data for NLC
"""
from pymongo import MongoClient
import os




class nlc_trainer(object):
    def __init__(self):
        self.client = MongoClient(os.environ["MONGODB_URI"])
        self.db = self.client.SpartanData

    def train(self):
        datas = self.db.greensheet.find()
        response = ""
        file = open("training-data.csv","w+")
        for data in datas:
            for keyword in data["keywords"]:
                try:
                    file.write(response + keyword + "," + data["sentence"] +"\n")
                except:
                    print data["sentence"]
        file.write(response)
        file.close()