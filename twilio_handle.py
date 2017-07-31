import os
from flask import Flask, request
# from twilio import twiml
#from twilio.rest import TwilioRestClient
from slackclient import SlackClient

control = controller()

AT_BOT = "<@" + os.environ["bot_id"] + ">"
twilio_number = os.environ.get("twilio_number")
accept_number = os.environ.get("user_number")
app = Flask(__name__)
#twilio_client = TwilioRestClient()
slack_client = SlackClient(os.environ.get("slacktoken", None))
 
@app.route("/twilio", methods=['POST'])
def post_to_slack():
    print "hit flask" + request.form['Body']
    # response = twiml.Response()
    if request.form['From'] in accept_number:
        message = request.form['Body']
        slack_client.api_call("chat.postMessage",
                              channel="#testonebotchanel",
                              text=AT_BOT +" "+ message, as_user=True)
        #twilio_client.messages.create(to=accept_number, from_=twilio_number,body="response")
    # return Response(response.toxml(), mimetype="text/xml"), 200
    return '', 200



@app.route("/alexa_endpoint/<question>", methods=['POST'])
def return_to_alexa(question):
    print "hit flask" + request.form['Body']
    # response = twiml.Response()
    
        #twilio_client.messages.create(to=accept_number, from_=twilio_number,body="response")
    # return Response(response.toxml(), mimetype="text/xml"), 200
    return control.find_solution(question)


if __name__ == "__main__":
    heroku_port = int(os.environ.get("PORT", 6000))
    app.run(host='0.0.0.0', port=heroku_port)
