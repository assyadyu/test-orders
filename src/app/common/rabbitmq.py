import aio_pika
from aio_pika import logger

from app.common import settings, logger


async def rabbit_connection() -> aio_pika.abc.AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbitmq_url)


async def publish_message(message: str) -> None:
    logger.info(f"Publishing message: {message}")
    async with await rabbit_connection() as conn:
        channel = await conn.channel()
        exchange = await channel.declare_exchange('direct', auto_delete=True)
        queue = await channel.declare_queue(settings.RABBITMQ_QUEUE, auto_delete=False)
        await queue.bind(exchange, settings.RABBITMQ_ROUTE)
        await exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=settings.RABBITMQ_ROUTE
        )
