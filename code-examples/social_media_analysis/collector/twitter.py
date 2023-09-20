import requests

bearer_token = "<bearer_token>"
search_users_tweets_url = "https://api.twitter.com/2/users/{}/tweets"
    
def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

        
def connect_to_endpoint(url=None, params=None):
    try:
        response = requests.get(url=url, params=params, auth=bearer_oauth)
        if response.status_code != 200:
            if response.status_code != 429: #Too Many Requests
                print(response.status_code, response.text)
                return []
            else:
                return []
        else:
            return response.json()['data']
    except Exception as e:
        print(e)
        return []

def get_tweets(account_id):
    try:
        # Modify connect_to_endpoint implemntation to fit deifferent API calls for different data sources
        # You can use different frameworks to connect to the API, like tweepy and praw for Twitter and Reddit respectively
        return connect_to_endpoint(search_users_tweets_url.format(account_id),{})
    except:
        return []
    
    