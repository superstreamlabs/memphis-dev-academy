# Dotnet Documentation

This document will go over the available memphis methods that users may used in the dotnet API. The dotnet API makes available 4 useful classes. These are the Memphis, Consumer, Producer, and Station classes.

## Memphis

With the Memphis class, the power of Memphis is at your fingertips. With a MemphisClient, you can use the CreateClient, CreateStation, AttachSchema, EnforceSchema, DetachSchema, Dispose, CreateProducer, CreateConsumer, Produce, FetchMessages, and CreateSchema methods to fulfill all of your streaming needs.

### Connect

```csharp
public static async Task<MemphisClient> CreateClient(ClientOptions opts,
            CancellationToken cancellationToken = default){...}


public sealed class ClientOptions
{
    public string Host { get; set; }
    public string Username { get; set; }
    public string Password { get; set; }
    public string ConnectionToken { get; set; }
    public int Port { get; set; }
    public bool Reconnect { get; set; }
    public int MaxReconnect { get; set; }
    public int MaxReconnectIntervalMs { get; set; }
    public int TimeoutMs { get; set; }
    public TlsOptions Tls { get; set; }

    /// <summary>
    /// The AccountId field should be set only on the cloud version of Memphis, otherwise it will be ignored.
    /// </summary>
    public int AccountId { get; set; }

    public EventHandler<MemphisConnectionEventArgs> ClosedEventHandler;   
}

public sealed class TlsOptions
{
    public TlsOptions(string fileName)
        => (FileName) = (fileName);

    public TlsOptions(string fileName, string password) : this(fileName)
        => (Password) = (password);

    public TlsOptions(X509Certificate2 certificate)
        => (Certificate) = (certificate);

    public X509Certificate2 Certificate { get; set; }
    public string FileName { get; set; }
    public string Password { get; set; }
    public RemoteCertificateValidationCallback RemoteCertificateValidationCallback { get; set; }
}
```

To connect to Memphis with the dotnet API, the CreateClient method will be used.  

What options are set with the CreateClient method change depending on the type of connection being made. The available options are given in the classes above. A password-based connection would look like this (using the defualt root memphis login with Memphis open-source):

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";  
    var memphisClient = await MemphisClientFactory.CreateClient(options);
}
catch (Exception ex) {
    // handle exception
}
```

A JWT, token-based connection would look like this:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.ConnectionToken = "Token";  
    var memphisClient = await MemphisClientFactory.CreateClient(options);
}
catch (Exception ex) {
    // handle exception
}
```

Memphis needs to be configured to use token based connection. See the [docs](https://docs.memphis.dev/memphis/memphis-broker/concepts/security) for help doing this.

A TLS based connection would look like this:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Tls = new TlsOptions("tlsFileName");
    var memphisClient = await MemphisClientFactory.CreateClient(options);
}
catch (Exception ex)
{
    // handle exception
}
```

Memphis needs to configured for these use cases. To configure memphis to use TLS see the [docs](https://docs.memphis.dev/memphis/open-source-installation/kubernetes/production-best-practices#memphis-metadata-tls-connection-configuration). 


### station 
```csharp
public async Task<MemphisStation> CreateStation(StationOptions stationOptions, CancellationToken cancellationToken = default){...}

public sealed class StationOptions
{
    public string Name { get; set; }
    public string RetentionType { get; set; } = RetentionTypes.MAX_MESSAGE_AGE_SECONDS;
    public int RetentionValue { get; set; } = 604_800;
    public string StorageType { get; set; } = StorageTypes.DISK;
    public int Replicas { get; set; } = 1;
    public int IdempotenceWindowMs { get; set; } = 120_000;
    public string SchemaName { get; set; } = string.Empty;
    public bool SendPoisonMessageToDls { get; set; } = false;
    public bool SendSchemaFailedMessageToDls { get; set; } = true;
    public bool TieredStorageEnabled { get; set; } = false;
    public int PartitionsNumber { get; set; } = 1;

