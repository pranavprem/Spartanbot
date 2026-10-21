"""Print the Slack user id for the configured bot name.

The 2017 script had a bot token in source. Pass the token with
``SLACK_BOT_TOKEN`` (or the old ``slacktoken`` name) instead.
"""

import sys

from settings import setting


def main():
    bot_name = setting("SLACK_BOT_NAME", default="testonebot")
    token = setting("SLACK_BOT_TOKEN", "slacktoken")
    if not token:
        print("Set SLACK_BOT_TOKEN (or slacktoken) to look up the bot user id.")
        return 1
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError

    client = WebClient(token=token)
    try:
        auth = client.auth_test()
        print("This token belongs to user id %s (%s)." % (auth.get("user_id"), auth.get("user")))
        api_call = client.users_list()
    except SlackApiError as exc:
        print("could not list users: %s" % exc)
        return 1
    members = api_call.get("members", []) if api_call.get("ok") else []
    for user in members:
        if user.get("name") == bot_name:
            print("Bot ID for '" + user["name"] + "' is " + user.get("id"))
            return 0
    print("could not find bot user with the name " + bot_name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
