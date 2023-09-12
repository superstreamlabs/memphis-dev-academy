from google.cloud import bigquery
import pandas as pd
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "<path-to-google-application-credentials>"
job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_APPEND",
)
client = bigquery.Client()
table_id = "<table-id>"


def upload_to_bigquery(client, dataframe, table_id):
    try:
        print("Uploading to BigQuery")
        job = client.load_table_from_dataframe(
            dataframe, table_id, job_config=job_config)
        job.result()
        print("Upload Completed")
    except Exception as e:
        print("Error in upload_to_bigquery: ")
        print(e)

def upload(topics, period_days, timestamp):
    data_to_upload = []
    for _, topic_content in topics:
        data_to_upload.append({"topics": topic_content,"period_days": period_days,"timestamp": timestamp})
     
    dataframe = pd.DataFrame(data_to_upload,
            columns=[
                "topics",
                "period_days",
                "timestamp",
                ])
    upload_to_bigquery(client, dataframe, table_id)
        