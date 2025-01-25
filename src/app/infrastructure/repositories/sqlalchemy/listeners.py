import asyncio
import json

from sqlalchemy import event, inspect

from app.common import logger
from app.common.rabbitmq import publish_message
from app.events.schemas import StatusChanged
from app.infrastructure.db.models import OrderModel


@event.listens_for(OrderModel, 'before_update')
def compare_old_and_new_values(mapper, connection, target):
    logger.info("compare_old_and_new_values")
    tracked_fields = ["status"]

    state = inspect(target)
    changes = {}
    for attr in state.attrs:
        hist = state.get_history(attr.key, True)

        if not hist.has_changes():
            continue
        elif attr.key in tracked_fields:
            old_value = hist.deleted[0] if hist.deleted else None
            new_value = hist.added[0] if hist.added else None
            changes[attr.key] = [old_value, new_value]
    if changes:
        new_event = StatusChanged(
            order_id=str(target.uuid),
            old_status=changes["status"][0],
            new_status=changes["status"][1],
        )
        logger.info("new event: ", new_event.__dict__)
        loop = asyncio.get_running_loop()
        loop.create_task(publish_message(json.dumps(new_event.__dict__)))
