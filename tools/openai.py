import requests
import json

api_key = ""

def create (model="gpt-3.5-turbo",messages=[]):
    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    json_response = response.json()

    return json_response