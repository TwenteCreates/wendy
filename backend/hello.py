
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


#MICROSOFT code
microsoft_cognitive_secret = get_environmental_variable('MICROSOFT_COGNITIVE_SECRET')
MICROSOFT_ENDPOINT_URL = "https://australiaeast.api.cognitive.microsoft.com/face/v1.0"



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

def _classify_images(urls):
    global access_token_kpn
    # use the token to classify
    # parse image and extensions
    body = {
        "data": urls
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'BearerToken %s' %(access_token_kpn)
    }
    response = requests.post(KPN_CLASSIFY_URL, json=body, headers=headers)
    return jsonify(response.json())


@app.route("/image-classify", methods=['POST'])
def image_classifier():
    image_urls = json.loads(request.data).get('urls', None)
    if not image_urls:
        raise
    get_access_token_if_died()
    return _classify_images(image_urls)

def make_microsoft_face_api_request(suffix, request_type, collection_id, payload):
    url = MICROSOFT_ENDPOINT_URL + '/' + suffix
    headers = {
        'ocp-apim-subscription-key': "c9f4b9a5d14a4083af48fe563521edc4",
        'content-type': "application/json",
    }

    response = requests.request(request_type, url, data=payload, headers=headers)
    print(response.status_code)
    print(response.text)
    return response

def get_collection_id(collection_name):
    collection_id = 1
    if collection_name == 'final':
        collection_id = 0
    return collection_id

@app.route("/create-image-collection/<collection_name>")
def create_image_collection(collection_name):
    suffix = 'largepersongroups/%s' %(get_collection_id(collection_name))
    payload = json.dumps({"name":collection_name})
    request_type = 'PUT'
    response = make_microsoft_face_api_request(suffix, request_type, get_collection_id(collection_name), payload)
    if response.status_code == 200:
        return jsonify({})
    else:
        raise

@app.route("/delete-image-collection/<collection_name>")
def delete_image_collection(collection_name):
    suffix = 'largepersongroups/%s' % (get_collection_id(collection_name))
    payload = ''
    request_type = 'DELETE'
    response = make_microsoft_face_api_request(suffix, request_type, get_collection_id(collection_name), payload)
    if response.status_code == 200:
        return jsonify({})
    else:
        raise

@app.route("/train-image-to-collection/<collection_name>")
def train_image_collection(collection_name):
    get_collection_id(collection_name)
    return jsonify({})


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/bye")
def test_function():
    return "GO to "+get_environmental_variable("HOME")




if __name__ == "__main__":
    # list_all_images_in_collection()
    # add_images_to_collection()
    # list_all_images_in_collection()
    # test_images()
    # upload_all_images_to_collection()
    app.run(host='0.0.0.0', port=12000, debug=True)
