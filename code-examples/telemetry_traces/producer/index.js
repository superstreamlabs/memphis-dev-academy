const fastify = require("fastify")({ logger: false });
const { sendEvent } = require("./producer.js");

fastify.post("/add-trace", async (request, reply) => {
  const requestBody = request.body;
  await sendEvent(requestBody);
  reply.send({ success: true });
});

const start = async () => {
  try {
    await fastify.listen({ port: 3000 });
    console.log("Server is running on port 3000");
  } catch (err) {
    console.error("Error starting server:", err);
    process.exit(1);
  }
};

start();
