const { memphis } = require("memphis-dev");
let producer;
(async () => {
  let memphisConnection;

  try {
    memphisConnection = await memphis.connect({
      host: "<host>",
      username: "<client-type-user>",
      password: "<client-type-password>",
      accountId: "<account-id>",
    });

    producer = await memphisConnection.producer({
      stationName: "traces",
      producerName: "traces_producer",
    });
  } catch (ex) {
    console.log(ex);
    if (memphisConnection) memphisConnection.close();
  }
})();

const sendEvent = async (trace) => {
  const headers = memphis.headers();
  headers.add("<header>", "<value>"); // add your own headers here
  await producer.produce({
    message: {
      event: trace.event,
      timestamp: Date.now(),
      ip: trace.ip,
    },
    headers: headers,
    asyncProduce: true,
  });
};

exports.sendEvent = sendEvent;
