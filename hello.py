
from flask import Flask
from flask import render_template, request

from twilio.rest import TwilioRestClient

import requests
import urllib

# Twilio configuration.
TWILIO_ACCOUNT_SID = "AC52a3d465bd5577c994ebad881c1ac48a"
TWILIO_AUTH_TOKEN = "5fdc4c5e212bd4e3301211631ad5e729"
TWILIO_NUMBER = "+14152148445"
WALMART_KEY = "zyaws883qm53fwt9ty36f8u6"

client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message')
def send_message():
    #client.sms.messages.create(to=toNumber, from_=twilioNumber["number"], body=body)
    #find_store()
    find_location_in_store(5457, 'candy')

    return "yo"

@app.route("/receive_message", methods=['POST'])
def receive_message():
    phone_number = request.values.get("From")
    body = request.values.get("Body").strip()
    client.sms.messages.create(to="9253896343",from_=TWILIO_NUMBER, body=body)

def find_store():
    base_url = "http://api.walmartlabs.com/v1/stores"
    payload = {
        'apiKey': WALMART_KEY,
        'city': "San Francisco"
    }
    return make_request(base_url, payload)

def find_location_in_store(store_id, query):
    base_url = "http://search.mobile.walmart.com/search"
    payload = {
        'store': store_id,
        'query': query,
        'offset': 0,
        'size': 20
    }
    return make_request(base_url, payload)

def make_request(base_url, payload):
    url = "%s?%s" % (base_url, urllib.urlencode(payload))
    resp = requests.get(url)
    json = resp.json()
    if 'results' in json:
        return json['results']

if __name__ == '__main__':
    app.run(debug=True)