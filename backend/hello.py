
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
KPN_SMS_URL = "https://api-prd.kpn.com/messaging/sms-kpn/v1/send"


#MICROSOFT code
microsoft_cognitive_secret = get_environmental_variable('MICROSOFT_COGNITIVE_SECRET')
MICROSOFT_ENDPOINT_URL = "https://australiaeast.api.cognitive.microsoft.com/face/v1.0"

#Politie code
politie_api_key = get_environmental_variable("POLITIE_API_KEY")
POLITIE_MISSINGPERSON_ENDPOINT_URL = "https://api.acceptatie.politie.nl/v4/vermist?language=en&radius=5.0&maxnumberofitems=25&offset=0"
POLITIE_FUGITIVEPERSON_ENDPOINT_URL = "https://api.acceptatie.politie.nl/v4/gezocht?language=en&radius=5.0&maxnumberofitems=25&offset=0"


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
        'ocp-apim-subscription-key': microsoft_cognitive_secret,
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

@app.route("/create-collection/<collection_name>")
def create_image_collection(collection_name):
    suffix = 'persongroups/%s' %(get_collection_id(collection_name))
    payload = json.dumps({"name":collection_name})
    request_type = 'PUT'
    response = make_microsoft_face_api_request(suffix, request_type, get_collection_id(collection_name), payload)
    if response.status_code == 200:
        return jsonify({})
    else:
        raise

@app.route("/delete-collection/<collection_name>")
def delete_image_collection(collection_name):
    suffix = 'persongroups/%s' % (get_collection_id(collection_name))
    payload = ''
    request_type = 'DELETE'
    response = make_microsoft_face_api_request(suffix, request_type, get_collection_id(collection_name), payload)
    if response.status_code == 200:
        return jsonify({})
    else:
        raise

@app.route("/train-collection/<collection_name>")
def train_image_collection(collection_name):
    # get_collection_id(collection_name)
    suffix = 'persongroups/%s/train' % (get_collection_id(collection_name))
    request_type='POST'
    payload = ''
    make_microsoft_face_api_request(suffix, request_type, get_collection_id(collection_name), payload)
    return jsonify({})

@app.route("/training-status-collection/<collection_name>")
def training_status_collection(collection_name):
    # get_collection_id(collection_name)
    payload = ''
    suffix = 'persongroups/%s/training' % (get_collection_id(collection_name))
    request_type='GET'
    response = make_microsoft_face_api_request(suffix, request_type, get_collection_id(collection_name), payload)
    return jsonify(response.json())

def _add_image_to_collection(collection_name, name, userdata, url):
    collection_id = get_collection_id(collection_name)
    #1. add person : https://[location].api.cognitive.microsoft.com/face/v1.0/persongroups/{personGroupId}/persons
    suffix = "persongroups/%s/persons" %(collection_id)
    request_type='POST'
    payload = json.dumps({"name":name, "userData":userdata})
    response = make_microsoft_face_api_request(suffix, request_type, collection_id, payload)

    person_id = response.json()['personId']
    #2. add image to that person:
    suffix = "persongroups/%s/persons/%s/persistedFaces" %(collection_id, person_id)
    import urllib
    payload = urllib.urlopen(url)

    url = MICROSOFT_ENDPOINT_URL + '/' + suffix
    headers = {
        'ocp-apim-subscription-key': microsoft_cognitive_secret,
        'content-type': "application/octet-stream",
        'Content-Transfer-Encoding': 'base64'
    }

    response = requests.request(request_type, url, data=payload, headers=headers)
    return jsonify(response.json())

@app.route("/add-image-to-collection/<collection_name>", methods=['POST'])
def add_image_to_collection(collection_name):
    req_json = json.loads(request.data)
    import random, string
    name = req_json.get("name", ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))
    userdata = req_json.get("userData", '')
    url = req_json.get("url")
    return _add_image_to_collection(collection_name, name, userdata, url)


@app.route("/check-image-in-collections", methods=['POST'])
def check_face_in_collections():
    #1. detect face(you will get faceid)
    suffix = "detect?returnFaceId=true"
    request_type = 'POST'
    req_json = json.loads(request.data)
    url = req_json.get("url") #"https://i.dawn.com/large/2018/02/5a8bf2139739e.png"
    import urllib
    payload = urllib.urlopen(url)
    # payload = #json.dumps({"url": url})
    # response = make_microsoft_face_api_request(suffix, request_type, 0, payload)
    url = MICROSOFT_ENDPOINT_URL + '/' + suffix
    headers = {
        'ocp-apim-subscription-key': microsoft_cognitive_secret,
        'content-type': "application/octet-stream",
        'Content-Transfer-Encoding': 'base64'
    }

    response = requests.request(request_type, url, data=payload, headers=headers)
    face_id = response.json()[0].get('faceId')
    face_id_array = [face_id]

    #2. identify face
    suffix = "identify"
    request_type = 'POST'
    payload = json.dumps({
        "personGroupId": "0",
        "faceIds": face_id_array,
        "maxNumOfCandidatesReturned": 1,
    })
    response = make_microsoft_face_api_request(suffix, request_type, 0, payload)
    person_id = response.json()[0].get("candidates")[0].get('personId')

    #3. get person info
    suffix = "persongroups/%s/persons/%s" %("0", person_id)
    request_type = 'GET'
    payload = ''
    response = make_microsoft_face_api_request(suffix, request_type, 0, payload)
    return jsonify(response.json())

@app.route("/send-sms", methods=['POST'])
def send_sms():
    import pdb;
    pdb.set_trace()
    get_access_token_if_died()
    global access_token_kpn
    # use the token to classify
    # parse image and extensions
    req_json = json.loads(request.data)
    messages = req_json.get('messages', None)
    if not messages:
        raise
    sender = req_json.get('sender', 'Demo App')
    body = {
        "messages": messages,
        "sender": sender
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'BearerToken %s' %(access_token_kpn)
    }
    response = requests.post(KPN_SMS_URL, json=body, headers=headers)
    return jsonify(response.json())
    # requests.request('POST', , data=payload, headers=header)


@app.route("/load-missing-person-data/<collection_name>")
def load_missing_person_data(collection_name):
    headers = {
        'x-api-key': politie_api_key,
        'content-type': "application/json",
    }

    response = requests.request('GET', POLITIE_MISSINGPERSON_ENDPOINT_URL, data='', headers=headers)
    missing_persons = response.json().get("vermisten")
    for missing_person in missing_persons:
        name = missing_person.get('titel')
        url = missing_person.get('afbeeldingen')[0].get('url')
        _add_image_to_collection(collection_name, name, json.dumps(missing_person), url)
    return jsonify({})

@app.route("/load-fugitive-person-data/<collection_name>")
def load_fugitive_person_data(collection_name):
    headers = {
        'x-api-key': politie_api_key,
        'content-type': "application/json",
    }

    response = requests.request('GET', POLITIE_FUGITIVEPERSON_ENDPOINT_URL, data='', headers=headers)
    fugitive_persons = response.json().get("opsporingsberichten")
    for fugitive_person in fugitive_persons:
        name = fugitive_person.get('titel')
        url = fugitive_person.get('afbeeldingen')[0].get('url')
        response = _add_image_to_collection(collection_name, name, json.dumps(fugitive_person), url)
        print response
    return jsonify({})


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/bye")
def test_function():
    return "GO to "+get_environmental_variable("HOME")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12000, debug=True)

