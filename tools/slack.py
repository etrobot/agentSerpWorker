import requests,json,os
def send_slack_message(message, webhook_url):
    headers = {
        'Content-type': 'application/json',
    }
    data = {
        'text': message
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    return response