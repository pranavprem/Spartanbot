"""Flask app: Twilio SMS into Slack, and the Alexa answer endpoint.

The 2017 SMS path posted ``<@bot> <message>`` as the bot user and relied on
the RTM worker hearing its own message. Socket Mode does not deliver a bot's
own messages back to it, so this process now posts the question and the
answer itself. ``user_number`` is still the allow-list; an unset allow-list
refuses the relay instead of accepting every sender.
"""

import os

from flask import Flask, request

from controller import controller
from settings import clip_slack_text, setting

app = Flask(__name__)
_control = None
_slack = None


def get_control():
    global _control
    if _control is None:
        _control = controller()
    return _control


def get_slack():
    global _slack
    if _slack is None:
        token = setting("SLACK_BOT_TOKEN", "slacktoken")
        if not token:
            return None
        from slack_sdk import WebClient

        _slack = WebClient(token=token)
    return _slack


@app.route("/")
def health():
    return "Spartanbot is running."


@app.route("/twilio", methods=["POST"])
def post_to_slack():
    body = request.form.get("Body", "")
    sender = request.form.get("From", "")
    print("hit flask " + body)
    accept_number = setting("user_number")
    if not accept_number:
        print("user_number is not set; refusing to relay SMS")
        return "", 403
    if sender not in accept_number:
        return "", 200
    slack_client = get_slack()
    if slack_client is None:
        print("SLACK_BOT_TOKEN is not set; SMS was not posted")
        return "", 503
    channel = setting("SLACK_CHANNEL", default="#testonebotchanel")
    answer = get_control().find_solution(body)
    slack_client.chat_postMessage(channel=channel, text=clip_slack_text(body))
    slack_client.chat_postMessage(channel=channel, text=clip_slack_text(answer))
    return "", 200


@app.route("/alexa_endpoint/<question>", methods=["GET"])
def return_to_alexa(question):
    spoken = question.replace("_", " ")
    print("hit flask " + spoken)
    return get_control().find_solution(spoken).replace("\n", ". ")


if __name__ == "__main__":
    heroku_port = int(os.environ.get("PORT", 6000))
    app.run(host="0.0.0.0", port=heroku_port)
