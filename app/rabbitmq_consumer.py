import os
import json
import threading
import pika
from app.database import SessionLocal
from app import models


def process_message(ch, method, properties, body):
    data = json.loads(body)
    session = SessionLocal()
    try:
        customer = models.Customer(**data)
        session.add(customer)
        session.commit()
        session.refresh(customer)
        print(f"Customer {customer.id} added.")
    except Exception as e:
        session.rollback()
        print(f"Error processing message: {e}")
    finally:
        session.close()
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    def run():
        RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
        RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
        RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
        RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange='orders', exchange_type='fanout')
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='orders', queue=queue_name)

        channel.basic_consume(
            queue=queue_name, on_message_callback=process_message
        )
        print('RabbitMQ consumer started. Waiting for messages.')
        channel.start_consuming()

    threading.Thread(target=run, daemon=True).start()
