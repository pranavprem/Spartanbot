"""Knowledge store for greensheet sentences and keyword lists.

MongoDB is used when ``MONGODB_URI`` is set, which is how the Heroku/mLab
deployment worked. With no URI, the same records are stored in a local JSON
file so learning and answering work without a database server. mLab itself
shut down years ago; point ``MONGODB_URI`` at any current MongoDB, or leave
it unset.
"""

import json
import os
import threading

from settings import setting

_LOCK = threading.Lock()
_ROOT = os.path.dirname(os.path.abspath(__file__))


def local_db_path():
    return setting(
        "SPARTANBOT_LOCAL_DB",
        default=os.path.join(_ROOT, "data", "knowledge.json"),
    )


def select_database(client):
    """Pick the Mongo database, preserving the 2017 mLab name as a last resort."""
    from pymongo.errors import ConfigurationError

    db_name = setting("MONGODB_DB")
    if db_name:
        return client[db_name]
    try:
        return client.get_default_database()
    except ConfigurationError:
        return client["heroku_jrt9gnq3"]


def _clean_keyword(keyword):
    return (keyword or "").strip().lower()


class LocalBackend(object):
    def __init__(self, path):
        self.path = path

    def _load(self):
        if not os.path.exists(self.path):
            return {"subjects": [], "objects": [], "greensheet": []}
        with open(self.path, encoding="utf-8") as handle:
            return json.load(handle)

    def _save(self, data):
        directory = os.path.dirname(self.path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")

    def insert(self, data):
        with _LOCK:
            store = self._load()
            store["greensheet"].append(
                {
                    "keywords": list(data.get("keywords", [])),
                    "sentence": data.get("sentence", ""),
                }
            )
            self._save(store)

    def read(self):
        return list(self._load().get("greensheet", []))

    def insert_object(self, keyword):
        self._insert_keyword("objects", keyword)

    def insert_subject(self, keyword):
        self._insert_keyword("subjects", keyword)

    def _insert_keyword(self, field, keyword):
        keyword = _clean_keyword(keyword)
        if not keyword:
            return
        with _LOCK:
            store = self._load()
            if keyword not in store[field]:
                store[field].append(keyword)
                self._save(store)

    def get_subjects(self):
        return list(self._load().get("subjects", []))

    def get_objects(self):
        return list(self._load().get("objects", []))


class MongoBackend(object):
    def __init__(self, uri):
        from pymongo import MongoClient

        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self.db = select_database(self.client)

    def insert(self, data):
        self.db.greensheet.insert_one(
            {
                "keywords": list(data.get("keywords", [])),
                "sentence": data.get("sentence", ""),
            }
        )

    def read(self):
        return list(self.db.greensheet.find())

    def insert_object(self, keyword):
        self._append_unique(self.db.objects, "objects", keyword)

    def insert_subject(self, keyword):
        self._append_unique(self.db.subjects, "subjects", keyword)

    def _append_unique(self, collection, field, keyword):
        keyword = _clean_keyword(keyword)
        if not keyword:
            return
        existing = None
        for obj in collection.find():
            existing = obj
        if existing is None:
            collection.insert_one({field: [keyword]})
            return
        values = list(existing.get(field, []))
        if keyword in values:
            return
        values.append(keyword)
        existing[field] = values
        collection.replace_one({"_id": existing["_id"]}, existing)

    def get_subjects(self):
        return self._keyword_list(self.db.subjects, "subjects")

    def get_objects(self):
        return self._keyword_list(self.db.objects, "objects")

    def _keyword_list(self, collection, field):
        keywords = []
        for obj in collection.find():
            keywords = obj[field]
        return keywords


class spartandb(object):
    def __init__(self):
        uri = setting("MONGODB_URI")
        if uri:
            self._backend = MongoBackend(uri)
            self.backend_name = "mongo"
        else:
            self._backend = LocalBackend(local_db_path())
            self.backend_name = "local"

    def insert(self, data):
        self._backend.insert(data)

    def read(self):
        return self._backend.read()

    def insert_object(self, keyword):
        self._backend.insert_object(keyword)

    def insert_subject(self, keyword):
        self._backend.insert_subject(keyword)

    def get_subjects(self):
        return self._backend.get_subjects()

    def get_objects(self):
        return self._backend.get_objects()
