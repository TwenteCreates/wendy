from flask import Flask, jsonify, request
from flask_cors import CORS

import json
import os
import requests

app = Flask(__name__)
cors = CORS(app)

def get_environmental_variable(key=None):
    if not key:
        raise
    return os.getenv(key, default=None)

#KPN ode
kpn_key = get_environmental_variable("KPN_KEY")
kpn_secret = get_environmental_variable("KPN_SECRET")
access_token_kpn = ""
active_till_kpn = 0
KPN_BASE_URL = "https://api-prd.kpn.com/oauth/client_credential/accesstoken?grant_type=client_credentials"
KPN_CLASSIFY_URL = "https://api-prd.kpn.com/ai/image-classifier/v1/classify"


def get_access_token_if_died():
    global access_token_kpn
    #request to get kpn token if its dead or needs renewal
    querystring = {"grant_type": "client_credentials"}

    payload = "client_id=%s&client_secret=%s" %(kpn_key, kpn_secret)
    headers = {
        'content-type': "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", KPN_BASE_URL, data=payload, headers=headers, params=querystring)
    json_resp = json.loads(response.text)
    access_token_kpn = json_resp.get('access_token', "")

def _classify_image():
    global access_token_kpn
    # use the token to classify
    # parse image and extensions
    body = {
        "data":[ #list of images with ext
            {
                "ext": "jpg",
                "path": "http://www.babushahi.com/upload/image/Train-Engine_HKM.jpg"
            },
            {
                "ext" : "jpg",
                "path" : "https://upload.wikimedia.org/wikipedia/commons/0/0e/Atlanta_Zoo_Panda.jpg"
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'BearerToken %s' %(access_token_kpn)
    }
    response = requests.post(KPN_CLASSIFY_URL, json=body, headers=headers)
    return jsonify(response.json())


@app.route("/image-classify", methods=['POST'])
def image_classifier():
    image_url = request.values.get('url', None)
    if not image_url:
        raise
    get_access_token_if_died()
    return _classify_image()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/bye")
def test_function():
    return "GO to "+get_environmental_variable("HOME")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12000, debug=True)
