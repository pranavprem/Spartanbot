from slack_sdk.socket_mode.request import SocketModeRequest

import spartanbot
import twilio_handle
from settings import clip_slack_text


class FakeWeb(object):
    def __init__(self):
        self.messages = []

    def chat_postMessage(self, channel, text):
        self.messages.append((channel, text))


class FakeSocket(object):
    def __init__(self):
        self.web_client = FakeWeb()
        self.acks = []

    def send_socket_mode_response(self, response):
        self.acks.append(response.envelope_id)


class Control(object):
    def find_solution(self, command):
        return "answer:" + command


def test_parse_slack_output_returns_the_mentioned_command():
    events = [
        {"text": "hello", "channel": "C0"},
        {"text": "<@U1> office hours", "channel": "C1"},
        {"text": "<@U1> ignored", "channel": "C2"},
    ]
    assert spartanbot.parse_slack_output(events, "<@U1>") == ("office hours", "C1")
    assert spartanbot.parse_slack_output([{"text": "no mention", "channel": "C1"}], "<@U1>") == (
        None,
        None,
    )


def test_socket_mode_acks_and_answers_an_app_mention():
    client = FakeSocket()
    request = SocketModeRequest(
        type="events_api",
        envelope_id="env-1",
        payload={"event": {"type": "app_mention", "text": "<@U1> do 2 + 2", "channel": "C9"}},
    )
    spartanbot.handle_socket_request(client, request, "<@U1>", Control())
    assert client.acks == ["env-1"]
    assert client.web_client.messages == [("C9", "answer:do 2 + 2")]


def test_dispatch_ignores_message_subtypes():
    web = FakeWeb()
    dispatch_event = spartanbot.dispatch_event
    dispatch_event(
        web,
        {"type": "message", "subtype": "bot_message", "text": "<@U1> hi", "channel": "C1"},
        "<@U1>",
        Control(),
    )
    assert web.messages == []


def test_clip_slack_text():
    assert clip_slack_text("short") == "short"
    clipped = clip_slack_text("x" * 4000)
    assert len(clipped) < 4000
    assert clipped.endswith("\n...")


def test_health_and_alexa_smalltalk():
    client = twilio_handle.app.test_client()
    assert client.get("/").get_data(as_text=True) == "Spartanbot is running."
    body = client.get("/alexa_endpoint/how_are_you").get_data(as_text=True)
    assert body == "I am good.Thankyou."


def test_twilio_refuses_an_open_relay_and_posts_an_answer():
    client = twilio_handle.app.test_client()
    assert client.post("/twilio", data={"From": "+1555", "Body": "hi"}).status_code == 403

    import os

    os.environ["user_number"] = "+15551212"
    posted = []

    class Slack(object):
        def chat_postMessage(self, channel, text):
            posted.append((channel, text))

    twilio_handle._slack = Slack()
    allowed = client.post("/twilio", data={"From": "+15551212", "Body": "how are you?"})
    assert allowed.status_code == 200
    assert posted[0] == ("#testonebotchanel", "how are you?")
    assert "I am good.Thankyou." in posted[1][1]

    posted.clear()
    blocked = client.post("/twilio", data={"From": "+1999", "Body": "how are you?"})
    assert blocked.status_code == 200
    assert posted == []


def test_twilio_reports_missing_slack_token():
    import os

    os.environ["user_number"] = "+1555"
    twilio_handle._slack = None
    client = twilio_handle.app.test_client()
    response = client.post("/twilio", data={"From": "+1555", "Body": "hi"})
    assert response.status_code == 503


def test_findbotid_needs_a_token():
    from findbotid import main

    assert main() == 1