    public string DlsStation { get; set; } = string.Empty;
}
```

The CreateStation method is used to create a station. Using the different options available, one can programically create many different types of stations. The Memphis UI can also be used to create stations to the same effect. 

A minimal example, using all default values would simply create a station with the given name:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var station = await memphisClient.CreateStation(
        stationOptions: new StationOptions
        {
            Name = "MyNewStation"
        }
    );
}
catch (Exception ex)
{
    // handle exception
}
```

To change what criteria the station uses to decide if a message should be retained in the station, change the retention type. The different types of retention are documented [here](https://github.com/memphisdev/memphis.net#retention-types) in the dotnet README. 

The unit of the rentention value will vary depending on the RetentionTypes. The [previous link](https://github.com/memphisdev/memphis.net#retention-types) also describes what units will be used. 

Here is an example of a station which will only hold up to 10 messages:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var station = await memphisClient.CreateStation(
        stationOptions: new StationOptions
        {
            Name = "MyNewStation",
            RetentionType = RetentionTypes.MESSAGES,
            RetentionValue = 10
        }
    );  
}
catch (Exception ex)
{
    // handle exception
}
```

Memphis stations can either store Messages on disk or in memory. A comparison of those types of storage can be found [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#tier-1-local-storage).

Here is an example of how to create a station that uses Memory as its storage type:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var station = await memphisClient.CreateStation(
        stationOptions: new StationOptions
        {
            Name = "MyNewStation",
            StorageType = StorageTypes.MEMORY
        }
    );
}
catch (Exception ex) {
    // handle exception
}
```

In order to make a station more redundant, replicas can be used. Read more about replicas [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#replicas-mirroring). Note that replicas are only available in cluster mode. Cluster mode can be enabled in the [Helm settings](https://docs.memphis.dev/memphis/open-source-installation/kubernetes/1-installation#appendix-b-helm-deployment-options) when deploying Memphis with Kubernetes.

Here is an example of creating a station with 3 replicas:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var station = await memphisClient.CreateStation(
        stationOptions: new StationOptions
        {
            Name = "MyNewStation",
            Replicas = 3
        }
    );
}
catch (Exception ex)
{
    // handle exception
}
```

Idempotency defines how Memphis will prevent duplicate messages from being stored or consumed. The duration of time the message ID's will be stored in the station can be set with IdempotencyWindowMs. If the environment Memphis is deployed in has unreliably connection and/or a lot of latency, increasing this value might be desiriable. The default duration of time is set to two minutes. Read more about idempotency [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/idempotency).

Here is an example of changing the idempotency window to 3 seconds:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var station = await memphisClient.CreateStation(
        stationOptions: new StationOptions
        {
            Name = "MyNewStation",
            IdempotenceWindowMs = 180_000
        }
    );
}
catch (Exception ex)
{
    // handle exception
}
```

The schema name is used to set a schema to be enforced by the station. The default value of "" ensures that no schema is enforced. Here is an example of changing the schema to a defined schema in schemaverse called "SensorLogs":

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var station = await memphisClient.CreateStation(
        stationOptions: new StationOptions
        {
            Name = "MyNewStation",
            SchemaName = "SensorLogs"
        }
    );
}
catch (Exception ex)
{
    // handle exception
}
```

There are two options for sending messages to the [dead-letter station(DLS)](https://docs.memphis.dev/memphis/memphis-broker/concepts/dead-letter#terminology). These are SendPoisonMessageToDls and SendSchemaFailedMessageToDls. 

Here is an example of sending poison messages to the DLS but not messages which fail to conform to the given schema.

```csharp
    try
    {
        var options = MemphisClientFactory.GetDefaultOptions();
        options.Host = "localhost";
        options.Username = "root";
        options.Password = "memphis";
        var memphisClient = await MemphisClientFactory.CreateClient(options);

        var station = await memphisClient.CreateStation(
            stationOptions: new StationOptions
            {
                Name = "MyNewStation",
                SendPoisonMessageToDls = true,
                SendSchemaFailedMessageToDls = false
            }
        );
    }
    catch (Exception ex)
    {
        // handle exception
    }
