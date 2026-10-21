"""Environment helpers.

Historical Heroku config used names such as ``slacktoken`` and ``my_api_key``.
Newer aliases are accepted too. A local ``.env`` file is loaded with
``setdefault``, so a real environment variable always wins.
"""

import os

SLACK_TEXT_LIMIT = 3900

_DOTENV_LOADED = False


def load_dotenv(path=None):
    """Load KEY=VALUE lines from ``.env`` next to this file, if it exists."""
    global _DOTENV_LOADED
    explicit = path is not None
    if not explicit:
        if _DOTENV_LOADED:
            return
        _DOTENV_LOADED = True
        if os.environ.get("SPARTANBOT_DISABLE_DOTENV"):
            return
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                os.environ.setdefault(key, value)


def setting(*names, default=None):
    """Return the first non-empty environment variable among ``names``."""
    load_dotenv()
    for name in names:
        value = os.environ.get(name)
        if value not in (None, ""):
            return value
    return default


def clip_slack_text(text):
    """Keep a Slack message inside the typical chat.postMessage size."""
    text = "" if text is None else str(text)
    if len(text) <= SLACK_TEXT_LIMIT:
        return text
    return text[:SLACK_TEXT_LIMIT] + "\n..."
