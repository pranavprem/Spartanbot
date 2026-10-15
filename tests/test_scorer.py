from scorer import analyzer


class MemoryDB(object):
    def __init__(self, rows):
        self.rows = rows

    def read(self):
        return self.rows


def test_score_divides_by_the_longer_list():
    scored = analyzer(dbclient=MemoryDB([]))
    assert scored.score(["a", "b", "c"], ["a", "b"]) == (2 / 3) * 100
    assert scored.score(["a"], ["a", "b", "c"]) == (1 / 3) * 100
    assert scored.score([], ["a"]) == 0
    assert scored.score(["a"], []) == 0


def test_threshold_keeps_the_top_quarter_of_the_range():
    rows = [
        {"keywords": ["instructor", "sithu"], "sentence": "best"},
        {"keywords": ["instructor"], "sentence": "mid"},
        {"keywords": ["unrelated"], "sentence": "miss"},
    ]
    # question keywords overlap 2/2 with best (100), 1/2 with mid (50), 0 with miss.
    result = analyzer(dbclient=MemoryDB(rows)).analyze({"keywords": ["instructor", "sithu"]})
    assert "best" in result
    assert "mid" not in result
    assert "miss" not in result
    assert result.index("best") < result.find("mid") or "mid" not in result
