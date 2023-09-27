import requests
    
def post_to_slack_support(message):
    try:
        headers = {
            'Content-type': 'application/json',
        }
        json_data = {
             'text': str(message), #Modify this to your message
        }
        response = requests.post(
            'https://hooks.slack.com/services/.../.../...',   
            headers=headers,
            json=json_data,
        )
        print(response)
    except Exception as e:
        print(e)
        return 
    