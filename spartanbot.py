import os
import time
from slackclient import SlackClient
import botdata



BOT_ID = "U4NE6GQE7"

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ["slacktoken"])




def operate(thing):
	if thing[1] == "+":
		return "result is %d"%(int(thing[0])+int(thing[2]))
	elif thing[1] == "-":
		return "result is %d"%(int(thing[0])-int(thing[2]))
	elif thing[1] == "*":
		return "result is %d"%(int(thing[0])*int(thing[2]))
	elif thing[1] == "/":
		return "result is %d"%int(int(thing[0])/int(thing[2]))


def dowhat(thing):
    thing = thing.split(" ")
    for word in thing:
        print "word is:" + word
        if "you" in word:
            print "it got zebot"
            subject = botdata.zebot()
        elif "tushar" in word:
            print "it got tushar"
            subject = botdata.zeTushar()
    
    print subject

    for word in thing:
        print "word is:" + word
        if "name" in word:
            print "it got name"
            return subject.name
        elif "age" in word or "old" in word or "years" in word:
            print "it got age"
            return subject.age
        elif "gender" in word or "sex" in word:
            print "it got gender"
            return subject.gender
        elif "maker" in word or "creator" in word or "made" in word:
            print "it got maker"
            return subject.creator


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """    
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        print command.split(" ")
        response = operate(command.split(" ")[1:])
    elif "what" in command:
        response = dowhat(command)
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("SpartanBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
	print("Connection failed. Invalid Slack token or bot ID?")
