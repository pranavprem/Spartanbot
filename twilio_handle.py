import os
from flask import Flask, request, Response
from twilio import twiml
from twilio.rest import TwilioRestClient
from slackclient import SlackClient


twilio_number = os.environ.get("twilio_number")
accept_number = os.environ.get("accepted_numbers")
app = Flask(__name__)
twilio_client = TwilioRestClient()
slack_client = SlackClient(os.environ.get("twilio_slack_token", None))
 
@app.route("/", methods=['POST'])
def post_to_slack():
    # response = twiml.Response()
    if request.form['From'] in accept_number:
        message = request.form['Body']
        slack_client.api_call("chat.postMessage",
                              channel="#testonebotchanel",
                              text=message, as_user=True)
    # return Response(response.toxml(), mimetype="text/xml"), 200


if __name__ == "__main__":
    heroku_port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=heroku_port)
