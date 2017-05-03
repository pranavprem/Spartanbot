import json
import requests
from watson_developer_cloud import NaturalLanguageClassifierV1

class nlc_module(object):

    def __init__(self):
        self.natural_language_classifier = NaturalLanguageClassifierV1(
            username='1307bdf3-b9b4-4831-ac7c-7ad46c9e18fd',password='3KKFgtr4iNMh')

    def classify(self, sentence):
        classes = self.natural_language_classifier.classify('90e7b4x199-nlc-49477', sentence)
        return json.dumps(classes["top_class"], indent=2)