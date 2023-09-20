from __future__ import annotations
import asyncio
import consumer
import lda
import big_query
import datetime

async def main():
    time_period = [1, 3, 7]
    timestamp = datetime.datetime.now()
    for period in time_period:
        try:
            print("Consuming...")
            data = await consumer.consume(period)
            print("Run LDA...")
            topics = lda.run_model(data)
            print("Uploading to BigQuery...")
            await big_query.upload(topics, period, timestamp)
        except Exception as e:
            print(e)
       
if __name__ == "__main__":
    asyncio.run(main())