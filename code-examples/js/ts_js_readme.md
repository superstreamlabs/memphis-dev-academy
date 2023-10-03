# TS/JS Documentation

This document will go over the available memphis functions that users may used in the Node API. The Node API makes available 4 useful classes. These are the Memphis, Consumer, Producer, and Station classes.

## The Memphis class

The Memphis class has some overlap with the other classes, but also has some unique functionality. With the Memphis class, you have available to you the connect, station, enforceSchema, detachSchema, close, producer, consumer, produce, fetchMessages, and createSchema functions.

### Connect

```typescript
  connect({
    host,
    port = 6666,
    username,
    accountId = 1,
    connectionToken = '',
    password = '',
    reconnect = true,
    maxReconnect = 10,
    reconnectIntervalMs = 1500,
    timeoutMs = 2000,
    keyFile = '',
    certFile = '',
    caFile = '',
    suppressLogs = false
  }: {
    host: string;
    port?: number;
    username: string;
    accountId?: number;
    connectionToken?: string;
    password?: string;
    reconnect?: boolean;
    maxReconnect?: number;
    reconnectIntervalMs?: number;
    timeoutMs?: number;
    keyFile?: string;
    certFile?: string;
    caFile?: string;
    suppressLogs?: boolean;
  }): Promise<Memphis>

```

The connect function in the Memphis class allows for the connection to Memphis. Connecting to Memphis (cloud or open-source) will be needed in order to use any of the other functionality of the Memphis class.

What arguments are used with the Memphis.connect function change depending on the type of connection being made. A standard password-based connection would look like this (using the defualt root memphis login with Memphis open-source):

```typescript
async function connectPassword(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
                host: "localhost",
                username: "root", // (root/application type user)
                password: "memphis" 
                });
    }catch(exception){
        // Handle exception
    }
}
```

A JWT, token-based connection would look like this:

```typescript
async function connectToken(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
                host: "localhost",
                username: "root", // (root/application type user)
                connectionToken: "token"
                });
    }catch(exception){
        // Handle exception
    }
}
```

