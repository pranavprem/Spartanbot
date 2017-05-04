import os
import time
from slackclient import SlackClient
from controller import controller


AT_BOT = "<@" + os.environ["bot_id"] + ">"
slack_client = SlackClient(os.environ["slacktoken"])

control=controller()

def handle_command(command, channel):
    slack_client.api_call("chat.postMessage", channel=channel, text=control.find_solution(command), as_user=True)



def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print "SpartanBot connected and running!"
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
	    print "Connection failed. Invalid Slack token or bot ID?"
