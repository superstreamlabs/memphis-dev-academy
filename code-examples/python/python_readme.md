# Python Documentation

This document will go over the available memphis functions that users may used in the python API. The python API makes available 4 useful classes. These are the Memphis, Consumer, Producer, and Station classes.

## The Memphis class

The Memphis class has some overlap with the other classes, but also has some unique functionality. With the Memphis class, you have available to you the connect, station, attach_schema, enforce_schema, detach_schema, close, producer, consumer, produce, fetch_message, and create_schema functions.

### Connect

```python
    async def connect(
        self,
        host: str,
        username: str,
        account_id: int = 1,
        connection_token: str = "",
        password: str = "",
        port: int = 6666,
        reconnect: bool = True,
        max_reconnect: int = 10,
        reconnect_interval_ms: int = 1500,
        timeout_ms: int = 2000,
        cert_file: str = "",
        key_file: str = "",
        ca_file: str = "",
    )
```

The connect function in the Memphis class allows for the connection to Memphis. Connecting to Memphis (cloud or open-source) will be needed in order to use any of the other functionality of the Memphis class.

What arguments are used with the Memphis.connect function change depending on the type of connection being made. A standard password-based connection would look like this (using the defualt root memphis login with Memphis open-source):

```python
    # Imports hidden. See other examples

    try:
        memphis = Memphis()
        await memphis.connect(
            host = "localhost",
            username = "root",
            password = "memphis",
            # port = 6666, default port
            # reconnect = True, default reconnect setting
            # max_reconnect = 10, default number of reconnect attempts
            # reconnect_interval_ms = 1500, default reconnect interval
            # timeout_ms = 2000, default duration of time for the connection to timeout
        )
    except Exception as e:
        print(e)
    finally:
        await memphis.close()
```

A JWT, token-based connection would look like this:

```python
    # Imports hidden. See other examples

    try:
        memphis = Memphis()
        await memphis.connect(
            host = "localhost",
            username = "user",
            connection_token = "token",
            # port = 6666, default port
            # reconnect = True, default reconnect setting
            # max_reconnect = 10, default number of reconnect attempts
            # reconnect_interval_ms = 1500, default reconnect interval
            # timeout_ms = 2000, default duration of time for the connection to timeout
        )
    except Exception as e:
        print(e)
    finally:
        await memphis.close()
```

