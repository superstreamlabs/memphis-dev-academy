using Memphis.Client;
using Memphis.Client.Consumer;
using Memphis.Client.Producer;
using Memphis.Client.Station;
using System.Collections.Specialized;
using System.Text;

// Connecting Examples
async static void ConnectPassword()
{
    try
    {
        var options = MemphisClientFactory.GetDefaultOptions();
        options.Host = "localhost";
        options.Username = "root";
        options.Password = "memphis";
        var memphisClient = await MemphisClientFactory.CreateClient(options);
    }
    catch (Exception ex)
    {
        // handle exception
    }
}

async static void ConnectToken()
{
    try
    {
        var options = MemphisClientFactory.GetDefaultOptions();
        options.Host = "localhost";
        options.Username = "root";
        options.ConnectionToken = "Token";
        var memphisClient = await MemphisClientFactory.CreateClient(options);
    }
    catch (Exception ex)
    {
        // handle exception
    }
}

async static void ConnectTLS()
{
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
}

// Station Examples

async static void StationDefault()
{
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
}

async static void StationRetentionType()
{
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
}

async static void StationMemoryStorage()
{
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
}

async static void StationWithReplicas()
{
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
}

async static void StationIdempotency()
{
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
}

async static void StationWithSchema()
{
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
}

async static void StationWithDeadLetter()
{
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
}

async static void StationWithDeadLetterToStation()
{
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
}

async static void StationWithTieredStorage()
{
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
}

async static void StationWithPartitions()
{
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
}

// Attach Schema Examples

// This static void is deprecated. Use enforceSchema instead

// Enforce Schema Examples

async static void EnforceSchema()
{
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
}

// Detach Schema Examples

async static void DetachSchema()
{
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
}

// Close Examples

async static void Dispose()
{
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
}

// Produce Examples

async static void ProducerBasic()
{
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
}

async static void ProduceFromConnection()
{
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
                ProducerName = "MyProducer",
            },
            message: Encoding.UTF8.GetBytes("MyMessage"),
            asyncProduceAck: false
        ); ;
    }
    catch (Exception ex)
    {
        // handle exception
    }
}

async static void ProduceWithIdempotency()
{
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
}

async static void ProduceWithHeaders()
{
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
}

async static void ProduceWithPartition()
{
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
            // partitionKey: "Partition3" coming soon
        );
    }
    catch (Exception ex)
    {
        // handle exception
    }
}

// Consume Examples

async static void ConsumerDefualt()
{
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
    }
}

async static void ConsumerGroup()
{
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
}

async static void ConsumerPollInterval()
{
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
}

async static void ConsumerBatched()
{
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
}

async static void ConsumerMaxMessages()
{
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
}

// Fetch Messages Examples

async static void FetchMessages()
{
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
}

// Create Schema Examples

async static void CreateSchema()
{
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
}