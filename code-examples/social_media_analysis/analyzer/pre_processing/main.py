from __future__ import annotations
import asyncio
import consumer
import producer
import pre_processing

async def main():
    
    time_period = [1, 3, 7]
    for period in time_period:
        try:
            print("Consuming...")
            data = await consumer.consume(period)
            print("Preprocessing...")
            data = pre_processing.preprocess_data(data, "twitter")
            print("Producing...")
            await producer.produce(data, period)
        except Exception as e:
            print(e)
       
if __name__ == "__main__":
    asyncio.run(main())