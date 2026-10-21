"""Slack listener, with a local REPL when Slack is not configured.

The 2017 worker used Slack's RTM API through the ``slackclient`` package.
New Slack apps cannot use RTM. Socket Mode is the supported replacement and
is used when ``SLACK_APP_TOKEN`` is set. A leftover classic bot token still
tries RTM. With neither token, ``python spartanbot.py`` answers in the terminal.
"""

import sys
from threading import Event

from controller import controller
from settings import clip_slack_text, setting


def parse_slack_output(slack_rtm_output, at_bot):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and "text" in output and at_bot and at_bot in output["text"]:
                return output["text"].split(at_bot)[1].strip().lower(), output["channel"]
    return None, None


def handle_command(web_client, command, channel, control):
    text = clip_slack_text(control.find_solution(command))
    web_client.chat_postMessage(channel=channel, text=text)


def dispatch_event(web_client, event, at_bot, control):
    if not isinstance(event, dict):
        return
    if event.get("type") == "message" and event.get("subtype"):
        return
    command, channel = parse_slack_output(
        [{"text": event.get("text", ""), "channel": event.get("channel")}],
        at_bot,
    )
    if command and channel:
        handle_command(web_client, command, channel, control)


def resolve_bot_id(web_client):
    configured = setting("SLACK_BOT_ID", "bot_id")
    if configured:
        return configured
    auth = web_client.auth_test()
    return auth["user_id"]


def run_repl(control):
    print("SpartanBot local mode. No Slack token configured.")
    print("Ask a CMPE 273 question. Type quit to exit.")
    while True:
        try:
            command = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        command = command.strip().lower()
        if command in ("quit", "exit"):
            break
        if not command:
            continue
        print(control.find_solution(command))
    return 0


def run_rtm(token, control):
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    from slack_sdk.rtm_v2 import RTMClient

    web = WebClient(token=token)
    try:
        bot_id = resolve_bot_id(web)
    except SlackApiError as exc:
        print("Connection failed. Invalid Slack token or bot ID?")
        print(exc)
        return 1
    at_bot = "<@" + bot_id + ">"
    rtm = RTMClient(token=token, web_client=web)

    @rtm.on("message")
    def handle(client, event):
        try:
            dispatch_event(client.web_client, event, at_bot, control)
        except Exception as exc:
            print("Failed to handle Slack message: %s" % exc)

    print("SpartanBot connected and running!")
    try:
        rtm.start()
    except SlackApiError as exc:
        print("RTM connection failed. New Slack apps cannot use the legacy RTM API.")
        print("Create a Socket Mode app and set SLACK_APP_TOKEN plus SLACK_BOT_TOKEN.")
        print(exc)
        return 1
    return 0


def handle_socket_request(client, req, at_bot, control):
    from slack_sdk.socket_mode.response import SocketModeResponse

    if req.type != "events_api":
        return
    client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))
    try:
        dispatch_event(client.web_client, req.payload.get("event", {}), at_bot, control)
    except Exception as exc:
        print("Failed to handle Slack event: %s" % exc)


def run_socket_mode(token, app_token, control):
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    from slack_sdk.socket_mode import SocketModeClient

    web = WebClient(token=token)
    try:
        bot_id = resolve_bot_id(web)
    except SlackApiError as exc:
        print("Connection failed. Invalid Slack token or bot ID?")
        print(exc)
        return 1
    at_bot = "<@" + bot_id + ">"
    socket_client = SocketModeClient(app_token=app_token, web_client=web)

    def process(client, req):
        handle_socket_request(client, req, at_bot, control)

    socket_client.socket_mode_request_listeners.append(process)
    try:
        socket_client.connect()
    except SlackApiError as exc:
        print("Socket Mode connection failed.")
        print(exc)
        return 1
    print("SpartanBot connected and running!")
    Event().wait()
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    control = controller()
    if "--local" in argv:
        return run_repl(control)
    token = setting("SLACK_BOT_TOKEN", "slacktoken")
    app_token = setting("SLACK_APP_TOKEN")
    if app_token and token:
        return run_socket_mode(token, app_token, control)
    if token:
        return run_rtm(token, control)
    if sys.stdin is None or not sys.stdin.isatty():
        print("No Slack token configured and stdin is not a terminal.")
        print("Set SLACK_APP_TOKEN and SLACK_BOT_TOKEN, or run in a terminal for local mode.")
        return 1
    return run_repl(control)


if __name__ == "__main__":
    sys.exit(main())
