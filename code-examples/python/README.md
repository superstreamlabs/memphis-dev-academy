<div align="center">
  
  ![Banner- Memphis dev streaming  (2)](https://github.com/memphisdev/memphis.py/assets/107035359/6787500c-d806-4f22-96aa-a182d4c24dfa)
  
</div>

<div align="center">

  <h4>

**[Memphis](https://memphis.dev)** is an intelligent, frictionless message broker.<br>Made to enable developers to build real-time and streaming apps fast.

  </h4>
  
  <a href="https://landscape.cncf.io/?selected=memphis"><img width="200" alt="CNCF Silver Member" src="https://github.com/cncf/artwork/raw/master/other/cncf-member/silver/white/cncf-member-silver-white.svg#gh-dark-mode-only"></a>
  
</div>

<div align="center">
  
  <img width="200" alt="CNCF Silver Member" src="https://github.com/cncf/artwork/raw/master/other/cncf-member/silver/color/cncf-member-silver-color.svg#gh-light-mode-only">
  
</div>
 
 <p align="center">
  <a href="https://memphis.dev/pricing/">Cloud</a> - <a href="https://memphis.dev/docs/">Docs</a> - <a href="https://twitter.com/Memphis_Dev">Twitter</a> - <a href="https://www.youtube.com/channel/UCVdMDLCSxXOqtgrBaRUHKKg">YouTube</a>
</p>

<p align="center">
<a href="https://discord.gg/WZpysvAeTf"><img src="https://img.shields.io/discord/963333392844328961?color=6557ff&label=discord" alt="Discord"></a>
<a href="https://github.com/memphisdev/memphis/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/memphisdev/memphis?color=6557ff"></a> 
  <img src="https://img.shields.io/npm/dw/memphis-dev?color=ffc633&label=installations">
<a href="https://github.com/memphisdev/memphis/blob/master/CODE_OF_CONDUCT.md"><img src="https://img.shields.io/badge/Code%20of%20Conduct-v1.0-ff69b4.svg?color=ffc633" alt="Code Of Conduct"></a> 
<a href="https://docs.memphis.dev/memphis/release-notes/releases/v0.4.2-beta"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/memphisdev/memphis?color=61dfc6"></a>
<img src="https://img.shields.io/github/last-commit/memphisdev/memphis?color=61dfc6&label=last%20commit">
</p>

Memphis.dev is more than a broker. It's a new streaming stack.<br><br>
It accelerates the development of real-time applications that require<br>
high throughput, low latency, small footprint, and multiple protocols,<br>with minimum platform operations, and all the observability you can think of.<br><br>
Highly resilient, distributed architecture, cloud-native, and run on any Kubernetes,<br>on any cloud without zookeeper, bookeeper, or JVM.

## Installation

```sh
$ pip3 install memphis-py
```

Notice: you may receive an error about the "mmh3" package, to solve it please install python3-devel
```sh
$ sudo yum install python3-devel
```

## Importing

```python
from memphis import Memphis, Headers
from memphis.types import Retention, Storage
import asyncio
```

### Connecting to Memphis

First, we need to create Memphis `object` and then connect with Memphis by using `memphis.connect`.

```python
async def main():
  try:
    memphis = Memphis()
    await memphis.connect(
      host="<memphis-host>",
      username="<application-type username>",
      account_id=<account_id>, # Cloud only, ignored otherwise. The account_id can be found in the Memphis UI profile page.
      connection_token="<broker-token>", # Received during application type user creation
      password="<string>", # Deployment dependent - default connection uses token-based authentication
      port=<port>, # defaults to 6666
      reconnect=True, # defaults to True
      max_reconnect=10, # defaults to 10
      reconnect_interval_ms=1500, # defaults to 1500
      timeout_ms=1500, # defaults to 1500
      # TLS connection parameters:
      key_file='<key-client.pem>', 
      cert_file='<cert-client.pem>', 
      ca_file='<rootCA.pem>'
      )
    ...
  except Exception as e:
    print(e)
  finally:
    await memphis.close()

if __name__ == '__main__':
  asyncio.run(main())
```

Upon connection, all of Memphis' features are available.

### Disconnecting from Memphis

To disconnect from Memphis, call `close()` on the memphis object.

```python
await memphis.close()
```

### Creating a Station
**Unexist stations will be created automatically through the SDK on the first producer/consumer connection with default values.**<br><br>
_If a station already exists nothing happens, the new configuration will not be applied_

```python
station = memphis.station(
  name="<station-name>",
  schema_name="<schema-name>", # defaults to "" (no schema)
  retention_type=Retention.MAX_MESSAGE_AGE_SECONDS, # MAX_MESSAGE_AGE_SECONDS/MESSAGES/BYTES/ACK_BASED(cloud only). Defaults to MAX_MESSAGE_AGE_SECONDS
  retention_value=604800, # defaults to 604800
  storage_type=Storage.DISK, # Storage.DISK/Storage.MEMORY. Defaults to DISK
  replicas=1, # defaults to 1
  idempotency_window_ms=120000, # defaults to 2 minutes
  send_poison_msg_to_dls=True, # defaults to true
  send_schema_failed_msg_to_dls=True, # defaults to true
  tiered_storage_enabled=False, # defaults to false
  partitions_number=1, # defaults to 1 
  dls_station="<station-name>" # defaults to "" (no DLS station) - If selected DLS events will be sent to selected station as well
)
```

### Retention types

Retention types define the methodology behind how a station behaves with its messages. Memphis currently supports the following retention types:

```python
memphis.types.Retention.MAX_MESSAGE_AGE_SECONDS
```

When the retention type is set to MAX_MESSAGE_AGE_SECONDS, messages will persist in the station for the number of seconds specified in the retention_value. 


```python
memphis.types.Retention.MESSAGES
```

When the retention type is set to MESSAGES, the station will only hold up to retention_value messages. The station will delete the oldest messsages to maintain a retention_value number of messages.

```python
memphis.types.Retention.BYTES
```

When the retention type is set to BYTES, the station will only hold up to retention_value BYTES. The oldest messages will be deleted in order to maintain at maximum retention_vlaue BYTES in the station.

```python
memphis.types.Retention.ACK_BASED # for cloud users only
```

When the retention type is set to ACK_BASED, messages in the station will be deleted after they are acked by all subscribed consumer groups.

### Retention Values

The unit of the `retention_value` changes depending on the `retention_type` specified. 

All retention values are of type `int`. The following units are used based on the respective retention type:

`memphis.types.Retention.MAX_MESSAGE_AGE_SECONDS` is **in seconds**,<br>
`memphis.types.Retention.MESSAGES` is a **number of messages**,<br>
`memphis.types.Retention.BYTES` is a **number of bytes**, <br>
With `memphis.ACK_BASED`, the `retention_type` is ignored 

### Storage types

Memphis currently supports the following types of messages storage:

```python
memphis.types.Storage.DISK
```
When storage is set to DISK, messages are stored on disk.

```python
memphis.types.Storage.MEMORY
```
When storage is set to MEMORY, messages are stored in the system memory.

### Station partitions

Memphis stations are created with 1 patition by default.
You can change the patitions number as you wish in order to scale your stations. See the [documentation](https://docs.memphis.dev/memphis/memphis-broker/concepts/station#partitions) for more details on partitions.

### Destroying a Station

Destroying a station will remove all its resources (including producers/consumers)

```python
station.destroy()
```

### Creating a New Schema 

```python
await memphis.create_schema("<schema-name>", "<schema-type>", "<schema-file-path>")
```
Current available schema types - Protobuf / JSON schema / GraphQL schema / Avro

### Enforcing a Schema on an Existing Station

```python
await memphis.enforce_schema("<schema-name>", "<station-name>")
```

### Deprecated  - Attaching a Schema, use enforce_schema instead

```python
await memphis.attach_schema("<schema-name>", "<station-name>")
```

### Detaching a Schema from Station

```python
await memphis.detach_schema("<station-name>")
```

### Produce and Consume messages

The most common client operations are `produce` to send messages and `consume` to
receive messages.

Messages are published to a station and consumed from it by creating a consumer.
Consumers are pull based and consume all the messages in a station unless you are using a consumers group, in this case messages are spread across all members in this group.

Memphis messages are payload agnostic. Payloads are `bytearray`s.

In order to stop getting messages, you have to call `consumer.destroy()`. Destroy will terminate regardless
of whether there are messages in flight for the client.

If a station is created with more than one partition, produce and consume bill be perform in a Round Robin fasion

### Creating a Producer

```python
producer = await memphis.producer(station_name="<station-name>", producer_name="<producer-name>")
```

### Producing a message
Without creating a producer. <br>
 
```python
await memphis.produce(station_name='test_station_py', producer_name='prod_py',
  message='bytearray/protobuf class/dict/string/graphql.language.ast.DocumentNode', # bytearray / protobuf class (schema validated station - protobuf) or bytearray/dict (schema validated station - json schema) or string/bytearray/graphql.language.ast.DocumentNode (schema validated station - graphql schema) or bytearray/dict (schema validated station - avro schema)
  ack_wait_sec=15, # defaults to 15
  headers=headers, # default to {}
  nonblocking=False, #defaults to false
  msg_id="123",
  producer_partition_key="key" #default to None
)
```


With creating a producer. Creating a producer and calling produce on it will increase the performance of producing messages.
```python
await producer.produce(
  message='bytearray/protobuf class/dict/string/graphql.language.ast.DocumentNode', # bytearray / protobuf class (schema validated station - protobuf) or bytearray/dict (schema validated station - json schema) or string/bytearray/graphql.language.ast.DocumentNode (schema validated station - graphql schema) or or bytearray/dict (schema validated station - avro schema)
  ack_wait_sec=15) # defaults to 15
```

### Add headers

```python
headers= Headers()
headers.add("key", "value")
await producer.produce(
  message='bytearray/protobuf class/dict/string/graphql.language.ast.DocumentNode', # bytearray / protobuf class (schema validated station - protobuf) or bytearray/dict (schema validated station - json schema) or string/bytearray/graphql.language.ast.DocumentNode (schema validated station - graphql schema) or or bytearray/dict (schema validated station - avro schema)
  headers=headers) # default to {}
```

### Non-blocking Produce
For better performance, the client won't block requests while waiting for an acknowledgment.

```python
await producer.produce(
  message='bytearray/protobuf class/dict/string/graphql.language.ast.DocumentNode', # bytearray / protobuf class (schema validated station - protobuf) or bytearray/dict (schema validated station - json schema) or string/bytearray/graphql.language.ast.DocumentNode (schema validated station - graphql schema)
  headers={}, nonblocking=True)
```

### Produce using partition key
Use any string to produce messages to a specific partition

```python
await producer.produce(
  message='bytearray/protobuf class/dict/string/graphql.language.ast.DocumentNode', # bytearray / protobuf class (schema validated station - protobuf) or bytearray/dict (schema validated station - json schema) or string/bytearray/graphql.language.ast.DocumentNode (schema validated station - graphql schema)
  producer_partition_key="key") #default to None
```

### Non-blocking Produce with Task Limits
For better performance, the client won't block requests while waiting for an acknowledgment.
If you are producing a large number of messages and see timeout errors, then you may need to
limit the number of concurrent tasks like so:

```python
await producer.produce(
  message='bytearray/protobuf class/dict/string/graphql.language.ast.DocumentNode', # bytearray / protobuf class (schema validated station - protobuf) or bytearray/dict (schema validated station - json schema) or string/bytearray/graphql.language.ast.DocumentNode (schema validated station - graphql schema)
  headers={}, nonblocking=True, limit_concurrent_tasks=500)
```


### Message ID
Stations are idempotent by default for 2 minutes (can be configured), Idempotency achieved by adding a message id

```python
await producer.produce(
  message='bytearray/protobuf class/dict', # bytes / protobuf class (schema validated station - protobuf) or bytes/dict (schema validated station - json schema)
  headers={}, 
  async_produce=True,
  msg_id="123")
```

### Destroying a Producer

```python
producer.destroy()
```

### Creating a Consumer

```python
consumer = await memphis.consumer(
  station_name="<station-name>",
  consumer_name="<consumer-name>",
  consumer_group="<group-name>", # defaults to the consumer name
  pull_interval_ms=1000, # defaults to 1000
  batch_size=10, # defaults to 10
  batch_max_time_to_wait_ms=5000, # defaults to 5000
  max_ack_time_ms=30000, # defaults to 30000
  max_msg_deliveries=10, # defaults to 10
  start_consume_from_sequence=1, # start consuming from a specific sequence. defaults to 1
  last_messages=-1 # consume the last N messages, defaults to -1 (all messages in the station)
)
```

### Setting a context for message handler function

```python
context = {"key": "value"}
consumer.set_context(context)
```

### Processing messages

Once all the messages in the station were consumed the msg_handler will receive error: `Memphis: TimeoutError`.

```python
async def msg_handler(msgs, error, context):
  for msg in msgs:
    print("message: ", msg.get_data())
    await msg.ack()
  if error:
    print(error)
consumer.consume(msg_handler)
```

### Consume using a partition key
The key will be used to consume from a specific partition

```python
consumer.consume(msg_handler,
                 consumer_partition_key = "key" #consume from a specific partition
                )
```

### Fetch a single batch of messages
```python
msgs = await memphis.fetch_messages(
  station_name="<station-name>",
  consumer_name="<consumer-name>",
  consumer_group="<group-name>", # defaults to the consumer name
  batch_size=10, # defaults to 10
  batch_max_time_to_wait_ms=5000, # defaults to 5000
  max_ack_time_ms=30000, # defaults to 30000
  max_msg_deliveries=10, # defaults to 10
  start_consume_from_sequence=1, # start consuming from a specific sequence. defaults to 1
  last_messages=-1, # consume the last N messages, defaults to -1 (all messages in the station))
  consumer_partition_key="key" # used to consume from a specific partition, default to None 
)
```

### Fetch a single batch of messages after creating a consumer
```python
msgs = await consumer.fetch(batch_size=10) # defaults to 10
```

### Acknowledge a message

Acknowledge a message indicates the Memphis server to not re-send the same message again to the same consumer / consumers group

```python
await message.ack()
```

### Delay the message after a given duration

Delay the message and tell Memphis server to re-send the same message again to the same consumer group. The message will be redelivered only in case `consumer.max_msg_deliveries` is not reached yet.

```python
await message.delay(delay_in_seconds)
```

### Get headers 
Get headers per message

```python
headers = message.get_headers()
```

### Get message sequence number
Get message sequence number

```python
sequence_number = msg.get_sequence_number()
```

### Destroying a Consumer

```python
consumer.destroy()
```


### Check connection status

```python
memphis.is_connected()
```
