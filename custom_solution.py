"""Greensheet retrieval: sentence engine, then the confidence scorer."""

from scorer import analyzer
from sentence_engine import sentence_engine


class custom_solution(object):
    def __init__(self, engine=None, analysis=None):
        self.engine = engine
        self.analysis = analysis

    def doCustom(self, command):
        engine = self.engine or sentence_engine()
        analysis = self.analysis or analyzer()
        test = engine.analyze(command)
        return analysis.analyze(test)
