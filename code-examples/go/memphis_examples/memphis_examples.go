package main

import (
	"fmt"
	"os"
	"time"

	"github.com/memphisdev/memphis.go"
)

// These are examples of the functions available by the Memphis API

func main() {
	// Put methods here to run them...
}

// Connecting Examples

func ConnectPassword() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	fmt.Printf(conn.ConnId)
}

func ConnectToken() {
	conn, err := memphis.Connect("localhost", "root", memphis.ConnectionToken("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	fmt.Printf(conn.ConnId)
}

func ConnectTLS() {
	conn, err := memphis.Connect("localhost", "root", memphis.Tls(
		"~/tls_file_path.key",
		"~/tls_cert_file_path.crt",
		"~/tls_cert_file_path.crt",
	))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	fmt.Printf(conn.ConnId)
}

// Station Examples

func StationDefault() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	station, err := conn.CreateStation("myStation")

	fmt.Printf(station.Name) // To quiet the go compiler...
}

func StationRetentionType() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	station, err := conn.CreateStation(
		"myStation",
		memphis.RetentionTypeOpt(memphis.Messages),
		memphis.RetentionVal(10),
	)

	fmt.Printf(station.Name) // To quiet the go compiler...
}

func StationMemoryStorage() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	station, err := conn.CreateStation(
		"myStation",
		memphis.StorageTypeOpt(memphis.Memory),
	)

	fmt.Printf(station.Name) // To quiet the go compiler...
}

func StationWithReplicas() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	station, err := conn.CreateStation(
		"myStation",
		memphis.Replicas(3),
	)

	fmt.Printf(station.Name) // To quiet the go compiler...
}

func StationIdempotency() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	station, err := conn.CreateStation(
		"myStation",
		memphis.IdempotencyWindow(3*time.Minute),
	)

	fmt.Printf(station.Name) // To quiet the go compiler...
}

func StationWithSchema() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	station, err := conn.CreateStation(
		"myStation",
		memphis.SchemaName("sensorLogs"),
	)

	fmt.Printf(station.Name) // To quiet the go compiler...
}

func StationPoisonDls() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	station, err := conn.CreateStation(
		"myStation",
		memphis.SchemaName("SensorLogs"),
		memphis.SendPoisonMsgToDls(true),
		memphis.SendSchemaFailedMsgToDls(false),
	)

	fmt.Printf(station.Name) // To quiet the go compiler...
}

func StationWithPoisonDlsToStation() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	station, err := conn.CreateStation(
		"myStation",
		memphis.SchemaName("SensorLogs"),
		memphis.SendPoisonMsgToDls(true),
		memphis.SendSchemaFailedMsgToDls(false),
		// memphis.DlsStation("badSensorMessagesStation"), When this gets released it'll work...
	)

	fmt.Printf(station.Name) // To quiet the go compiler...
}

func StationWithTieredStorage() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	station, err := conn.CreateStation(
		"myStation",
		memphis.TieredStorageEnabled(true),
	)

	fmt.Printf(station.Name) // To quiet the go compiler...
}

func StationWithPartitions() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	station, err := conn.CreateStation(
		"myStation",
		memphis.PartitionsNumber(3),
	)

	fmt.Printf(station.Name) // To quiet the go compiler...
}

// Attach Schema Examples

// This function is deprecated. Use enforce_schema instead

// Enforce Schema Examples

func EnforceSchema() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	err = conn.EnforceSchema(
		"SchemaName",
		"MyStation",
	)

	// Handle enforce schema err
}

// Detach Schema Examples

func DeatchSchema() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	err = conn.DetachSchema(
		"SchemaName",
	)

	// Handle enforce schema err
}

// Close Examples

func Close() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	conn.Close()

	// You can defer this after handling the connection error, if desired
}

// Produce Examples

func ProduceBasic() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	producer, err := conn.CreateProducer(
		"StationToProduceFor",
		"MyNewProducer",
	)

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	fmt.Printf(producer.Name) // To quiet the go compiler...
}

func ProduceWithHeaders() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	producer, err := conn.CreateProducer(
		"StationToProduceFor",
		"MyNewProducer",
	)

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	hdrs := memphis.Headers{}
	hdrs.New()
	err = hdrs.Add("key", "value")

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	err = producer.Produce(
		[]byte("My Message :)"),
		memphis.MsgHeaders(hdrs),
	)

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}
}

func ProduceWithPartition() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	producer, err := conn.CreateProducer(
		"StationToProduceFor",
		"MyNewProducer",
	)

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	err = producer.Produce(
		[]byte("My Message :)"),
		memphis.ProducerPartitionKey("2ndPartition"),
	)

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}
}

// Consume Examples

func ConsumerDefault() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	consumer, err := conn.CreateConsumer(
		"MyStation",
		"MyNewConsumer",
	)

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	fmt.Printf(consumer.Name) // To quiet the go compiler...
}

func ConsumerWithGroup() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	consumer, err := conn.CreateConsumer(
		"MyStation",
		"MyNewConsumer",
		memphis.ConsumerGroup("ConsumerGroup1"),
	)

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	fmt.Printf(consumer.Name) // To quiet the go compiler...
}

func ConsumerPullInterval() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	consumer, err := conn.CreateConsumer(
		"MyStation",
		"MyNewConsumer",
		memphis.PullInterval(2*time.Second),
	)

	fmt.Printf(consumer.Name) // To quiet the go compiler...
}

func ConsumerBatchMaxTimeToWait() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	consumer, err := conn.CreateConsumer(
		"MyStation",
		"MyNewConsumer",
		memphis.PullInterval(10*time.Second),
		memphis.BatchSize(100),
		memphis.BatchMaxWaitTime(15*time.Second),
	)

	fmt.Printf(consumer.Name) // To quiet the go compiler...
}

func ConsumerMaxMsgDeliveries() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	consumer, err := conn.CreateConsumer(
		"MyStation",
		"MyNewConsumer",
		memphis.PullInterval(10*time.Second),
		memphis.BatchSize(100),
		memphis.BatchMaxWaitTime(15*time.Second),
		memphis.MaxMsgDeliveries(100),
	)

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	fmt.Printf(consumer.Name) // To quiet the go compiler...
}

// Fetch Messages Examples

func FetchMessages() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	msgs, err := conn.FetchMessages(
		"MyStation",
		"MyConsumer",
		memphis.FetchBatchSize(5),
		// memphis.FetchStartCStartConsumeFromSequence(3), Why this not existing?
	)

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	fmt.Printf(string(msgs[0].Data())) // To quiet the go compiler...
}

// Create Schema Examples

func CreateSchema() {
	conn, err := memphis.Connect("localhost", "root", memphis.Password("memphis"))

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	conn.CreateSchema(
		"SchemaName",
		"SchemaType",
		"~/PathToSchema.json",
	)

	if err != nil {
		fmt.Printf("An error has occured :( : %v", err)
		os.Exit(1)
	}

	fmt.Printf(conn.ConnId) // To quiet the go compiler...
}