Memphis needs to be configured to use token based connection. See the [docs](https://docs.memphis.dev/memphis/memphis-broker/concepts/security) for help doing this.

A TLS based connection would look like this:

```typescript
async function connectTLS(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
                host: "localhost",
                username: "root", // (root/application type user)
                keyFile: "~/tls_file_path.key",
                certFile: "~/tls_cert_file_path.crt",
                caFile: "~/tls_ca_file_path.crt"
                });
    }catch(exception){
        // Handle exception
    }
}
```

Memphis needs to configured for these use cases. To configure memphis to use TLS see the [docs](https://docs.memphis.dev/memphis/open-source-installation/kubernetes/production-best-practices#memphis-metadata-tls-connection-configuration). 


### station 
```typescript
  async station({
    name,
    retentionType = retentionTypes.MAX_MESSAGE_AGE_SECONDS,
    retentionValue = 604800,
    storageType = storageTypes.DISK,
    replicas = 1,
    idempotencyWindowMs = 120000,
    schemaName = '',
    sendPoisonMsgToDls = true,
    sendSchemaFailedMsgToDls = true,
    tieredStorageEnabled = false,
    partitionsNumber = 1,
    dlsStation = '',
  }: {
    name: string;
    retentionType?: string;
    retentionValue?: number;
    storageType?: string;
    replicas?: number;
    idempotencyWindowMs?: number;
    schemaName?: string;
    sendPoisonMsgToDls?: boolean;
    sendSchemaFailedMsgToDls?: boolean;
    tieredStorageEnabled?: boolean;
    partitionsNumber?: number;
    dlsStation?: string;
  }): Promise<Station>
```

The station function is used to create a station. Using the different arguemnts, one can programically create many different types of stations. The Memphis UI can also be used to create stations to the same effect. 

A minimal example, using all default values would simply create a station with the given name:

```typescript
async function stationDefault(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.station({
            name: "myStation"
        });
    }catch(exception){
        // Handle exception
    }
}
```

To change what criteria the station uses to decide if a message should be retained in the station, change the retention type. The different types of retention are documented [here](https://github.com/memphisdev/memphis.js#retention-types) in the node README. 

The unit of the rentention value will vary depending on the RetentionType. The [previous link](https://github.com/memphisdev/memphis.js#retention-types) also describes what units will be used. 

Here is an example of a station which will only hold up to 10 messages:

```typescript
async function stationRetentionType(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.station({
            name: "myStation",
            retentionType: memphis.retentionTypes.MESSAGES
        });
    }catch(exception){
        // Handle exception
    }
}
```

Memphis stations can either store Messages on disk or in memory. A comparison of those types of storage can be found [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#tier-1-local-storage).

Here is an example of how to create a station that uses Memory as its storage type:

```typescript
async function stationMemoryStorage(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.station({
            name: "myStation",
            storageType: memphis.storageTypes.MEMORY
        });
    }catch(exception){
        // Handle exception
    }
}
```

In order to make a station more redundant, replicas can be used. Read more about replicas [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#replicas-mirroring). Note that replicas are only available in cluster mode. Cluster mode can be enabled in the [Helm settings](https://docs.memphis.dev/memphis/open-source-installation/kubernetes/1-installation#appendix-b-helm-deployment-options) when deploying Memphis with Kubernetes.

Here is an example of creating a station with 3 replicas:

```typescript
async function stationWithReplicas(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.station({
            name: "myStation",
            replicas: 3
        });
    }catch(exception){
        // Handle exception
    }
}
```

Idempotency defines how Memphis will prevent duplicate messages from being stored or consumed. The duration of time the message ID's will be stored in the station can be set with idempotencyWindowsMs. If the environment Memphis is deployed in has unreliably connection and/or a lot of latency, increasing this value might be desiriable. The default duration of time is set to two minutes. Read more about idempotency [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/idempotency).

Here is an example of changing the idempotency window to 3 seconds:

```typescript
async function stationIdempotency(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.station({
            name: "myStation",
            idempotencyWindowMs: 180000
        });
    }catch(exception){
        // Handle exception
    }
}
```

The schema name is used to set a schema to be enforced by the station. The default value of "" ensures that no schema is enforced. Here is an example of changing the schema to a defined schema in schemaverse called "sensorLogs":

```typescript
async function stationWithSchema(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.station({
            name: "myStation",
            schemaName: "sensorLogs"
        });
    }catch(exception){
        // Handle exception
    }
}
```

There are two parameters for sending messages to the [dead-letter station(DLS)](https://docs.memphis.dev/memphis/memphis-broker/concepts/dead-letter#terminology). These are sendPoisonMsgToDls and sendSchemaFailedMsgToDls. 

Here is an example of sending poison messages to the DLS but not messages which fail to conform to the given schema.

```typescript
async function stationWithDeadLetter(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.station({
            name: "myStation",
            sendPoisonMsgToDls: true,
            sendSchemaFailedMsgToDls: false
        });
    }catch(exception){
        // Handle exception
    }
}
```

When either of the DLS flags are set to True, a station can also be set to handle these events. To set a station as the station to where schema failed or poison messages will be set to, use the DlsStation parameter:

```typescript
async function stationWithDeadLetterToStation(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.station({
            name: "myStation",
            sendPoisonMsgToDls: true,
            sendSchemaFailedMsgToDls: false,
            dlsStation: "badSensorLogsStation"
        });
    }catch(exception){
        // Handle exception
    }
}
```

When the retention value is met, Memphis by default will delete old messages. If tiered storage is setup, Memphis can instead move messages to tier 2 storage. Read more about tiered storage [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#storage-tiering). Enable this setting with the respective flag:

```typescript
async function stationWithTieredStorage(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.station({
            name: "myStation",
            tieredStorageEnabled: true
        });
    }catch(exception){
        // Handle exception
    }
}
```

[Partitioning](https://docs.memphis.dev/memphis/memphis-broker/concepts/station#partitions) might be useful for a station. To have a station partitioned, simply change the partitions number:

```typescript
async function stationWithPartitions(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.station({
            name: "myStation",
            partitionsNumber: 3
        });
    }catch(exception){
        // Handle exception
    }
}
```

### attachSchema 

This function is deprecated. Use enforceSchema instead    

### enforceSchema 
```typescript
  async enforceSchema({
    name,
    stationName
  }: {
    name: string;
    stationName: string;
  }): Promise<void>
```

To add a schema to an already created station, enforceSchema can be used. Here is an example using enforceSchema to add a schema to a station:

```typescript
async function enforceSchema(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphis.enforceSchema({
            name: "mySchema",
            stationName: "myStation"
        });
    }catch(exception){
        // Handle exception
    }
}
```

### detachSchema 
```typescript

async detachSchema({ stationName }: { stationName: string }): Promise<void>

```

To remove a schema from an already created station, detachSchema can be used. Here is an example of removing a schmea from a station:

```typescript
async function detachSchema(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.detachSchema({
            stationName: "myStation",
        });
    }catch(exception){
        // Handle exception
    }
}
```

### close 

```typescript
async close()
```

To safely and correctly close down a Memphis connection use the close function. Here is an example of closing a Memphis connection.

```typescript
async function close(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.close();
    }catch(exception){
        // Handle exception
    }
}
```

### producer 
```typescript
async producer({
    stationName,
    producerName,
    genUniqueSuffix = false
  }: {
    stationName: string;
    producerName: string;
    genUniqueSuffix?: boolean;
  }): Promise<Producer>
```

Use the Memphis producer function to create a producer. Here is an example of creating a producer for a given station:

```typescript
async function producerBasic(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.producer({
            stationName: "myStation",
            producerName: "myNewProducer"
        });
    }catch(exception){
        // Handle exception
    }
}
```

### consumer

```typescript
async consumer({
    stationName,
    consumerName,
    consumerGroup = '',
    pullIntervalMs = 1000,
    batchSize = 10,
    batchMaxTimeToWaitMs = 5000,
    maxAckTimeMs = 30000,
    maxMsgDeliveries = 10,
    genUniqueSuffix = false,
    startConsumeFromSequence = 1,
    lastMessages = -1,
    consumerPartitionKey = null,
  }: {
    stationName: string;
    consumerName: string;
    consumerGroup?: string;
    pullIntervalMs?: number;
    batchSize?: number;
    batchMaxTimeToWaitMs?: number;
    maxAckTimeMs?: number;
    maxMsgDeliveries?: number;
    genUniqueSuffix?: boolean;
    startConsumeFromSequence?: number;
    lastMessages?: number;
    consumerPartitionKey?: string;
  }): Promise<Consumer>
```

Use the Memphis consumer function to create a Consumer. It offeres some extra options that may be useful.

Here is an example on how to create a consumer with all of the default options:

```typescript
async function consumerDefualt(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.consumer({
            stationName: "myStation",
            consumerName: "newConsumer"
        });
    }catch(exception){
        // Handle exception
    }
}
```

To create a consumer in a consumer group, add the consumerGroup parameter:

```typescript
async function consumerGroup(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.consumer({
            stationName: "myStation",
            consumerName: "newConsumer",
            consumerGroup: "consumerGroup1"
        });
    }catch(exception){
        // Handle exception
    }
}
```

When using Consumer.consume, the consumer will continue to consume in an infinite loop. To change the rate at which the consumer polls, change the pullIntervalMs parameter:

```typescript
async function consumerPollInterval(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.consumer({
            stationName: "myStation",
            consumerName: "newConsumer",
            pullIntervalMs: 2000
        });
    }catch(exception){
        // Handle exception
    }
}
```

Every time the consumer polls, the consumer will try to take batchSize number of elements from the station. However, sometimes there are not enough messages in the station for the consumer to consume a full batch. In this case, the consumer will continue to wait until either batchSize messages are gathered or the time in milliseconds specified by batchMaxTimeToWaitMs is reached. 

Here is an example of a consumer that will try to poll 100 messages every 10 seconds while waiting up to 15 seconds for all messages to reach the consumer.

```typescript
async function consumerBatched(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.consumer({
            stationName: "myStation",
            consumerName: "newConsumer",
            pullIntervalMs: 10000,
            batchSize: 100,
            batchMaxTimeToWaitMs: 15000
        });
    }catch(exception){
        // Handle exception
    }
}
```

The maxMsgDeliveries parameter allows the user how many messages the consumer is able to consume before consuming more. 

```typescript
async function consumerMaxMessages(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.consumer({
            stationName: "myStation",
            consumerName: "newConsumer",
            pullIntervalMs: 10000,
            batchSize: 100,
            batchMaxTimeToWaitMs: 15000,
            maxMsgDeliveries: 100
        });
    }catch(exception){
        // Handle exception
    }
}
```

### produce

```typescript
public async produce({
    stationName,
    producerName,
    genUniqueSuffix = false,
    message,
    ackWaitSec,
    asyncProduce,
    headers,
    msgId,
    producerPartitionKey = null
  }: {
    stationName: string;
    producerName: string;
    genUniqueSuffix?: boolean;
    message: any;
    ackWaitSec?: number;
    asyncProduce?: boolean;
    headers?: any;
    msgId?: string;
    producerPartitionKey?: string;
  }): Promise<void>
```


The produce function allows for the user to produce a message without discretely creating a producer. Because this creates a producer for every message, it is better to create a producer if many message need to be produced. 

Here is a minimal example of creating a producer:

```typescript
async function produceFromConnection(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.produce({
            stationName: "myStation",
            producerName: "tempProducer",
            message: {some: "message"}
        });
    }catch(exception){
        // Handle exception
    }
}
```

For message data formats see [here](https://docs.memphis.dev/memphis/memphis-schemaverse/formats/produce-consume). 

When producing many messages with a producer, asyncProduce may be used to help increase the performance of the producer. By default, a producer will block until its message is ack'd. By using the asyncProduce parameter, messages may be sent while still waiting for the ack of previously sent messages. This reduces preceived network latency and will allow for producers to produce more messages. 

Here is an example of a produce function call that waits up to 30 seconds for an acknowledgement from memphis and does so in an async manner:

```typescript
async function produceAsync(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.produce({
            stationName: "myStation",
            producerName: "tempProducer",
            message: {some: "message"},
            ackWaitSec: 30,
            asyncProduce: true
        });
    }catch(exception){
        // Handle exception
    }
}
```

As discussed before in the station section, idempotency is an important feature of memphis. To achieve idempotency, an id must be assigned to messages that are being produced. Use the msgId parameter for this purpose.

```typescript
async function produceWithIdempotency(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.produce({
            stationName: "myStation",
            producerName: "tempProducer",
            message: {some: "message"},
            msgId: "42"
        });
    }catch(exception){
        // Handle exception
    }
}
```

To add message headers to the message, use the headers function to create a headers object which you can add headers to. Headers can help with observability when using certain 3rd party to help monitor the behavior of memphis. See [here](https://docs.memphis.dev/memphis/memphis-broker/comparisons/aws-sqs-vs-memphis#observability) for more details.

```typescript
async function produceWithHeaders(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});

        let headers = memphis.headers()
        headers.add("trace_header_example", "track_me_123")

        await memphisConnection.produce({
            stationName: "myStation",
            producerName: "tempProducer",
            message: {some: "message"},
            headers: headers
        });
    }catch(exception){
        // Handle exception
    }
}
```

Lastly, memphis can produce to a specific partition in a station. To do so, use the producerPartitionKey parameter:

```typescript
async function produceWithPartition(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.produce({
            stationName: "myStation",
            producerName: "tempProducer",
            message: {some: "message"},
            producerPartitionKey: "somePartition"
        });
    }catch(exception){
        // Handle exception
    }
}
```

### fetchMessages 

```typescript
public async fetchMessages({
    stationName,
    consumerName,
    consumerGroup = '',
    genUniqueSuffix = false,
    batchSize = 10,
    maxAckTimeMs = 30000,
    batchMaxTimeToWaitMs = 5000,
    maxMsgDeliveries = 10,
    startConsumeFromSequence = 1,
    lastMessages = -1,
    consumerPartitionKey = null,
  }: {
    stationName: string;
    consumerName: string;
    consumerGroup?: string;
    genUniqueSuffix?: boolean;
    batchSize?: number;
    maxAckTimeMs?: number;
    batchMaxTimeToWaitMs?: number;
    maxMsgDeliveries?: number;
    startConsumeFromSequence?: number;
    lastMessages?: number;
    consumerPartitionKey?: string;
  }): Promise<Message[]>
```

Use the fetchMessages function in order to consume a batch of messages without having to create a consumer manually. Because this function creates a consumer on each call, it is more performative to create a consumer with the Memphis.consumer function and to use that to do many calls to Consumer.fetch.

Because of the overlap of this method and Consumer.fetch and Consumer.consume, here is one example for fetching a batch of 5 messages, skipping the first 3 in the station:

```typescript
async function fetchMessages(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.fetchMessages({
            stationName: "myStation",
            consumerName: "tempConsumer",
            batchSize: 5,
            startConsumeFromSequence: 4
        });
    }catch(exception){
        // Handle exception
    }
}
```

### createSchema 

```typescript
async createSchema({
    schemaName,
    schemaType,
    schemaFilePath
  }: {
    schemaName: string;
    schemaType: string;
    schemaFilePath: string;
  }): Promise<void>
```

The createSchema method creates a schema. To use this function, simply name the schema, list its type and then give a file path to the schema file.

```typescript
async function createSchema(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({...});
        await memphisConnection.createSchema({
            schemaName: "newSchema",
            schemaType: "json",
            schemaFilePath: "~/schemas/my_schema_path.json"
        });
    }catch(exception){
        // Handle exception
    }
}
```