"""One-shot loader for subjects, objects, their synonyms, and the greensheet.

Run ``python learn.py`` once before asking greensheet questions. It is not a
long-running worker. Re-running it does not duplicate keyword lists; it does
append greensheet sentences again.
"""

import os
import sys

from db import spartandb
from learner import learner
from nltk_setup import ensure_nltk_data
from sentence_engine import wordnet_synonyms

_ROOT = os.path.dirname(os.path.abspath(__file__))


def _load_terms(filename):
    path = os.path.join(_ROOT, filename)
    with open(path, encoding="utf-8") as handle:
        terms = []
        for word in handle.read().split(","):
            word = word.strip().lower()
            if word and word not in terms:
                terms.append(word)
        return terms


def load_vocabulary(dbclient=None):
    dbclient = dbclient or spartandb()
    ensure_nltk_data()
    for keyword in _load_terms("subjects.txt"):
        dbclient.insert_subject(keyword)
    for keyword in _load_terms("objects.txt"):
        dbclient.insert_object(keyword)
        for key in keyword.split(" "):
            synonyms = wordnet_synonyms(key)
            if synonyms is not None:
                for synonym in synonyms:
                    dbclient.insert_object(synonym)
    return dbclient


def main():
    try:
        dbclient = load_vocabulary()
        learner().read()
    except LookupError as exc:
        print(exc)
        print("Run: python -m nltk.downloader punkt_tab wordnet omw-1.4")
        return 1
    print(
        "Learned %d sentences, %d subjects, %d objects (%s store)."
        % (
            len(dbclient.read()),
            len(dbclient.get_subjects()),
            len(dbclient.get_objects()),
            dbclient.backend_name,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
