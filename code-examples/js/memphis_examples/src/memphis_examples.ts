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

// Station Examples

async function stationDefault(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.station({
            name: "myStation"
        });
    }catch(exception){
        // Handle exception
    }
}

async function stationRetentionType(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.station({
            name: "myStation",
            retentionType: memphis.retentionTypes.MESSAGES
        });
    }catch(exception){
        // Handle exception
    }
}

async function stationMemoryStorage(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.station({
            name: "myStation",
            storageType: memphis.storageTypes.MEMORY
        });
    }catch(exception){
        // Handle exception
    }
}

async function stationWithReplicas(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.station({
            name: "myStation",
            replicas: 3
        });
    }catch(exception){
        // Handle exception
    }
}

async function stationIdempotency(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.station({
            name: "myStation",
            idempotencyWindowMs: 180000
        });
    }catch(exception){
        // Handle exception
    }
}

async function stationWithSchema(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.station({
            name: "myStation",
            schemaName: "sensorLogs"
        });
    }catch(exception){
        // Handle exception
    }
}

async function stationWithDeadLetter(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.station({
            name: "myStation",
            sendPoisonMsgToDls: true,
            sendSchemaFailedMsgToDls: false
        });
    }catch(exception){
        // Handle exception
    }
}

async function stationWithDeadLetterToStation(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.station({
            name: "myStation",
            sendPoisonMsgToDls: true,
            sendSchemaFailedMsgToDls: false,
            // dlsStation: "badSensorLogsStation" Coming soon
        });
    }catch(exception){
        // Handle exception
    }
}

async function stationWithTieredStorage(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.station({
            name: "myStation",
            tieredStorageEnabled: true
        });
    }catch(exception){
        // Handle exception
    }
}

async function stationWithPartitions(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.station({
            name: "myStation",
            partitionsNumber: 3
        });
    }catch(exception){
        // Handle exception
    }
}

// Attach Schema Examples

// This function is deprecated. Use enforceSchema instead

// Enforce Schema Examples

async function enforceSchema(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphis.enforceSchema({
            name: "mySchema",
            stationName: "myStation"
        });
    }catch(exception){
        // Handle exception
    }
}

// Detach Schema Examples

async function detachSchema(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.detachSchema({
            stationName: "myStation",
        });
    }catch(exception){
        // Handle exception
    }
}

// Close Examples

async function close(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.close();
    }catch(exception){
        // Handle exception
    }
}

// Produce Examples

async function producerBasic(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.producer({
            stationName: "myStation",
            producerName: "myNewProducer"
        });
    }catch(exception){
        // Handle exception
    }
}

async function produceFromConnection(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.produce({
            stationName: "myStation",
            producerName: "tempProducer",
            message: {some: "message"}
        });
    }catch(exception){
        // Handle exception
    }
}

async function produceAsync(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
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

async function produceWithIdempotency(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
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

async function produceWithHeaders(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });

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

async function produceWithPartition(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
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

// Consume Examples

async function consumerDefualt(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.consumer({
            stationName: "myStation",
            consumerName: "newConsumer"
        });
    }catch(exception){
        // Handle exception
    }
}

async function consumerGroup(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.consumer({
            stationName: "myStation",
            consumerName: "newConsumer",
            consumerGroup: "consumerGroup1"
        });
    }catch(exception){
        // Handle exception
    }
}

async function consumerPollInterval(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.consumer({
            stationName: "myStation",
            consumerName: "newConsumer",
            pullIntervalMs: 2000
        });
    }catch(exception){
        // Handle exception
    }
}

async function consumerBatched(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
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

async function consumerMaxMessages(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
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

// Fetch Messages Examples

async function fetchMessages(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
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

// Create Schema Examples

async function createSchema(){
    let memphisConnection;
    try{
        memphisConnection = await memphis.connect({
            host: 'localhost',
            username: 'root',
            password: 'memphis',
        });
        await memphisConnection.createSchema({
            schemaName: "newSchema",
            schemaType: "json",
            schemaFilePath: "~/schemas/my_schema_path.json"
        });
    }catch(exception){
        // Handle exception
    }
}