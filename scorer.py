from db import spartandb
from sentence_engine import sentence_engine

class analyzer(object):
    def __init__(self):
        self.dbclient = spartandb()
        self.engine = sentence_engine()
        

    def score(self, list1, list2):
        score =0.0
        #print list1
        #print "-----------"
        #print list2
        for element in list1:
            #print element+'---'
            #print (element in list2)
            if element in list2:
                print element
                score = score +1.0
        if len(list1) == 0 or len(list2)==0:
            return 0
        else:
            if len(list1)>=len(list2):
                return (score/len(list1))*100
            else:
                return (score/len(list2))*100

    def analyze(self, obj):
        #print "reached here"
        
        greensheet = self.dbclient.read()
        response = ""
        matches = []
        maximum=0.0
        minimum=100.0
        for element in greensheet:
            match={}
            confidence = self.score(obj["keywords"], element["keywords"])
            if confidence>0:
                match["confidence"]=confidence
                match["sentence"]=element["sentence"]
                matches.append(match)
                if match["confidence"]<minimum:
                    minimum=match["confidence"]
                if match["confidence"]>maximum:
                    maximum=match["confidence"]
        
        threshold = maximum-((maximum-minimum)/4)
        

        matches = sorted(matches, key = lambda k: k["confidence"], reverse=True)

        for match in matches:
            print match
            if match["confidence"]>=threshold:
                response = response+"\n"+match["sentence"]

        return response




