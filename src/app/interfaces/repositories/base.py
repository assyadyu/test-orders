from abc import abstractmethod, ABC
from typing import Any, TypeVar, Union

from uuid import UUID

MODEL = TypeVar("MODEL")
KEY = TypeVar("KEY")


class IBaseRepository(ABC):
    """
    Abstract base class for repositories with methods that are required for all repositories
    """

    @abstractmethod
    async def create(self, obj: MODEL, **kwargs) -> Union[MODEL, None]:
        """
        Create object in repository
        :param obj: data of corresponding Model to create
        :param kwargs: additional arguments if Model logic involves handling it
        :return: created object of Model or None if something went wrong
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, object_id: UUID) -> MODEL:
        """
        Get object by id
        :param object_id: object id to get from repository
        :return: object of corresponding Model
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, object_id: UUID, **values: Any) -> MODEL:
        """
        Update object by id with values provided as keyword arguments
        :param object_id: id of object to update
        :param values: keyword arguments to update
        :return: updated object of corresponding Model
        """
        raise NotImplementedError
