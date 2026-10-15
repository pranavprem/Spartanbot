"""Rank greensheet sentences against a question's keywords.

The confidence is the size of the overlap divided by the longer keyword list,
times 100. Sentences in the top quarter of that confidence range are returned,
highest first. The 2017 README described dividing by the shorter list; the
code has always divided by the longer one, and that is what still runs.
"""

from db import spartandb


class analyzer(object):
    def __init__(self, dbclient=None):
        self.dbclient = dbclient if dbclient is not None else spartandb()

    def score(self, list1, list2):
        score = 0.0
        for element in list1:
            if element in list2:
                score = score + 1.0
        if len(list1) == 0 or len(list2) == 0:
            return 0
        if len(list1) >= len(list2):
            return (score / len(list1)) * 100
        return (score / len(list2)) * 100

    def analyze(self, obj):
        greensheet = self.dbclient.read()
        response = ""
        matches = []
        maximum = 0.0
        minimum = 100.0
        for element in greensheet:
            match = {}
            confidence = self.score(obj["keywords"], element["keywords"])
            if confidence > 0:
                match["confidence"] = confidence
                match["sentence"] = element["sentence"]
                matches.append(match)
                if match["confidence"] < minimum:
                    minimum = match["confidence"]
                if match["confidence"] > maximum:
                    maximum = match["confidence"]

        threshold = maximum - ((maximum - minimum) / 4)
        matches = sorted(matches, key=lambda item: item["confidence"], reverse=True)

        for match in matches:
            if match["confidence"] >= threshold:
                response = response + "\n" + match["sentence"]

        return response
