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

    asr_output = open('asr_output.txt', 'r')
    nbest_list = [line for line in asr_output]
    asr_output.close()

    payload = '{"text":"%s", "frame":%s, "nbest_transcripts_text":%s}' % (
        inp, json.dumps(data['frame']), json.dumps(nbest_list))

    response = requests.post(url=URL, headers=headers, data=payload)

    data = response.json()

    reply = data['directives'][0]['payload']['text']

    print('App: ' + reply)
