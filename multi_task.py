import json
import requests
import signal
import sys


def handle_sigint(sig, frame):
    print('\n\nThank you for using the application.\nClosing now...')
    sys.exit(0)


URL = 'http://localhost:7150/parse'

headers = {
    'Content-Type': 'application/json',
}

signal.signal(signal.SIGINT, handle_sigint)

payload = '{"text": "Hi"}'

response = requests.post(url=URL, headers=headers, data=payload)

data = response.json()
reply = data['directives'][0]['payload']['text']

print('App: ' + reply)

while True:
    inp = input('You: ')

    payload = '{"text":"%s", "frame":%s}' % (inp, json.dumps(data['frame']))

    response = requests.post(url=URL, headers=headers, data=payload)

    data = response.json()

    reply = data['directives'][0]['payload']['text']

    print('App: ' + reply)
