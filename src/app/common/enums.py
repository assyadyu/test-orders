from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class UserRoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
