from flask import Flask, request
import json
import requests
import modules.gen_response as gen_res

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAABZB3OScsuIBAFIN9SjJ2ZAqwvcAMMZCi4uDw62iZBgtLile75GND8sO8aUgv2TKlZAopbULPEwk3KvN7NanlTpU1H6HAukv8Fm6t6v8htSpWbJA2uWt3ZATzODuv55HTu7OzW0icmp5luudUFR6sCwbjB7C6qyE5VgwZA0s6xbQZDZD'


#Set up the greeting page for the bot
def set_homepage():
    url = "https://graph.facebook.com/v2.6/me/messenger_profile"
    data = {
        "get_started":{
            "payload":"get_started_payload"
        }
    }
    r = requests.post(url=url,
                  data=json.dumps(data),
                  params = {"access_token":PAT},
                  headers={'Content-type': 'application/json'})
    print "\n\n\n home page setup \n\n\n"
    print r.status_code
#set_homepage()

@app.route('/', methods=['GET'])
def handle_verification():
    """
    function to handle validation with the facebook server
    """

    print "Handling Verification."
    if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
      print "Verification successful!"
      return request.args.get('hub.challenge', '')
    else:
      print "Verification failed!"
      return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
    print "Handling Messages"
    payload = request.get_data()
    print "\n\n payload is \n\n"
    print payload
    print "\n\n json is \n\n"
    print request.get_json()
    for sender, message in messaging_events(payload):
      print "Incoming from %s: %s" % (sender, message)
      send_message(PAT, sender, message, json.loads(payload))
    return "ok"


def messaging_events(payload):
    """
    Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    print data
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
      if "message" in event and "text" in event["message"]:
        yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
      else:
        yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text, payload):
    """
    Send the message text to recipient with id recipient.
    """

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                        "recipient": {"id": recipient},
                        "message": gen_res.gen_data_dict(text=text.decode('unicode_escape'), payload=payload, psid=recipient)
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
      print r.text


if __name__ == '__main__':
    app.run()
