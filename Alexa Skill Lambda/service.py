"""Alexa skill that asks the Spartanbot HTTP endpoint a course question.

Adapted from Amazon's color-picker sample. The skill calls
``/alexa_endpoint/<question>`` and speaks the plain-text body. The 2017
deployment used pycurl against a Heroku app. The URL is
``ALEXA_BACKEND_URL`` and defaults to that Heroku host, which is almost
certainly gone; point it at a running ``twilio_handle.py`` to use the skill.
"""

import json
import os
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen

DEFAULT_BACKEND = "https://shrouded-ocean-49421.herokuapp.com/alexa_endpoint/"


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output,
        },
        "card": {
            "type": "Simple",
            "title": "SessionSpeechlet - " + title,
            "content": "SessionSpeechlet - " + output,
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text,
            },
        },
        "shouldEndSession": should_end_session,
    }


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response,
    }


def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Yo"
    reprompt_text = "Ask me a question about 273 class"
    should_end_session = False
    return build_response(
        session_attributes,
        build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session),
    )


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Have a nice day! "
    should_end_session = True
    return build_response(
        {},
        build_speechlet_response(card_title, speech_output, None, should_end_session),
    )


def backend_url():
    return os.environ.get("ALEXA_BACKEND_URL", DEFAULT_BACKEND)


def fetch_answer(question, opener=None):
    opener = opener or urlopen
    slug = quote(question.replace(" ", "_"), safe="")
    url = backend_url().rstrip("/") + "/" + slug
    with opener(url, timeout=8) as response:
        payload = response.read()
    return payload.decode("utf-8", "replace")


def set_color_in_session(intent, session):
    """Fetch the course answer. The name is kept from the Alexa sample."""
    card_title = intent.get("name", "QuestionIntent")
    session_attributes = {}
    should_end_session = False
    reprompt_text = "Ask a question starting with ask the bot"
    slot = intent.get("slots", {}).get("Question", {})
    question = slot.get("value") if isinstance(slot, dict) else None
    if question:
        try:
            speech_output = fetch_answer(question)
        except (URLError, TimeoutError, OSError, ValueError) as exc:
            speech_output = "Sorry, I could not reach the course bot."
            print("alexa backend unavailable: %s" % exc)
    else:
        speech_output = "Sorry. Didn't catch that."
    return build_response(
        session_attributes,
        build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session),
    )


def on_session_started(session_started_request, session):
    print(
        "on_session_started requestId="
        + session_started_request["requestId"]
        + ", sessionId="
        + session["sessionId"]
    )


def on_launch(launch_request, session):
    print(
        "on_launch requestId=" + launch_request["requestId"] + ", sessionId=" + session["sessionId"]
    )
    return get_welcome_response()


def on_intent(intent_request, session):
    print(
        "on_intent requestId=" + intent_request["requestId"] + ", sessionId=" + session["sessionId"]
    )

    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "QuestionIntent":
        return set_color_in_session(intent, session)
    if intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    if intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print(
        "on_session_ended requestId="
        + session_ended_request["requestId"]
        + ", sessionId="
        + session["sessionId"]
    )


def handler(event, context):
    """Route a LaunchRequest, IntentRequest, or SessionEndedRequest."""
    print(
        "event.session.application.applicationId="
        + event["session"]["application"]["applicationId"]
    )

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    if event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    if event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])
    return None


if __name__ == "__main__":
    event_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "event.json")
    with open(event_path, encoding="utf-8") as handle:
        event = json.load(handle)
    print(json.dumps(handler(event, None), indent=2))
