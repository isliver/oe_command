import requests
import json
from tools import gpt_cost

api_key = ""

def create (model="gpt-3.5-turbo",messages=[]):
    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    payload = {
        "model": model,
        "messages": messages
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    json_response = response.json()

    gpt_cost.addResponse(json_response, model)

    return json_response