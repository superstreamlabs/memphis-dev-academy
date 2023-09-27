from memphis import Memphis, Headers
from memphis.types import Retention, Storage
import asyncio

# These are examples of the functions available by the Memphis API

### Memphis.connect

async def memphis_connect_password():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.connect(
      host = "localhost",
      username = "root",
      password = "memphis",
    )
    
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_connect_token():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.connect(
      host = "localhost",
      username = "user_id",
      connection_token = "token",
    )
    
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_connect_tls():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.connect(
      host = "localhost",
      username = "user_id",
      key_file = "~/tls_file_path.key"
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()


### Memphis.station

async def memphis_station_default():
  try:
    memphis = Memphis()
    await memphis.station(
        name = "my_station"
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_station_retention():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )
  
    await memphis.station(
        name = "my_station",
        retention_type = Retention.MESSAGES,
        retention_value = 10
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_station_storage():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.station(
        name = "my_station",
        storage_type = Storage.MEMORY
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_station_replicas():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.station(
        name = "my_station",
        replicas = 3
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_station_idempotency():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.station(
        name = "my_station",
        idempotency_window_ms = 180000
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_station_schema():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.station(
        name = "my_station",
        schema = "sensor_logs"
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_station_poison_dls():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.station(
        name = "my_station",
        schema = "sensor_logs",
        send_poison_msg_to_dls = True,
        send_schema_failed_msg_to_dls = False
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_station_poison_dls_to_station():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.station(
        name = "my_station",
        schema = "sensor_logs",
        send_poison_msg_to_dls = True,
        send_schema_failed_msg_to_dls = False,
        dls_station = "bad_sensor_messages_station"
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_station_tiered_storage():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.station(
        name = "my_station",
        tiered_storage_enabled = True
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

async def memphis_station_partitions():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

    await memphis.station(
        name = "my_station",
        partitions_number = 3 
   )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

### Memphis.attach_schema

  # This function is deprecated. Use enforce_schema instead    

### Memphis.enforce_schema

async def memphis_station_enforce_schema():
  try:
    memphis = Memphis()

    await memphis.connect(
              host = "localhost",
              username = "root", 
              password = "memphis",
      )

    await memphis.enforce_schmea(
        name = "my_schmea",
        station_name = "my_station"
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

### Memphis.detach_schema

async def memphis_station_detach_schema():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )
    
    await memphis.detach_schmea(
        station_name = "my_station"
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

### Memphis.close

async def memphis_station_close():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )
    
    await memphis.detach_schmea(
        station_name = "my_station"
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

### Memphis.proudcer

async def memphis_station_producer():
  try:
    memphis = Memphis()

    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )
    
    await memphis.producer(
        station_name = "my_station",
        producer_name = "new_producer"
    )
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

### Memphis.consumer

### Memphis.produce

### Memphis.fetch_message

### Memphis.create_schema

# if __name__ == '__main__':
#   asyncio.run( )