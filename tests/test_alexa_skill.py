import importlib.util
from pathlib import Path
from urllib.error import URLError


def load_service():
    path = Path(__file__).resolve().parents[1] / "Alexa Skill Lambda" / "service.py"
    spec = importlib.util.spec_from_file_location("alexa_service", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SERVICE = load_service()


def session(request):
    return {
        "session": {
            "new": True,
            "sessionId": "session-1",
            "application": {"applicationId": "amzn1.ask.skill.local"},
        },
        "request": request,
    }


def test_launch_says_yo():
    result = SERVICE.handler(session({"type": "LaunchRequest", "requestId": "req-1"}), None)
    assert result["response"]["outputSpeech"]["text"] == "Yo"


def test_question_intent_speaks_the_backend_body(monkeypatch):
    def fake_fetch(question, opener=None):
        return "Office hours are Wednesday"

    monkeypatch.setattr(SERVICE, "fetch_answer", fake_fetch)
    event = session(
        {
            "type": "IntentRequest",
            "requestId": "req-2",
            "intent": {
                "name": "QuestionIntent",
                "slots": {"Question": {"value": "where is the office"}},
            },
        }
    )
    result = SERVICE.handler(event, None)
    assert result["response"]["outputSpeech"]["text"] == "Office hours are Wednesday"


def test_missing_slot_does_not_crash():
    event = session(
        {
            "type": "IntentRequest",
            "requestId": "req-3",
            "intent": {"name": "QuestionIntent", "slots": {}},
        }
    )
    result = SERVICE.handler(event, None)
    assert result["response"]["outputSpeech"]["text"] == "Sorry. Didn't catch that."


def test_backend_failure_is_spoken(monkeypatch):
    def explode(question, opener=None):
        raise URLError("heroku app is gone")

    monkeypatch.setattr(SERVICE, "fetch_answer", explode)
    event = session(
        {
            "type": "IntentRequest",
            "requestId": "req-4",
            "intent": {"name": "QuestionIntent", "slots": {"Question": {"value": "office hours"}}},
        }
    )
    result = SERVICE.handler(event, None)
    assert "could not reach" in result["response"]["outputSpeech"]["text"]


def test_stop_intent_and_invalid_intent():
    stop = session(
        {
            "type": "IntentRequest",
            "requestId": "req-5",
            "intent": {"name": "AMAZON.StopIntent"},
        }
    )
    result = SERVICE.handler(stop, None)
    assert result["response"]["shouldEndSession"] is True
    import pytest

    with pytest.raises(ValueError):
        SERVICE.handler(
            session(
                {
                    "type": "IntentRequest",
                    "requestId": "req-6",
                    "intent": {"name": "ColorIntent"},
                }
            ),
            None,
        )


def test_fetch_answer_quotes_the_question(monkeypatch):
    monkeypatch.setenv("ALEXA_BACKEND_URL", "http://example.test/alexa_endpoint/")
    seen = {}

    class Body(object):
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return "ENG 281".encode("utf-8")

    def opener(url, timeout):
        seen["url"] = url
        return Body()

    assert SERVICE.fetch_answer("where is the office", opener=opener) == "ENG 281"
    assert seen["url"] == "http://example.test/alexa_endpoint/where_is_the_office"
