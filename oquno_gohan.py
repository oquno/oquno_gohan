from dotenv import load_dotenv
import requests, os
from requests_oauthlib import OAuth1
import tweepy
from datetime import datetime

load_dotenv()

hass_token = os.environ.get("HA_TOKEN")
hass_host = os.environ.get("HA_HOST")
device_id = os.environ.get("HA_DEVICE_ID")
endpoint_path = f'/api/states/{device_id}'
last_state_path = "./last_state.txt"

consumer_key = os.environ.get("X_CONSUMER_KEY")
consumer_secret = os.environ.get("X_CONSUMER_SECRET")
access_token = os.environ.get("X_ACCESS_TOKEN")
access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

running_message = os.environ.get("RUNNING_MESSAGE")
ready_message = os.environ.get("READY_MESSAGE")
complete_message = os.environ.get("COMPLETE_MESSAGE")
keepwarm_message = os.environ.get("KEEPWARM_MESSAGE")
keepwarm_end_message = os.environ.get("KEEPWARM_END_MESSAGE")
cancel_message = os.environ.get("CANCEL_MESSAGE")

def connect_to_oauth(consumer_key, consumer_secret, acccess_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(consumer_key, consumer_secret, acccess_token, access_token_secret)
    return url, auth

def post(text):
    print(f"post {text}")
    payload = { 'text': text }
    url, auth = connect_to_oauth(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    request = requests.post(
        auth=auth, url=url, json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(request)

def tweep(text):
    print(f"post {text}")
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    ret = client.create_tweet(text=text)
    print(ret)

def fetch_gohan_state():
    url = f"{hass_host}{endpoint_path}"
    headers = {
        "Authorization": f"Bearer {hass_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    return response.json()["state"]

def get_last_state():
    if not os.path.isfile(last_state_path):
        return None
    with open(last_state_path, encoding='UTF-8') as f:
        return f.read().strip()

def write_last_state(state):
    with open(last_state_path, mode='w', encoding='UTF-8') as f:
        return f.write(state)

last_state = get_last_state()
curr_state = fetch_gohan_state()
if last_state != curr_state:
    text = None
    if curr_state == 'running':
        text = running_message
    if curr_state == 'idle':
        if last_state == 'keep warm':
            text = keepwarm_end_message
        if last_state == 'running':
            text = complete_message 
        if last_state == 'delay':
            text = cancel_message
    if curr_state == 'delay':
        text = ready_message
    if curr_state == 'keep warm':
        text = keepwarm_message
        if last_state == 'runnig':
            text = complete_message
    if text != None:
        post(text)
    write_last_state(curr_state)
