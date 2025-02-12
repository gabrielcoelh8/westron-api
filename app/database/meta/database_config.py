from abc import ABC, abstractmethod
from sqlalchemy.engine import URL


class DatabaseConfig(ABC):
    @property
    @abstractmethod
    def database_url(self) -> URL:
        pass

    @property
    @abstractmethod
    def track_modifications(self) -> bool:
        pass

    @property
    @abstractmethod
    def declarative_base(self):
        pass
