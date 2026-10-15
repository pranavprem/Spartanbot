"""Split a sentence into the subjects and objects the scorer compares.

Subjects are the proper-noun style terms in ``subjects.txt`` (and anything
learned later) and match as substrings. Objects are the attribute words in
``objects.txt`` and match as lemmatized tokens. Synonyms of a matched object
are added to the keyword set.

PyDictionary used to supply those synonyms by scraping dictionary sites. That
scraper has been broken for years, so synonyms now come from NLTK WordNet's
first synset, which is the same idea: one dictionary sense, not a new search
service.
"""

import nltk
from nltk.corpus import wordnet as wn

from nltk_setup import ensure_nltk_data


def wordnet_synonyms(word):
    """Return lemmas for the first WordNet sense, or None when there are none."""
    ensure_nltk_data()
    synsets = wn.synsets(word)
    if not synsets:
        return None
    names = []
    for lemma in synsets[0].lemmas():
        name = lemma.name().replace("_", " ").lower()
        if name != word.lower() and name not in names:
            names.append(name)
    return names or None


class sentence_engine(object):
    def __init__(self, dbclient=None, synonyms=None, lemmatizer=None, tokenize=None):
        self.dbclient = dbclient
        self.synonyms = synonyms
        self._lemmatizer = lemmatizer
        self._tokenize = tokenize

    def _db(self):
        if self.dbclient is None:
            from db import spartandb

            self.dbclient = spartandb()
        return self.dbclient

    def analyze(self, sentence):
        try:
            return self._analyze(sentence)
        except LookupError as exc:
            raise LookupError(
                "NLTK data is missing (%s). Run: "
                "python -m nltk.downloader punkt_tab wordnet omw-1.4" % exc
            ) from exc

    def _analyze(self, sentence):
        if self._tokenize is None or self._lemmatizer is None or self.synonyms is None:
            ensure_nltk_data()
        tokenize = self._tokenize or nltk.tokenize.word_tokenize
        lemmatizer = self._lemmatizer or nltk.stem.WordNetLemmatizer()
        synonyms_for = self.synonyms or wordnet_synonyms

        ret_dict = {}
        lowercase_sen = sentence.lower()
        tokens = tokenize(lowercase_sen)
        lowercase_sen_lem = [lemmatizer.lemmatize(word) for word in tokens]
        dbclient = self._db()
        pre_subjects = dbclient.get_subjects()
        pre_objects = [obj.lower() for obj in dbclient.get_objects()]
        keywords = []

        for word in pre_subjects:
            if word.lower() in lowercase_sen:
                keywords.append(word.lower())

        for word in lowercase_sen_lem:
            if word.lower() in pre_objects:
                keywords.append(word.lower())
                synonyms = synonyms_for(word)
                if synonyms is not None:
                    for synonym in synonyms:
                        keywords.append(synonym.lower())

        ret_dict["keywords"] = list(set(keywords))
        ret_dict["sentence"] = sentence
        return ret_dict
