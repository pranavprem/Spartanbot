import os

from settings import load_dotenv, setting


def test_dotenv_does_not_override_existing_variables(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        'SLACK_BOT_TOKEN=from-file\nuser_number="+1555"\n# comment\n\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("SLACK_BOT_TOKEN", "from-env")
    monkeypatch.delenv("user_number", raising=False)
    load_dotenv(str(env_file))
    assert os.environ["SLACK_BOT_TOKEN"] == "from-env"
    assert setting("user_number") == "+1555"