```

When either of the DLS flags are set to True, a station can also be set to handle these events. To set a station as the station to where schema failed or poison messages will be set to, use the DlsStation StationOptions:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var station = await memphisClient.CreateStation(
        stationOptions: new StationOptions
        {
            Name = "MyNewStation",
            SendPoisonMessageToDls = true,
            SendSchemaFailedMessageToDls = false,
            // DlsStation = "DeadLetterMessageStation" // Coming soon
        }
    );
}
catch (Exception ex)
{
    // handle exception
}
```

When the retention value is met, Mempihs by default will delete old messages. If tiered storage is setup, Memphis can instead move messages to tier 2 storage. Read more about tiered storage [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#storage-tiering). Enable this setting with the option provided:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var station = await memphisClient.CreateStation(
        stationOptions: new StationOptions
        {
            Name = "MyNewStation",
            TieredStorageEnabled = true
        }
    );
}
catch (Exception ex)
{
    // handle exception
}
```

[Partitioning](https://docs.memphis.dev/memphis/memphis-broker/concepts/station#partitions) might be useful for a station. To have a station partitioned, simply change the partitions number:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var station = await memphisClient.CreateStation(
        stationOptions: new StationOptions
        {
            Name = "MyNewStation",
            PartitionsNumber = 3
        }
    );
}
catch (Exception ex)
{
    // handle exception
}
```

### AttachSchema 

This method is deprecated. Use EnforceSchema instead    

### EnforceSchema 
```csharp
public async Task EnforceSchema(string stationName, string schemaName, CancellationToken cancellationToken = default)
```

To add a schema to an already created station, EnforceSchema can be used. Here is an example using EnforceSchema to add a schema to a station:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    await memphisClient.EnforceSchema(
        stationName: "MyStation",
        schemaName: "MySchema"
    );
}
catch (Exception ex)
{
    // handle exception
}
```

### DetachSchema 
```csharp
    public async Task DetachSchema(string stationName)
```

To remove a schema from an already created station, DetachSchema can be used. Here is an example of removing a schmea from a station:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    await memphisClient.DetachSchema(
        stationName: "MyStation"
    );
}
catch (Exception ex)
{
    // handle exception
} 
```

### close 

```csharp
    public void Dispose()
```

To safely and correctly close down a Memphis connection use the Dispose method. Here is an example of closing a Memphis connection.

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    memphisClient.Dispose();
}
catch (Exception ex)
{
    // handle exception
}
```

### producer 
```csharp
public async Task<MemphisProducer> CreateProducer(MemphisProducerOptions producerOptions){...}


public class MemphisProducerOptions
{
    public string StationName { get; set; }
    public string ProducerName { get; set; }

    public bool GenerateUniqueSuffix { get; set; } //GenerateUniqueSuffix will stop being supported after November 1'st, 2023.
    
    public int MaxAckTimeMs { get; set; } = 30_000;
}
```

Use the Memphis producer method to create a producer. Here is an example of creating a producer for a given station:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var producer = await memphisClient.CreateProducer(new MemphisProducerOptions
    {
        StationName = "MyStation",
        ProducerName = "MyProducer"
    });
}
catch (Exception ex)
{
    // handle exception
}
```

### consumer

```csharp
public async Task<MemphisConsumer> CreateConsumer(MemphisConsumerOptions consumerOptions){}

public sealed class MemphisConsumerOptions
{
    public string StationName { get; set; }
    public string ConsumerName { get; set; }
    public string ConsumerGroup { get; set; } = string.Empty;
    public int PullIntervalMs { get; set; } = 1_000;
    public int BatchSize { get; set; } = 10;
    public int BatchMaxTimeToWaitMs { get; set; } = 5_000;
    public int MaxAckTimeMs { get; set; } = 30_000;
    public int MaxMsgDeliveries { get; set; } = 10;

    public bool GenerateUniqueSuffix { get; set; } = false; //GenerateUniqueSuffix will stop being supported after November 1'st, 2023.

    public int StartConsumeFromSequence { get; set; } = 1;
    public int LastMessages { get; set; } = -1;

    internal string RealName { get; set; }
}
```

Use the Memphis CreateConsumer method to create a Consumer. It offeres some extra options that may be useful.

