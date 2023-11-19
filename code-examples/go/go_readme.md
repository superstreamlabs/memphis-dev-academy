# Go Documentation

This document will go over the available memphis functions that users may used in the Go API. 

## Useful Memphis Functions

With the Go Memphis package, you can use the Connect, CreateStation, EnforceSchema, DetachSchema, Close, Producer, Consumer, Produce, FetchMessages, and CreateSchema functions.

### Connect

```go
func Connect(host, username string, options ...Option) (*Conn, error)

type Options struct {
	Host              string
	Port              int
	Username          string
	AccountId         int
	ConnectionToken   string
	Reconnect         bool
	MaxReconnect      int
	ReconnectInterval time.Duration
	Timeout           time.Duration
	TLSOpts           TLSOpts
	Password          string
}   

func getDefaultOptions() Options {
	return Options{
		Port:              6666,
		Reconnect:         true,
		MaxReconnect:      10,
		ReconnectInterval: 1 * time.Second,
		Timeout:           2 * time.Second,
		TLSOpts: TLSOpts{
			TlsCert: "",
			TlsKey:  "",
			CaFile:  "",
		},
		ConnectionToken: "",
		Password:        "",
		AccountId:       1,
	}
}

```

The Connect function allows for the creation of a connection to Memphis. Connecting to Memphis (cloud or open-source) will be needed in order to use any of the other functionality of the Memphis class.

What arguments are used with the memphis.Connect function change depending on the type of connection being made.

The getDefaultOptions() is used interally, and is present to display what arguments are applied if no additional optional functions are passed into the Connect function.

 A standard password-based connection would look like this (using the defualt root memphis login with Memphis open-source):

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))
```

A JWT, token-based connection would look like this:

```go
conn, err := memphis.Connect("localhost", "root", memphis.ConnectionToken("memphis"))
```

Memphis needs to be configured to use token based connection. See the [docs](https://docs.memphis.dev/memphis/memphis-broker/concepts/security) for help doing this.

To use a TLS based connection, the TLS function will need to be invoked:

```go
func Tls(TlsCert string, TlsKey string, CaFile string) Option {
	return func(o *Options) error {
		o.TLSOpts = TLSOpts{
			TlsCert: TlsCert,
			TlsKey:  TlsKey,
			CaFile:  CaFile,
		}
		return nil
	}
}
```

Using this to connect to Memphis looks like this:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Tls(
    "~/tls_file_path.key",
    "~/tls_cert_file_path.crt",
    "~/tls_cert_file_path.crt",
))
```

