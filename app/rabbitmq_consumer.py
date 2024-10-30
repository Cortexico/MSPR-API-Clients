import os
import json
import asyncio
from aio_pika import connect_robust, ExchangeType
from app.database import SessionLocal
from app import crud, models

async def start_consumer():
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

    max_retries = 5
    retry_delay = 5  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            connection = await aio_pika.connect_robust(
                f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
            )
            break  # Exit the loop if connection is successful
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            await asyncio.sleep(retry_delay)
    else:
        print("All retry attempts failed. Exiting.")
        return  # Or raise an exception

    channel = await connection.channel()
    exchange = await channel.declare_exchange("orders", ExchangeType.FANOUT)
    queue = await channel.declare_queue('', exclusive=True)
    await queue.bind(exchange)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                order_data = json.loads(message.body.decode('utf-8'))
                await handle_order_created(order_data)
