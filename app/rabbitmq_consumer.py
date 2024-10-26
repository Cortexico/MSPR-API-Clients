import os
import json
import asyncio
from aio_pika import connect_robust, ExchangeType
from app.database import SessionLocal
from app import crud, models

async def start_consumer():
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

    connection = await connect_robust(
        f"amqp://guest:guest@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
    )

    channel = await connection.channel()
    exchange = await channel.declare_exchange("orders", ExchangeType.FANOUT)
    queue = await channel.declare_queue('', exclusive=True)
    await queue.bind(exchange)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                order_data = json.loads(message.body.decode('utf-8'))
                await handle_order_created(order_data)

async def handle_order_created(order_data):
    # Logique pour traiter les messages de commandes créées
    # Par exemple, mettre à jour le statut du client
    pass  # À implémenter selon vos besoins