To configure memphis to use TLS see the [docs](https://docs.memphis.dev/memphis/open-source-installation/kubernetes/production-best-practices#memphis-metadata-tls-connection-configuration). 


### station 
```go
func (c *Conn) CreateStation(Name string, opts ...StationOpt) (*Station, error)

// StationsOpts - configuration options for a station.
type StationOpts struct {
    Name                     string
    RetentionType            RetentionType
    RetentionVal             int
    StorageType              StorageType
    Replicas                 int
    IdempotencyWindow        time.Duration
    SchemaName               string
    SendPoisonMsgToDls       bool
    SendSchemaFailedMsgToDls bool
    TieredStorageEnabled     bool
    PartitionsNumber         int
    DlsStation               string
}

// GetStationDefaultOptions - returns default configuration options for the station.
// NOTE: This is not used by the user. This is just for 
// display purposes.
func GetStationDefaultOptions() StationOpts {
	return StationOpts{
		RetentionType:            MaxMessageAgeSeconds,
		RetentionVal:             604800,
		StorageType:              Disk,
		Replicas:                 1,
		IdempotencyWindow:        2 * time.Minute,
		SchemaName:               "",
		SendPoisonMsgToDls:       true,
		SendSchemaFailedMsgToDls: true,
		TieredStorageEnabled:     false,
		PartitionsNumber:         1,
		DlsStation:               "",
	}
}

// RetentionType - station's message retention type
type RetentionType int

const (
    MaxMessageAgeSeconds RetentionType = iota
    Messages
    Bytes
    AckBased
)

// StorageType - station's message storage type
type StorageType int

const (
    Disk StorageType = iota
    Memory
)

```

The CreateStation function is used to create a station. Using the different arguemnts, one can programically create many different types of stations. The Memphis UI can also be used to create stations to the same effect. 

A minimal example, using all default values would simply create a station with the given name:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

station, err := conn.CreateStation("myStation")
```

To change what criteria the station uses to decide if a message should be retained in the station, change the retention type. The different types of retention are documented [here](https://github.com/memphisdev/memphis.go#retention-types) in the go README. 

The unit of the rentention value will vary depending on the RetentionType. The [previous link](https://github.com/memphisdev/memphis.go#retention-types) also describes what units will be used. 

Here is an example of a station which will only hold up to 10 messages:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

station, err := conn.CreateStation(
    "myStation",
    memphis.RetentionTypeOpt(memphis.Messages),
    memphis.RetentionVal(10)
    )
```

Memphis stations can either store Messages on disk or in memory. A comparison of those types of storage can be found [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#tier-1-local-storage).

Here is an example of how to create a station that uses Memory as its storage type:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

station, err := conn.CreateStation(
    "myStation",
    memphis.StorageTypeOpt(memphis.Memory)
    )
```

In order to make a station more redundant, replicas can be used. Read more about replicas [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#replicas-mirroring). Note that replicas are only available in cluster mode. Cluster mode can be enabled in the [Helm settings](https://docs.memphis.dev/memphis/open-source-installation/kubernetes/1-installation#appendix-b-helm-deployment-options) when deploying Memphis with Kubernetes.

Here is an example of creating a station with 3 replicas:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

station, err := conn.CreateStation(
    "myStation",
    memphis.Replicas(3)
    )
```

Idempotency defines how Memphis will prevent duplicate messages from being stored or consumed. The duration of time the message ID's will be stored in the station can be set with the IdempotencyWindow StationOpt. If the environment Memphis is deployed in has unreliably connection and/or a lot of latency, increasing this value might be desiriable. The default duration of time is set to two minutes. Read more about idempotency [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/idempotency).

Here is an example of changing the idempotency window to 3 seconds:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

station, err := conn.CreateStation(
    "myStation",
    memphis.IdempotencyWindow(3 * time.Minute)
    )
```

The SchemaName is used to set a schema to be enforced by the station. The default value ensures that no schema is enforced. Here is an example of changing the schema to a defined schema in schemaverse called "sensorLogs":

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

station, err := conn.CreateStation(
    "myStation",
    memphis.SchemaName("sensorLogs")
    )
```

There are two parameters for sending messages to the [dead-letter station(DLS)](https://docs.memphis.dev/memphis/memphis-broker/concepts/dead-letter#terminology). Use the functions SendPoisonMsgToDls and SendSchemaFailedMsgToDls to se these parameters. 

Here is an example of sending poison messages to the DLS but not messages which fail to conform to the given schema.

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

station, err := conn.CreateStation(
    "myStation",
    memphis.SchemaName("SensorLogs"),
    memphis.SendPoisonMsgToDls(true),
    memphis.SendSchemaFailedMsgToDls(false)
    )
```

When either of the DLS flags are set to True, a station can also be set to handle these events. To set a station as the station to where schema failed or poison messages will be set to, use the DlsStation StationOpt:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

station, err := conn.CreateStation(
    "myStation",
    memphis.SchemaName("SensorLogs"),
    memphis.SendPoisonMsgToDls(true),
    memphis.SendSchemaFailedMsgToDls(false),
    memphis.DlsStation("badSensorMessagesStation")
    )
```

When the retention value is met, Mempihs by default will delete old messages. If tiered storage is setup, Memphis can instead move messages to tier 2 storage. Read more about tiered storage [here](https://docs.memphis.dev/memphis/memphis-broker/concepts/storage-and-redundancy#storage-tiering). Enable this setting with the respective StationOpt:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

station, err := conn.CreateStation(
    "myStation",
    memphis.TieredStorageEnabled(true)
    )
```

[Partitioning](https://docs.memphis.dev/memphis/memphis-broker/concepts/station#partitions) might be useful for a station. To have a station partitioned, simply set the PartitionNumber StationOpt:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

station, err := conn.CreateStation(
    "myStation",
    memphis.PartitionsNumber(3)
    )
```

### AttachSchema 

This function is deprecated. Use EnforceSchema instead    

### EnforceSchema 
```go
func (c *Conn) EnforceSchema(name string, stationName string) error
```

To add a schema to an already created station, EnforceSchema can be used. Here is an example using EnforceSchema to add a schema to a station:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

err := conn.EnforceSchema(
    "SchemaName",
    "MyStation",
)

// Handle enforce schema err
```

### DetachSchema 
```go
func (c *Conn) DetachSchema(stationName string) error
```

To remove a schema from an already created station, DetachSchema can be used. Here is an example of removing a schmea from a station:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

err := conn.DetachSchema(
    "SchemaName",
)

// Handle enforce schema err
```

### close 

```go
func (c *Conn) Close()
```

To safely and correctly close down a Memphis connection use the close function. Here is an example of closing a Memphis connection.

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

conn.Close()

// You can defer this after handling the connection error, if desired
```

### producer 
```go
func (c *Conn) CreateProducer(stationName, name string, opts ...ProducerOpt) (*Producer, error)

// ProducerOpts - configuration options for producer creation.
type ProducerOpts struct {
	GenUniqueSuffix bool
}
```

Use the Memphis producer function to create a producer. Here is an example of creating a producer for a given station:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

producer, err := conn.CreateProducer(
    "StationToProduceFor",
    "MyNewProducer",
)

// Handle err
```

### consumer

```go
func (c *Conn) CreateConsumer(stationName, consumerName string, opts ...ConsumerOpt) (*Consumer, error) 

// ConsumerOpts - configuration options for a consumer.
type ConsumerOpts struct {
	Name                     string
	StationName              string
	ConsumerGroup            string
	PullInterval             time.Duration
	BatchSize                int
	BatchMaxWaitTime       time.Duration
	MaxAckTime               time.Duration
	MaxMsgDeliveries         int
	GenUniqueSuffix          bool
	ErrHandler               ConsumerErrHandler
	StartConsumeFromSequence uint64
	LastMessages             int64
}

// Default options applied by the Go SDK automatically
func getDefaultConsumerOptions() ConsumerOpts {
	return ConsumerOpts{
		PullInterval:             1 * time.Second,
		BatchSize:                10,
		BatchMaxWaitTime:       5 * time.Second,
		MaxAckTime:               30 * time.Second,
		MaxMsgDeliveries:         10,
		GenUniqueSuffix:          false,
		ErrHandler:               DefaultConsumerErrHandler, // Printf with log package
		StartConsumeFromSequence: 1,
		LastMessages:             -1,
	}
}

```

Use the connection.CreateConsumer function to create a Consumer. It offeres some extra options that may be useful.

A consumer can be created with the station CreateConsumer function as well. The station function for CreateConsumer is a direct wrapper around the connection function. The connection function will be used for all examples.

Here is an example on how to create a consumer with all of the default options:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

consumer, err := conn.CreateConsumer(
    "MyStation",
    "MyNewConsumer",
)

// Handle err
```

To create a consumer in a consumer group, add the ConsumerGroup parameter:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

consumer, err := conn.CreateConsumer(
    "MyStation",
    "MyNewConsumer",
    memphis.ConsumerGroup("ConsumerGroup1"),
)

// Handle err
```

When using the Consume function from a consumer, the consumer will continue to consume in an infinite loop. To change the rate at which the consumer polls, change the PullInterval consumer option:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

consumer, err := conn.CreateConsumer(
    "MyStation",
    "MyNewConsumer",
    memphis.PullInterval(2 * time.Second),
)

// Handle err
```

Every time the consumer polls, the consumer will try to take BatchSize number of elements from the station. However, sometimes there are not enough messages in the station for the consumer to consume a full batch. In this case, the consumer will continue to wait until either BatchSize messages are gathered or the time in milliseconds specified by BatchMaxWaitTime is reached. 

Here is an example of a consumer that will try to poll 100 messages every 10 seconds while waiting up to 15 seconds for all messages to reach the consumer.

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

consumer, err := conn.CreateConsumer(
    "MyStation",
    "MyNewConsumer",
    memphis.PullInterval(10 * time.Second),
    memphis.BatchSize(100),
    memphis.BatchMaxWaitTime(15 * time.Second).
)

// Handle err
```

The MaxMsgDeliveries ConsumerOpt allows the user to set how many messages the consumer is able to consume (without acknowledging) before consuming more. 

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

consumer, err := conn.CreateConsumer(
    "MyStation",
    "MyNewConsumer",
    memphis.PullInterval(10 * time.Second),
    memphis.BatchSize(100),
    memphis.BatchMaxWaitTime(15 * time.Second),
    memphis.MaxMsgDeliveries(100),
)

// Handle err
```

### produce

```go
func (c *Conn) Produce(stationName, name string, message any, opts []ProducerOpt, pOpts []ProduceOpt) error

// ProduceOpts - configuration options for produce operations.
type ProduceOpts struct {
	Message              any
	AckWaitSec           int // Default is 15
	MsgHeaders           Headers // Default is empty map[string][]string
	AsyncProduce         bool // Default is true
	ProducerPartitionKey string // Default is ""
}

// ProduceOpt - a function on the options for produce operations.
type ProduceOpt func(*ProduceOpts) error
```

The Produce function allows for the user to produce a message without discretely creating a producer. Because this creates a consumer or pulls it from a cache, it is better to create a producer if many message need to be produced quickly. 

Here is a minimal example of producing from a connection:

```go
c.Produce("MyStation", "MyProducer", []byte("My Message :)"), []memphis.ProducerOpt{}, []memphis.ProduceOpt{})
```

For the rest of the examples, the Produce method from a Producer will be used:

```go
func (p *Producer) Produce(message any, opts ...ProduceOpt) error
```

For message data formats see [here](https://docs.memphis.dev/memphis/memphis-schemaverse/formats/produce-consume). 

Here is an example of a produce function call that waits up to 30 seconds for an acknowledgement from memphis:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

producer, err := conn.CreateProducer(
    "StationToProduceFor",
    "MyNewProducer",
)

// Handle err

err = producer.Produce(
    []byte("My Message :)"),
    memphis.AckWaitSec(30),
)

// Handle err
```

As discussed before in the station section, idempotency is an important feature of memphis. To achieve idempotency, an id must be assigned to messages that are being produced. Use the MsgId ProducerOpt for this purpose.

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

producer, err := conn.CreateProducer(
    "StationToProduceFor",
    "MyNewProducer",
    // MsgID not supported yet...
)

// Handle err

err = producer.Produce(
    []byte("My Message :)"),
)

// Handle err
```

To add message headers to the message, use the headers parameter. Headers can help with observability when using certain 3rd party to help monitor the behavior of memphis. See [here](https://docs.memphis.dev/memphis/memphis-broker/comparisons/aws-sqs-vs-memphis#observability) for more details.

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

producer, err := conn.CreateProducer(
    "StationToProduceFor",
    "MyNewProducer",
)

// Handle err

hdrs := memphis.Headers{}
hdrs.New()
err := hdrs.Add("key", "value")

// Handle err

err = producer.Produce(
    []byte("My Message :)"),
    memphis.MsgHeaders(hdrs),
)

// Handle err
```

Lastly, memphis can produce to a specific partition in a station. To do so, use the ProducerPartitionKey ProducerOpt:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err

producer, err := conn.CreateProducer(
    "StationToProduceFor",
    "MyNewProducer",
)

// Handle err

err = producer.Produce(
    []byte("My Message :)"),
    memphis.ProducerPartitionKey("2ndPartition"),
)

// Handle err
```

### FetchMessages 

```go
func (c *Conn) FetchMessages(stationName string, consumerName string, opts ...FetchOpt) ([]*Msg, error)

// FetchOpts - configuration options for fetch.
type FetchOpts struct {
	ConsumerName             string
	StationName              string
	ConsumerGroup            string
	BatchSize                int
	BatchMaxWaitTime       time.Duration
	MaxAckTime               time.Duration
	MaxMsgDeliveries         int
	GenUniqueSuffix          bool
	ErrHandler               ConsumerErrHandler
	StartConsumeFromSequence uint64
	LastMessages             int64
	Prefetch                 bool
	FetchPartitionKey        string
}
```

Use the FetchMessages function in order to consume a batch of messages without having to create a consumer manually. Because this function creates a consumer or pulls a consumer from a cache on each call, it is more performative to create a consumer with the memphis.CreateConsumer function and to use that to do many calls to fetch.

Because of the overlap of this method and consumer.Fetch and consumer.Consume, here is one example for fetching a batch of 5 messages, skipping the first 3 in the station:

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err 

msgs, err := conn.FetchMessages(
    "MyStation",
    "MyConsumer",
    memphis.BatchSize(5),
    // memphis.StartConsumeFromSequence(3), Not valid yet :(
)

// Handle err
```

### CreateSchema 

```go
func (c *Conn) CreateSchema(name, schemaType, path string) error
```

The CreateSchema function creates a schema. To use this function, simply name the schema, list its type and then give a file path to the schema file.

```go
conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

// Handle err 

conn.CreateSchema(
    "SchemaName",
    "SchemaType",
    "~/PathToSchema.json",
)
```