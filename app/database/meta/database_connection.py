from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class DatabaseConnection(ABC):
    @property
    @abstractmethod
    def session(self) -> Session:
        pass

    @abstractmethod
    def _build_engine(self):
        pass

    @abstractmethod
    def _create_session(self, engine):
        pass

    @abstractmethod
    def _get_url(self):
        pass

    @abstractmethod
    def _create_schema(self, connectable):
        pass

    @abstractmethod
    def _create_all(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def get_engine(self):
        pass

