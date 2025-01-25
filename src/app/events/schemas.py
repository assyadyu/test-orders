from dataclasses import dataclass

from app.common.enums import OrderStatus


class Event:
    pass


@dataclass
class StatusChanged(Event):
    order_id: str
    old_status: OrderStatus
    new_status: OrderStatus