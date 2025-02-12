from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Dict, Any

T = TypeVar('T')


class DatabaseService(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T, data: Dict) -> bool:
        pass

    @abstractmethod
    def get_all(self, entity: T) -> List[T] | None:
        pass

    @abstractmethod
    def get_by(self, entity: T, filters) -> List[T] | None:
        pass

    @abstractmethod
    def get_one_by(self, entity: T, filters) -> T | None:
        pass

    @abstractmethod
    def update(self, entity: T, entity_id: int, updates: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete(self, entity: T, entity_id: int) -> bool:
        pass

    @abstractmethod
    def join(self, entities: List[T], filters) -> List[T]:
        pass
