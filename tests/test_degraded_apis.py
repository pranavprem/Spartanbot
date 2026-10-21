import requests

from db import spartandb
from google_solution import google_solution
from nlc_module import nlc_module
from nlc_trainer import nlc_trainer


def test_google_search_is_empty_without_keys():
    assert google_solution().google_search("office hours", num=1) == []


def test_google_search_swallows_client_errors(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
    monkeypatch.setenv("GOOGLE_CSE_ID", "test-cx")

    def explode(*args, **kwargs):
        raise RuntimeError("custom search retired for this key")

    import googleapiclient.discovery

    monkeypatch.setattr(googleapiclient.discovery, "build", explode)
    assert google_solution().google_search("office hours") == []


def test_watson_nlc_is_empty_without_credentials():
    assert nlc_module().classify("who teaches 273") == ""


def test_watson_nlc_is_empty_when_the_endpoint_fails(monkeypatch):
    monkeypatch.setenv("bluemix_username", "user")
    monkeypatch.setenv("bluemix_password", "secret")
    monkeypatch.setenv("WATSON_CLASSIFIER_ID", "classifier-1")

    def explode(*args, **kwargs):
        raise requests.ConnectionError("retired")

    monkeypatch.setattr("nlc_module.requests.post", explode)
    assert nlc_module().classify("who teaches 273") == ""


def test_watson_nlc_returns_a_confident_class(monkeypatch):
    monkeypatch.setenv("WATSON_USERNAME", "user")
    monkeypatch.setenv("WATSON_PASSWORD", "secret")
    monkeypatch.setenv("WATSON_CLASSIFIER_ID", "classifier-1")

    class FakeResponse(object):
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "top_class": "instructor",
                "classes": [{"confidence": 0.9, "class_name": "instructor"}],
            }

    monkeypatch.setattr("nlc_module.requests.post", lambda *args, **kwargs: FakeResponse())
    assert nlc_module().classify("who teaches") == "instructor"


def test_nlc_trainer_quotes_commas(tmp_path):
    store = spartandb()
    store.insert({"keywords": ["instructor"], "sentence": "Sithu Aung, ENG 281"})
    path = nlc_trainer(dbclient=store).train(str(tmp_path / "training-data.csv"))
    text = open(path, encoding="utf-8").read()
    assert "instructor" in text
    assert "Sithu Aung, ENG 281" in text
