import asyncio
from slack import post_to_slack_support
from memphis import Memphis, MemphisError, MemphisConnectError, MemphisHeaderError
import json
from google.cloud import bigquery
import pandas as pd
import os
from datetime import datetime
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./path to your service account key.json"
job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_APPEND",
)
client = bigquery.Client()
table_id = 'bigquery table id'


def get_geo_location(ip_address):
    print("Getting geo location")
    # Create your own function if needed...
    return


def upload_to_bigquery(client, dataframe, table_id):
    try:
        print("Uploading to BigQuery")
        job = client.load_table_from_dataframe(
            dataframe, table_id, job_config=job_config)
        job.result()
        print("Upload Completed")
        return True
    except Exception as e:
        print("Error in upload_to_bigquery: ")
        print(dataframe)
        print(e)
        return False


async def main():
    try:
        memphis = Memphis()
        await memphis.connect(host="<host>", username="<client-type-user>", password="<client-type-password>", account_id="<account-id>", max_reconnect=20 ,reconnect_interval_ms=60000, timeout_ms=6000)
        print("Connected to Memphis")
        consumer = await memphis.consumer(station_name="traces", consumer_name="traces_consumer", consumer_group="", max_ack_time_ms=60000, max_msg_deliveries=3)
        
        print("Connected to Consumer")
        while True:
            try:
                print("Fetching messages")
                msgs = await consumer.fetch(batch_size=500) 
                print("Fetched")
                is_succeeded = True
                records = []
                for msg in msgs:
                    trace = json.loads(msg.get_data().decode("utf-8"))
                    if trace['event'] == 'error':
                        post_to_slack_support("Generate some support message")
                    if trace['event'] == 'installation':
                        get_geo_location(trace['ip']) # Modify this to your function
                    trace['enriched'] = "Some enriched data here..."
                    trace['timestamp'] = trace['timestamp']
                    trace['bq_ingested_timestamp'] = datetime.utcnow()
                    records.append(trace)
                    await msg.ack()
                if len(records) > 0:
                    dataframe = pd.DataFrame(
                        records,
                        columns=[
                            "event",
                            "enriched",
                            "ip",
                            "site_url",
                            "timestamp",
                            "bq_ingested_timestamp"
                        ]
                    )
                    is_succeeded = upload_to_bigquery(client, dataframe, table_id)
                if is_succeeded:
                    time.sleep(1)
                else:
                    print("Sleeping for 11 minutes")
                    time.sleep(660)
            except Exception as e:
                print("Error in main loop: ")
                print(e)
                time.sleep(1)
                continue
      
    except (MemphisError, MemphisConnectError) as e:
        print(e)

    finally:
        await consumer.destroy()
        await memphis.close()

if __name__ == "__main__":
    asyncio.run(main())
