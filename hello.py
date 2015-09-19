
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
INTRO_TEXT = ("Welcome to Walmart. Please text the name of the product you are looking for and we will tell you where to "
              "find it in this store. Please text 'help' to be connected to a walmart associate who can assist you.")

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

    if phone_number == "+14157066803":
        client.sms.messages.create(to="+19253896343", from_=TWILIO_NUMBER, body=body)
        return

    if body == "Hi" or body == "hi":
        client.sms.messages.create(to=phone_number, from_=TWILIO_NUMBER, body=INTRO_TEXT)
        return

    if body == "help":
        return

    return_message = find_location_in_store(5457, body)
    client.sms.messages.create(to=phone_number, from_=TWILIO_NUMBER, body=return_message)

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
    in_stock = result.get('inventory').get('status') == "In Stock"

    aisles_string = ", ".join(map(lambda x: "Aisle %s" % x, aisles))
    str = ("%s can be found in %s" % (query, aisles_string)).capitalize()
    if in_stock:
        str += ". It's in stock."
    else:
        str += ", but it's not in stock."
    return str

def make_request(base_url, payload):
    url = "%s?%s" % (base_url, urllib.urlencode(payload))
    resp = requests.get(url)
    json = resp.json()
    print json
    if 'results' in json:
        return json['results']

if __name__ == '__main__':
    app.run(debug=True)