
from flask import Flask
from flask import render_template, request

from twilio.rest import TwilioRestClient

import requests
import urllib

# Twilio configuration.
TWILIO_ACCOUNT_SID = "ACbd6fbaccd6b0b257cbfabff29300c9be"
TWILIO_AUTH_TOKEN = "7ae2c137c0a76bb8846c801b793ec5aa"
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
    return find_location_in_store(5457, 'candy')

@app.route("/receive_message", methods=['POST'])
def receive_message():
    phone_number = request.values.get("From")
    body = request.values.get("Body").strip()
    return_message = find_location_in_store(5457, body)
    client.sms.messages.create(to="9253896343", from_=TWILIO_NUMBER, body=return_message)

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
    results = make_request(base_url, payload)
    result = results[0]
    location = result['location']
    aisles = location['aisle']

    aisles_string = ", ".join(map(lambda x: "Aisle %s" % x, aisles))
    return ("%s can be found in %s" % (query, aisles_string)).capitalize()


def make_request(base_url, payload):
    url = "%s?%s" % (base_url, urllib.urlencode(payload))
    resp = requests.get(url)
    json = resp.json()
    print json
    if 'results' in json:
        return json['results']

if __name__ == '__main__':
    app.run(debug=True)