import os
import json
import aio_pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

async def send_message_to_rabbitmq(message):
    connection = await aio_pika.connect_robust(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        login=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD
    )

    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange('customer_exchange', aio_pika.ExchangeType.FANOUT)
        message_body = json.dumps(message)
        await exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key=""
        )