Here is an example on how to create a consumer with all of the default options:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var consumer = await memphisClient.CreateConsumer(new MemphisConsumerOptions
    {
        StationName = "MyStation",
        ConsumerName = "MyConsumer"
    });
}
catch (Exception ex)
{
    // handle exception
}handle exception
}
```

To create a consumer in a consumer group, add the ConsumerGroup MemphisConsumerOptions:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
var memphisClient = await MemphisClientFactory.CreateClient(options);

    var consumer = await memphisClient.CreateConsumer(new MemphisConsumerOptions
    {
        StationName = "MyStation",
        ConsumerName = "MyConsumer",
        ConsumerGroup = "MyConsumerGroup1"
    });
}
catch (Exception ex)
{
    // handle exception
}
```

When using Consumer.consume, the consumer will continue to consume in an infinite loop. To change the rate at which the consumer polls, change the PullIntervalMs parameter:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var consumer = await memphisClient.CreateConsumer(new MemphisConsumerOptions
    {
        StationName = "MyStation",
        ConsumerName = "MyConsumer",
        PullIntervalMs = 2_000
    });
}
catch (Exception ex)
{
    // handle exception
}
```

Every time the consumer polls, the consumer will try to take BatchSize number of elements from the station. However, sometimes there are not enough messages in the station for the consumer to consume a full batch. In this case, the consumer will continue to wait until either BatchSize messages are gathered or the time in milliseconds specified by BatchMaxTimeToWaitMs is reached. 

Here is an example of a consumer that will try to poll 100 messages every 10 seconds while waiting up to 15 seconds for all messages to reach the consumer.

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
var memphisClient = await MemphisClientFactory.CreateClient(options);

    var consumer = await memphisClient.CreateConsumer(new MemphisConsumerOptions
    {
        StationName = "MyStation",
        ConsumerName = "MyConsumer",
        PullIntervalMs = 10_000,
        BatchSize = 100,
        BatchMaxTimeToWaitMs = 15_000
    });
}
catch (Exception ex)
{
    // handle exception
}
```

The MaxMsgDeliveries parameter allows the user how many messages the consumer is able to consume before consuming more.

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var consumer = await memphisClient.CreateConsumer(new MemphisConsumerOptions
    {
        StationName = "MyStation",
        ConsumerName = "MyConsumer",
        PullIntervalMs = 10_000,
        BatchSize = 100,
        BatchMaxTimeToWaitMs = 15_000,
        MaxMsgDeliveries = 100
    });
}
catch (Exception ex)
{
    // handle exception
}
```

### produce

```csharp
public async Task ProduceAsync(
    MemphisProducerOptions options,
    byte[] message,
    NameValueCollection headers = default,
    string messageId = default,
    bool asyncProduceAck = true,
    string partitionKey = "",
    CancellationToken cancellationToken = default){...}

public class MemphisProducerOptions
{
    public string StationName { get; set; }
    public string ProducerName { get; set; }
    
    [Obsolete("GenerateUniqueSuffix will be stopped to be supported after November 1'st, 2023.")]
    public bool GenerateUniqueSuffix { get; set; }
    
    public int MaxAckTimeMs { get; set; } = 30_000;
}
```


The ProduceAsync method allows for the user to produce a message without discretely creating a producer. Because this creates a producer for every message, it is better to create a producer if many message need to be produced. 

For message data formats see [here](https://docs.memphis.dev/memphis/memphis-schemaverse/formats/produce-consume). 

Messages produced by ProduceAsync run asyncronously by default. By using the AsyncProduce Option this can be set to produce messages syncronously, waiting for an ack after each message is produced. By default, messages are sent while still waiting for the ack of previously sent messages. This reduces preceived network latency and will allow for producers to produce more messages however may incur a loss in reliability. 

Here is an example of a ProduceAsync method call that waits up to one minute for an acknowledgement from memphis and produces messages syncronously:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    await memphisClient.ProduceAsync(
        options: new MemphisProducerOptions
        {
            MaxAckTimeMs = 60_000,
            StationName = "MyStation",
            ProducerName = "MyProducer"
        },
        message: Encoding.UTF8.GetBytes("MyMessage"),
        asyncProduceAck: false
    );
}
catch (Exception ex)
{
    // handle exception
}
```

