from db import LocalBackend, MongoBackend, select_database, spartandb


class FakeCursor(object):
    def __init__(self, docs):
        self.docs = docs

    def __iter__(self):
        return iter(self.docs)


class FakeCollection(object):
    def __init__(self):
        self.docs = []

    def find(self):
        return FakeCursor(self.docs)

    def insert_one(self, doc):
        stored = dict(doc)
        stored["_id"] = "id-%d" % (len(self.docs) + 1)
        self.docs.append(stored)
        return stored

    def replace_one(self, filt, doc):
        for index, existing in enumerate(self.docs):
            if existing.get("_id") == filt["_id"]:
                self.docs[index] = dict(doc)
                return


class FakeMongoDB(object):
    def __init__(self):
        self.subjects = FakeCollection()
        self.objects = FakeCollection()
        self.greensheet = FakeCollection()


class FakeClient(object):
    def __init__(self, default=None, error=None):
        self.default = default
        self.error = error
        self.names = {}

    def __getitem__(self, name):
        self.names.setdefault(name, "db:%s" % name)
        return self.names[name]

    def get_default_database(self):
        if self.error:
            raise self.error
        return self.default


def test_local_store_dedupes_keywords_and_reads_sentences(tmp_path):
    store = LocalBackend(str(tmp_path / "nested" / "knowledge.json"))
    store.insert_subject(" Sithu ")
    store.insert_subject("sithu")
    store.insert_subject("")
    store.insert_object("Office")
    store.insert({"keywords": ["office"], "sentence": "ENG 281"})
    assert store.get_subjects() == ["sithu"]
    assert store.get_objects() == ["office"]
    assert store.read() == [{"keywords": ["office"], "sentence": "ENG 281"}]


def test_spartandb_uses_the_local_backend_without_a_uri():
    store = spartandb()
    assert store.backend_name == "local"
    store.insert_subject("cmpe273")
    assert spartandb().get_subjects() == ["cmpe273"]


def test_select_database_preserves_the_mlab_name():
    from pymongo.errors import ConfigurationError

    client = FakeClient(error=ConfigurationError("no database in URI"))
    assert select_database(client) == "db:heroku_jrt9gnq3"


def test_select_database_prefers_mongodb_db(monkeypatch):
    monkeypatch.setenv("MONGODB_DB", "spartan")
    client = FakeClient(default="from-uri")
    assert select_database(client) == "db:spartan"


def test_select_database_uses_the_uri_database():
    client = FakeClient(default="from-uri")
    assert select_database(client) == "from-uri"


def test_mongo_backend_appends_keywords_with_replace_one():
    backend = MongoBackend.__new__(MongoBackend)
    backend.db = FakeMongoDB()
    backend.insert_subject("Sithu")
    backend.insert_subject("sithu")
    backend.insert_subject("Aung")
    assert backend.get_subjects() == ["sithu", "aung"]
    assert backend.db.subjects.docs[0]["_id"] == "id-1"
    backend.insert({"keywords": ["a"], "sentence": "one"})
    assert backend.read()[0]["sentence"] == "one"
