
from __future__ import annotations
import asyncio
from memphis import Memphis, Headers, MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError

 
async def produce(data, period_days):
    try:
        memphis = Memphis()
        await memphis.connect(host="<memphis-host>", username="<application-type username>", password="<string>", account_id="<account_id>")
        for index, row in data.iterrows():
            if period_days == 1:
                await memphis.produce(station_name="preprocess_1_day", producer_name="preprocess_1_day", message=row['preprocess_text'])
            elif period_days == 3:
                await memphis.produce(station_name="preprocess_3_days", producer_name="preprocess_3_days", message=row['preprocess_text'])
            else:
                await memphis.produce(station_name="preprocess_week", producer_name="preprocess_week", message=row['preprocess_text'])   
    except (MemphisError, MemphisConnectError, MemphisHeaderError, MemphisSchemaError) as e:
        print(e)
        await memphis.close()
 