import { memphis, Memphis } from 'memphis-dev';

(async function () {
    let memphisConnection: Memphis | null = null;

    try {
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });

        const producer = await memphisConnection.producer({
            stationName: 'test_station',
            producerName: 'test_producer'
        });

            await producer.produce({
                message: Buffer.from("Hello world"), // you can also send a JS object - {}
            });

        memphisConnection.close();
    } catch (ex) {
        console.log(ex);
        if (memphisConnection) memphisConnection.close();
    }
})(); 

// These are examples of the async functiontions available by the Memphis API

// Connecting Examples

async function ConnectPassword() {

}

async function ConnectToken() {

}

async function ConnectTLS() {

}

// Station Examples

async function StationDefault() {

}

async function StationRetentionType() {

}

async function StationMemoryStorage() {

}

async function StationWithReplicas() {

}

async function StationIdempotency() {

}

async function StationWithSchema() {

}

async function StationPoisonDls() {

}

async function StationWithPoisonDlsToStation() {

}

async function StationWithTieredStorage() {

}

async function StationWithPartitions() {

}

// Attach Schema Examples

// This async functiontion is deprecated. Use enforce_schema instead

// Enforce Schema Examples

async function EnforceSchema() {

}

// Detach Schema Examples

async function DeatchSchema() {

}

// Close Examples

async function Close() {

}

// Produce Examples

async function ProduceBasic() {

}

async function ProduceWithMessageID() {

}

async function ProduceWithHeaders() {

}

async function ProduceWithPartition() {

}

// Consume Examples

// Fetch Messages Examples

async function FetchMessages() {

}

// Create Schema Examples

async function CreateSchema() {

}
