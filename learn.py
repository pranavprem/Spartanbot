from db import spartandb
from PyDictionary import PyDictionary
from learner import learner

read_file = open("subjects.txt","r")
keywords = read_file.read().split(", ")
dbclient = spartandb()
dictionary = PyDictionary()
for keyword in keywords:
    dbclient.insert_subject(keyword.lower())
read_file.close()

read_file = open("objects.txt","r")
keywords = read_file.read().split(", ")
dbclient = spartandb()
dictionary = PyDictionary()
for keyword in keywords:
    dbclient.insert_object(keyword.lower())
    for key in keyword.split(" "):
        if dictionary.synonym(key) is not None:
            for synonym in dictionary.synonym(key):
                dbclient.insert_object(synonym)

learner_mod = learner()
learner_mod.read()

#print dbclient.get_keywords()   