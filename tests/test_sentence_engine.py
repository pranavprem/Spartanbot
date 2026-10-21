from sentence_engine import sentence_engine


class MemoryDB(object):
    def __init__(self):
        self.subjects = ["CMPE 273", "Sithu"]
        self.objects = ["office", "instructor"]

    def get_subjects(self):
        return self.subjects

    def get_objects(self):
        return self.objects


class Identity(object):
    def lemmatize(self, word):
        return word


def test_subjects_match_as_substrings_and_objects_add_synonyms():
    engine = sentence_engine(
        dbclient=MemoryDB(),
        synonyms=lambda word: ["teacher"] if word == "instructor" else None,
        lemmatizer=Identity(),
        tokenize=str.split,
    )
    result = engine.analyze("Where is Sithu's instructor office for CMPE 273?")
    assert "sithu" in result["keywords"]
    assert "cmpe 273" in result["keywords"]
    assert "instructor" in result["keywords"]
    assert "office" in result["keywords"]
    assert "teacher" in result["keywords"]
    assert result["sentence"].startswith("Where")