As discussed before in the station section, idempotency is an important feature of memphis. To achieve idempotency, an id must be assigned to messages that are being produced. Use the messageId parameter for this purpose.

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    await memphisClient.ProduceAsync(
        options: new MemphisProducerOptions
        {
            MaxAckTimeMs = 60_000,
            StationName = "MyStation",
            ProducerName = "MyProducer"
        },    
        message: Encoding.UTF8.GetBytes("MyMessage"),
        messageId: "UniqueMessageID"
    );
}
catch (Exception ex)
{
    // handle exception
}
```

To add message headers to the message, use the headers parameter. Headers can help with observability when using certain 3rd party to help monitor the behavior of memphis. See [here](https://docs.memphis.dev/memphis/memphis-broker/comparisons/aws-sqs-vs-memphis#observability) for more details.

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    var headers = new NameValueCollection
    {
        { "trace_header", "track_me_123" }
    };

    await memphisClient.ProduceAsync(
    options: new MemphisProducerOptions
    {
        MaxAckTimeMs = 60_000,
        StationName = "MyStation",
        ProducerName = "MyProducer"
    },
    message: Encoding.UTF8.GetBytes("MyMessage"),
    headers: headers
    );
}
catch (Exception ex)
{
    // handle exception
}
```

Lastly, memphis can produce to a specific partition in a station. To do so, use the partitionKey parameter:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    await memphisClient.ProduceAsync(
        options: new MemphisProducerOptions
        {
            MaxAckTimeMs = 60_000,
            StationName = "MyStation",
            ProducerName = "MyProducer"
        },    
        message: Encoding.UTF8.GetBytes("MyMessage")
        partitionKey: "Partition3"
    );
}
catch (Exception ex)
{
    // handle exception
}
```

### fetch_message 

```csharp
  public async Task<IEnumerable<MemphisMessage>> FetchMessages(
        FetchMessageOptions options,
        CancellationToken cancellationToken = default
    ){...}

public sealed class FetchMessageOptions
{
    public string ConsumerName { get; set; }
    public string StationName { get; set; }
    public string ConsumerGroup { get; set; }
    public int BatchSize { get; set; } = 10;
    public int BatchMaxTimeToWaitMs { get; set; } = 5_000;
    public int MaxAckTimeMs { get; set; } = 30_000;
    public int MaxMsgDeliveries { get; set; } = 10;

    public bool GenerateUniqueSuffix { get; set; } //GenerateUniqueSuffix will no longer be supported after November 1'st, 2023.
    public int StartConsumeFromSequence { get; set; } = 1;
    public int LastMessages { get; set; } = -1;
    public bool Prefetch { get; set; }

    public string PartitionKey { get; set; } = string.Empty;
}
```

Use the FetchMessages method in order to consume a batch of messages without having to create a consumer manually. Because this method creates a consumer on each call (or pulls one from a cache), it is more performative to create a consumer with the CreateConsumer Method and to use that to do many calls to Fetch.

Because of the overlap of FetchMessages and Fetch, here is just one example for fetching a batch of 5 messages, skipping the first 3 in the station:

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);


    await memphisClient.FetchMessages(
        options: new FetchMessageOptions
        {
            ConsumerName = "MyConsumer",
            StationName = "MyStationName",
            BatchSize = 5,
            StartConsumeFromSequence = 3
        }
    );
}
catch (Exception ex)
{
    // handle exception
}
```

### CreateSchema 

```csharp
    public async Task CreateSchema(string schemaName, string schemaType, string schemaFilePath, CancellationToken cancellationToken = default)

```

The CreateSchema creates a schema. To use this method, simply name the schema, list its type and then give a file path to the schema file.

```csharp
try
{
    var options = MemphisClientFactory.GetDefaultOptions();
    options.Host = "localhost";
    options.Username = "root";
    options.Password = "memphis";
    var memphisClient = await MemphisClientFactory.CreateClient(options);

    await memphisClient.CreateSchema(
        schemaName: "MyNewSchema",
        schemaType: "JSON",
        schemaFilePath: "~/schemas/my_new_json_schmea.json"
    );
}
catch (Exception ex)
{
    // handle exception
}
```