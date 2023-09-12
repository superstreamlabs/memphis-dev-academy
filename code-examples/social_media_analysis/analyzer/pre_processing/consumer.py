from __future__ import annotations
import asyncio
from memphis import Memphis, MemphisError, MemphisConnectError, MemphisHeaderError
import pandas as pd
 
async def consume(period_days):
    tweets = []
    try:
        memphis = Memphis()
        await memphis.connect(host="<memphis-host>", username="<application-type username>", password="<string>", account_id="<account_id>")
        if period_days == 1:
            consumer = await memphis.consumer(station_name="public_data_1_day", consumer_name="cons_1", consumer_group="", generate_random_suffix=True)
        elif period_days == 3:
            consumer = await memphis.consumer(station_name="public_data_3_days", consumer_name="cons_3", consumer_group="", generate_random_suffix=True)
        else:
            consumer = await memphis.consumer(station_name="public_data_week", consumer_name="cons_7", consumer_group="", generate_random_suffix=True)
        while True:
            msgs = await consumer.fetch(batch_size=100)
            if len(msgs) == 0:
                print("no messages")
                break 
            else:
                print("messages: ", len(msgs))
                for msg in msgs:
                    tweets.append({"text": msg.get_data().decode('utf-8')})
                    await msg.ack()
        
        print("done")
        tweets_df = pd.DataFrame(tweets)
        return tweets_df
        
    except (MemphisError, MemphisConnectError) as e:
        print(e)
        return None
        
    finally:
        await memphis.close()
