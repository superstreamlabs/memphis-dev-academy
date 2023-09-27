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

Memphis needs to be configured to use token based connection. See the (docs)[https://docs.memphis.dev/memphis/memphis-broker/concepts/security] for help doing this.

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
Memphis needs to configured for these use cases. To configure memphis to use TLS see the (docs)[https://docs.memphis.dev/memphis/open-source-installation/kubernetes/production-best-practices#memphis-metadata-tls-connection-configuration]. 

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
    await memphis.station(
        name = "my_station"
    )
```

To change what criteria the station uses to decide if a message should be retained in the station, change the retention type. The different types of retention are documented (here)[https://github.com/memphisdev/memphis.py#retention-types] in the python README. 

The unit of the rentention value will vary depending on the retention_type. The (previous link)[https://github.com/memphisdev/memphis.py#retention-types] also describes what units will be used. 

Here is an example of a station which will only hold up to 10 messages:

```python
    memphis = Memphis()
    await memphis.station(
        name = "my_station",
        retention_type = Retention.MESSAGES,
        retention_value = 10
    )
```

Memphis stations can either store Messages on disk or in memory. A comparison of those types of storage can be found (here)[https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#tier-1-local-storage].

Here is an example of how to create a station that uses Memory as its storage type:

```python
    memphis = Memphis()
    await memphis.station(
        name = "my_station",
        storage_type = Storage.MEMORY
    )
```

In order to make a station more redundant, replicas can be used. Read more about replicas (here)[https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#replicas-mirroring]. Note that replicas are only available in cluster mode. Cluster mode can be enabled in the (Helm settings)[https://docs.memphis.dev/memphis/open-source-installation/kubernetes/1-installation#appendix-b-helm-deployment-options] when deploying Memphis with Kubernetes.

Here is an example of creating a station with 3 replicas:

```python
    memphis = Memphis()
    await memphis.station(
        name = "my_station",
        replicas = 3
    )
```

Idempotency defines how Memphis will prevent duplicate messages from being stored or consumed. The duration of time the message ID's will be stored in the station can be set with idempotency_window_ms. If the environment Memphis is deployed in has unreliably connection and/or a lot of latency, increasing this value might be desiriable. The default duration of time is set to two minutes. Read more about idempotency (here)[https://docs.memphis.dev/memphis/memphis-broker/concepts/idempotency].

Here is an example of changing the idempotency window to 3 seconds:

```python
    memphis = Memphis()
    await memphis.station(
        name = "my_station",
        idempotency_window_ms = 180000
    )
```

The schema name is used to set a schema to be enforced by the station. The default value of "" ensures that no schema is enforced. Here is an example of changing the schema to a defined schema in schemaverse called "sensor_logs":

```python
    memphis = Memphis()
    await memphis.station(
        name = "my_station",
        schema = "sensor_logs"
    )
```

There are two parameters for sending messages to the (dead-letter station(DLS))[https://docs.memphis.dev/memphis/memphis-broker/concepts/dead-letter#terminology]. These are send_poison_msg_to_dls and send_schema_failed_msg_to_dls. 

Here is an example of sending poison messages to the DLS but not messages which fail to conform to the given schema.

```python
    memphis = Memphis()
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
    await memphis.station(
        name = "my_station",
        schema = "sensor_logs",
        send_poison_msg_to_dls = True,
        send_schema_failed_msg_to_dls = False,
        dls_station = "bad_sensor_messages_station"
    )
```

When the retention value is met, Mempihs by default will delete old messages. If tiered storage is setup, Memphis can instead move messages to tier 2 storage. Read more about tiered storage (here)[https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#storage-tiering]. Enable this setting with the respective flag:

```python
    memphis = Memphis()
    await memphis.station(
        name = "my_station",
        tiered_storage_enabled = True
    )
```

(Partitioning)[https://docs.memphis.dev/memphis/memphis-broker/concepts/station#partitions] might be useful for a station. To have a station partitioned, simply change the partitions number:

```python
    memphis = Memphis()
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
    # Using the default root login with Memphis open-source
    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

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
    # Using the default root login with Memphis open-source
    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

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
    # Using the default root login with Memphis open-source
    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

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
    # Using the default root login with Memphis open-source
    await memphis.connect(
            host = "localhost",
            username = "root", 
            password = "memphis",
    )

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
    consumer = await Memphis.consumer(
        station_name = "my_station",
        consumer_name: "new_consumer",
    )
```

To create a consumer in a consumer group, add the consumer_group parameter:

```python
    memphis = Memphis()
    consumer = await Memphis.consumer(
        station_name = "my_station",
        consumer_name: "new_consumer",
        consumer_group: "consumer_group_1"
    )
```

When using Consumer.consume, the consumer will continue to consume in an infinite loop. To change the rate at which the consumer polls, change the pull_interval_ms parameter:

```python
    memphis = Memphis()
    consumer = await Memphis.consumer(
        station_name = "my_station",
        consumer_name: "new_consumer",
        pull_interval_ms: 2000
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

...

### fetch_message 

...

### create_schema 

...