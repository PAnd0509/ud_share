import asyncio
import json
from aiokafka import AIOKafkaProducer
from app.config.settings import KAFKA_BOOTSTRAP_SERVERS

async def send_kafka_message(topic: str, message: dict):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda m: json.dumps(m).encode("utf-8")
    )
    await producer.start()
    try:
        await producer.send_and_wait(topic, message)
        print(f"Mensaje enviado a Kafka: {message}")
    finally:
        await producer.stop()
