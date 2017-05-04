from sentence_engine import sentence_engine
from scorer import analyzer


class custom_solution(object):
    def __init__(self):
        pass

    def doCustom(self, command):
        engine = sentence_engine()
        analysis = analyzer()
        test = engine.analyze(command)
        return analysis.analyze(test)
