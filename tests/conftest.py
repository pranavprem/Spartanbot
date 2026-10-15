import os

# Do this before any project import so a developer .env cannot leak into tests.
os.environ["SPARTANBOT_DISABLE_DOTENV"] = "1"

import pytest

import twilio_handle


@pytest.fixture(autouse=True)
def isolated_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("SPARTANBOT_LOCAL_DB", str(tmp_path / "knowledge.json"))
    monkeypatch.setenv("SPARTANBOT_DISABLE_DOTENV", "1")
    for name in (
        "MONGODB_URI",
        "MONGODB_DB",
        "my_api_key",
        "GOOGLE_API_KEY",
        "my_cse_id",
        "GOOGLE_CSE_ID",
        "bluemix_username",
        "bluemix_password",
        "WATSON_USERNAME",
        "WATSON_PASSWORD",
        "WATSON_CLASSIFIER_ID",
        "SLACK_BOT_TOKEN",
        "slacktoken",
        "SLACK_APP_TOKEN",
        "SLACK_BOT_ID",
        "bot_id",
        "user_number",
        "ALEXA_BACKEND_URL",
    ):
        monkeypatch.delenv(name, raising=False)
    twilio_handle._control = None
    twilio_handle._slack = None
    return tmp_path