Memphis needs to be configured to use token based connection. See the [docs](https://docs.memphis.dev/memphis/memphis-broker/concepts/security) for help doing this.

A TLS based connection would look like this:

```python
    # Imports hidden. See other examples

    try:
        memphis = Memphis()
        await memphis.connect(
            host = "localhost",
            username = "user",
            key_file = "~/tls_file_path.key",
            cert_file = "~/tls_cert_file_path.crt",
            ca_file = "~/tls_ca_file_path.crt",
            # port = 6666, default port
            # reconnect = True, default reconnect setting
            # max_reconnect = 10, default number of reconnect attempts
            # reconnect_interval_ms = 1500, default reconnect interval
            # timeout_ms = 2000, default duration of time for the connection to timeout
        )
    except Exception as e:
        print(e)
    finally:
```
Memphis needs to configured for these use cases. To configure memphis to use TLS see the [docs](https://docs.memphis.dev/memphis/open-source-installation/kubernetes/production-best-practices#memphis-metadata-tls-connection-configuration). 

> For the rest of the examples, the try-except statement will be withheld to assist with the succinctness of the examples. For full example functions for each use case see the memphis_examples.py file.

### station 

```python
    async def station(
        self,
        name: str,
        retention_type: Retention = Retention.MAX_MESSAGE_AGE_SECONDS,
        retention_value: int = 604800,
        storage_type: Storage = Storage.DISK,
        replicas: int = 1,
        idempotency_window_ms: int = 120000,
        schema_name: str = "",
        send_poison_msg_to_dls: bool = True,
        send_schema_failed_msg_to_dls: bool = True,
        tiered_storage_enabled: bool = False,
        partitions_number: int = 1,
        dls_station: str = "",
    )
```

The station function is used to create a station. Using the different arguemnts, one can programically create many different types of stations. The Memphis UI can also be used to create stations to the same effect. 

A minimal example, using all default values would simply create a station with the given name:

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.station(
        name = "my_station"
    )
```

To change what criteria the station uses to decide if a message should be retained in the station, change the retention type. The different types of retention are documented [here](https://github.com/memphisdev/memphis.py#retention-types) in the python README. 

The unit of the rentention value will vary depending on the retention_type. The [previous link](https://github.com/memphisdev/memphis.py#retention-types) also describes what units will be used. 

Here is an example of a station which will only hold up to 10 messages:

```python
    memphis = Memphis()

    await memphis.connect(...)
    
    await memphis.station(
        name = "my_station",
        retention_type = Retention.MESSAGES,
        retention_value = 10
    )
```

Memphis stations can either store Messages on disk or in memory. A comparison of those types of storage can be found [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#tier-1-local-storage).

Here is an example of how to create a station that uses Memory as its storage type:

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.station(
        name = "my_station",
        storage_type = Storage.MEMORY
    )
```

In order to make a station more redundant, replicas can be used. Read more about replicas [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#replicas-mirroring). Note that replicas are only available in cluster mode. Cluster mode can be enabled in the [Helm settings](https://docs.memphis.dev/memphis/open-source-installation/kubernetes/1-installation#appendix-b-helm-deployment-options) when deploying Memphis with Kubernetes.

Here is an example of creating a station with 3 replicas:

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.station(
        name = "my_station",
        replicas = 3
    )
```

Idempotency defines how Memphis will prevent duplicate messages from being stored or consumed. The duration of time the message ID's will be stored in the station can be set with idempotency_window_ms. If the environment Memphis is deployed in has unreliably connection and/or a lot of latency, increasing this value might be desiriable. The default duration of time is set to two minutes. Read more about idempotency [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/idempotency).

Here is an example of changing the idempotency window to 3 seconds:

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.station(
        name = "my_station",
        idempotency_window_ms = 180000
    )
```

The schema name is used to set a schema to be enforced by the station. The default value of "" ensures that no schema is enforced. Here is an example of changing the schema to a defined schema in schemaverse called "sensor_logs":

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.station(
        name = "my_station",
        schema = "sensor_logs"
    )
```

There are two parameters for sending messages to the [dead-letter station(DLS)](https://docs.memphis.dev/memphis/memphis-broker/concepts/dead-letter#terminology). These are send_poison_msg_to_dls and send_schema_failed_msg_to_dls. 

Here is an example of sending poison messages to the DLS but not messages which fail to conform to the given schema.

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.station(
        name = "my_station",
        schema = "sensor_logs",
        send_poison_msg_to_dls = True,
        send_schema_failed_msg_to_dls = False
    )
```

When either of the DLS flags are set to True, a station can also be set to handle these events. To set a station as the station to where schema failed or poison messages will be set to, use the dls_station parameter:

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.station(
        name = "my_station",
        schema = "sensor_logs",
        send_poison_msg_to_dls = True,
        send_schema_failed_msg_to_dls = False,
        dls_station = "bad_sensor_messages_station"
    )
```

When the retention value is met, Mempihs by default will delete old messages. If tiered storage is setup, Memphis can instead move messages to tier 2 storage. Read more about tiered storage [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#storage-tiering). Enable this setting with the respective flag:

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.station(
        name = "my_station",
        tiered_storage_enabled = True
    )
```

[Partitioning](https://docs.memphis.dev/memphis/memphis-broker/concepts/station#partitions) might be useful for a station. To have a station partitioned, simply change the partitions number:

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.station(
        name = "my_station",
        partitions_number = 3
    )
```

### attach_schema 

This function is deprecated. Use enforce_schema instead    

### enforce_schema 

```python
async def enforce_schema(self, name, station_name)
```

To add a schema to an already created station, enforce_schema can be used. Here is an example using enforce_schmea to add a schema to a station:

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.enforce_schmea(
        name = "my_schmea",
        station_name = "my_station"
    )
```

### detach_schema 

```python
    async def detach_schema(self, station_name)
```

To remove a schema from an already created station, detach_schema can be used. Here is an example of removing a schmea from a station:

```python
    memphis = Memphis()
   
    await memphis.connect(...)

    await memphis.detach_schmea(
        station_name = "my_station"
    )
```

### close 

```python
    async def close(self)
```

To safely and correctly close down a Memphis connection use the close function. Here is an example of closing a Memphis connection.

```python
    memphis = Memphis()
   
    await memphis.connect(...)

    await memphis.close()
```

### producer 

```python
    async def producer(
        self,
        station_name: str,
        producer_name: str,
        generate_random_suffix: bool = False, #Depreicated
    )
```

Use the Memphis producer function to create a producer. Here is an example of creating a producer for a given station:

```python
    memphis = Memphis()
   
    await memphis.connect(...)

    await memphis.producer(
        station_name = "my_station",
        producer_name = "new_producer"
    )
```

### consumer 

```python
    async def consumer(
        self,
        station_name: str,
        consumer_name: str,
        consumer_group: str = "",
        pull_interval_ms: int = 1000,
        batch_size: int = 10,
        batch_max_time_to_wait_ms: int = 5000,
        max_ack_time_ms: int = 30000,
        max_msg_deliveries: int = 10,
        generate_random_suffix: bool = False,
        start_consume_from_sequence: int = 1,
        last_messages: int = -1,
    )
```

Use the Memphis consumer function to create a Consumer. It offeres some extra options that may be useful.

Here is an example on how to create a consumer with all of the default options:

```python
    memphis = Memphis()

    await memphis.connect(...)

    consumer = await Memphis.consumer(
        station_name = "my_station",
        consumer_name: "new_consumer",
    )
```

To create a consumer in a consumer group, add the consumer_group parameter:

```python
    memphis = Memphis()

    await memphis.connect(...)

    consumer = await Memphis.consumer(
        station_name = "my_station",
        consumer_name: "new_consumer",
        consumer_group: "consumer_group_1"
    )
```

When using Consumer.consume, the consumer will continue to consume in an infinite loop. To change the rate at which the consumer polls, change the pull_interval_ms parameter:

```python
    memphis = Memphis()

    await memphis.connect(...)

    consumer = await Memphis.consumer(
        station_name = "my_station",
        consumer_name = "new_consumer",
        pull_interval_ms = 2000
    )
```

Every time the consumer polls, the consumer will try to take batch_size number of elements from the station. However, sometimes there are not enough messages in the station for the consumer to consume a full batch. In this case, the consumer will continue to wait until either batch_size messages are gathered or the time in milliseconds specified by batch_max_time_to_wait_ms is reached. 

Here is an example of a consumer that will try to poll 100 messages every 10 seconds while waiting up to 15 seconds for all messages to reach the consumer.

```python
    memphis = Memphis()

    await memphis.connect(...)

    consumer = await Memphis.consumer(
        station_name = "my_station",
        consumer_name = "new_consumer",
        pull_interval_ms = 10000,
        batch_size = 100,
        batch_max_time_to_wait_ms = 15000
    )
```

The max_msg_deliveries parameter allows the user how many messages the consumer is able to consume before consuming more. The max_ack_time_ms Here is an example where the consumer will only hold up to one batch of messages at a time:

```python
    memphis = Memphis()

    await memphis.connect(...)
    
    consumer = await Memphis.consumer(
        station_name = "my_station",
        consumer_name = "new_consumer",
        pull_interval_ms = 10000,
        batch_size = 100,
        batch_max_time_to_wait_ms = 15000,
        max_msg_deliveries = 100
    )
```

### produce

```python   
    async def produce(
        self,
        station_name: str,
        producer_name: str,
        message,
        generate_random_suffix: bool = False,
        ack_wait_sec: int = 15,
        headers: Union[Headers, None] = None,
        async_produce: bool = False,
        msg_id: Union[str, None] = None,
        producer_partition_key: Union[str, None] = None
    )
```

The produce function allows for the user to produce a message without discretely creating a producer. Because this creates a producer for every message, it is better to create a producer if many message need to be produced. 

Here is a minimal example of creating a producer:

```python
   memphis = Memphis()

    await memphis.connect(...)
    
    await memphis.produce(
        station_name = "some_station",
        producer_name = "temp_producer",
        message = {'some': 'message'}, 
    )
```

For message data formats see [here](https://docs.memphis.dev/memphis/memphis-schemaverse/formats/produce-consume). 

When producing many messages with a producer, async_produce may be used to help increase the performance of the producer. By default, a producer will block until its message is ack'd. By using the async_produce parameter, messages may be sent while still waiting for the ack of previously sent messages. This reduces preceived network latency and will allow for producers to produce more messages. 

Here is an example of a produce function call that waits up to 30 seconds for an acknowledgement from memphis and does so in an async manner:

```python
   memphis = Memphis()

    await memphis.connect(...)
    
    await memphis.produce(
        station_name = "some_station",
        producer_name = "temp_producer",
        message = {'some':'message'},
        ack_wait_sec = 30,
        async_produce = True
    )
```

As discussed before in the station section, idempotency is an important feature of memphis. To achieve idempotency, an id must be assigned to messages that are being produced. Use the msg_id parameter for this purpose.

```python
   memphis = Memphis()

    await memphis.connect(...)
    
    await memphis.produce(
        station_name = "some_station",
        producer_name = "temp_producer",
        message = {'some':'message'},
        msg_id = '42'
    )
```

To add message headers to the message, use the headers parameter. Headers can help with observability when using certain 3rd party to help monitor the behavior of memphis. See [here](https://docs.memphis.dev/memphis/memphis-broker/comparisons/aws-sqs-vs-memphis#observability) for more details.

```python
   memphis = Memphis()

    await memphis.connect(...)
    
    await memphis.produce(
        station_name = "some_station",
        producer_name = "temp_producer",
        message = {'some':'message'},
        headers = {
            'trace_header': 'track_me_123'
        }
    )
```

Lastly, memphis can produce to a specific partition in a station. To do so, use the producer_partition_key parameter:

```python
   memphis = Memphis()

    await memphis.connect(...)
    
    await memphis.produce(
        station_name = "some_station",
        producer_name = "temp_producer",
        message = {'some':'message'},
        producer_partition_key = "2nd_partition"
    )
```

### fetch_message 

```python
    async def fetch_messages(
            self,
            station_name: str,
            consumer_name: str,
            consumer_group: str = "",
            batch_size: int = 10,
            batch_max_time_to_wait_ms: int = 5000,
            max_ack_time_ms: int = 30000,
            max_msg_deliveries: int = 10,
            generate_random_suffix: bool = False,
            start_consume_from_sequence: int = 1,
            last_messages: int = -1,
            consumer_partition_key: str = None,
    )
```
Use the fetch_message function in order to consume a batch of messages without having to create a consumer manually. Because this function creates a consumer on each call, it is more performative to create a consumer with the Memphis.consumer function and to use that to do many calls to Consumer.fetch.

Because of the overlap of this method and Consumer.fetch and Consumer.consume, here is one example for fetching a batch of 5 messages, skipping the first 3 in the station:

```python
    memphis = Memphis()

    await memphis.connect(...)

    await Memphis.fetch_messages(
        station_name = "my_station",
        consumer_name = "new_consumer",
        batch_size = 5,
        start_consume_from_sequence = 4
    )
```

### create_schema 

```python
    async def create_schema(self, schema_name:str, schema_type:str, schema_path:str)
```

The create_schema creates a schema. To use this function, simply name the schema, list its type and then give a file path to the schema file.

```python
    memphis = Memphis()

    await memphis.connect(...)

    await memphis.create_schema(
        schema_name = "my_new_schema",
        schema_type = "json",
        schema_path = "~/schemas/my_new_json_schmea.json"
    )

```