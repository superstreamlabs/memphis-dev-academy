
from __future__ import annotations
import asyncio
from memphis import Memphis, Headers, MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError
import twitter

def get_accouns_list():
    with open('./accounts.txt') as f:
        return [{line.rstrip('\n').split()[0]: line.rstrip('\n').split()[1]} for line in f]
 
async def main():
    try:
        # Create a list of accounts to follow on Twitter. 
        # The file accounts.txt contains a list of accounts to follow, one per line, in the format: account_name account_id
        # The function get_accouns_list() reads the file and returns a list of dictionaries with the account name and id
        accounts = get_accouns_list()
        # Connect to Memphis
        memphis = Memphis()
        await memphis.connect(host="<memphis-host>", username="<application-type username>", password="<string>", account_id="<account_id>")
        # For each account, get the tweets and produce them to the different stations
        # Each tweet is produced with the account name as header
        # Each station has a different retention period: 1 day, 3 days and 1 week
        # For deduplication, the tweet id is used as message id - this way, the same tweet will not be produced twice
        for account in accounts:
            for key, value in account.items():
                print("Account: ", key, " - ", value)
                tweets = twitter.get_tweets(value)
                print("Tweets: ", len(tweets))
                print("Producing...")
                for tweet in tweets:
                    headers= Headers()
                    headers.add("account", key)
                    await memphis.produce(station_name="public_data_week", producer_name='prod7',
                        headers=headers,
                        message=tweet['text'],
                        msg_id=tweet['id'])
                    await memphis.produce(station_name="public_data_3_days", producer_name='prod3',
                        headers=headers,
                        message=tweet['text'],
                        msg_id=tweet['id'])
                    await memphis.produce(station_name="public_data_1_day", producer_name='prod1',
                        headers=headers,
                        message=tweet['text'],
                        msg_id=tweet['id'])
    except (MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError) as e:
        print(e)
        await memphis.close()
        
if __name__ == "__main__":
    asyncio.run(main())