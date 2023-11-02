import asyncio
import nats
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError

async def main():
    connection_options = {
        "servers": "localhost:6666",
        "allow_reconnect": True,
        "max_reconnect_attempts": 10,
        "reconnect_time_wait": 3,
        "connect_timeout": 15,
        "user":"root", # Optional in NATS. Mandatory in Memphis.
        "password":"memphis" # Optional in NATS. Mandatory in Memphis.
    }

    """
    Connect to the memphis broker through nats.
    Note that localhost:6666 is the servers target here.
    """ 
    nc = await nats.connect(**connection_options)

    # Create JetStream context.
    js = nc.jetstream()

    """
    Create the add_stream will create a station if it doesn't exist
    The station will be the name, but to produce to the station
    with publish, then you must use the subject defined here
    """
    await js.add_stream(name="sample-stream", subjects=["test"])
    await js.publish("test", f"hello world".encode())

    """
    If a station already was creatd through the memphis UI,
    then the subject must be in the format of <station>$<partition>.final
    Here is an example of producing to the first partition of a station called
    nats-test. 
    """
    await js.publish("nats-test$1.final", f"hello world".encode())

    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())