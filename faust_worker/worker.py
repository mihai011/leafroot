import sys

import faust

sys.path.append("/leafroot")

from config import config

app = faust.App(
    "hello-world",
    broker=f"kafka://{config.kafka_host}:9092",
)

greetings_topic = app.topic("greetings", value_type=str)


@app.agent(greetings_topic)
async def print_greetings(greetings):
    async for greeting in greetings:
        print(greeting)


@app.timer(5)
async def produce():
    for i in range(1000):
        await greetings_topic.send(value=f"hello {i}")


if __name__ == "__main__":
    app.main()
