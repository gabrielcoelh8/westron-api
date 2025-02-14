from os import environ

from sqlalchemy.engine import URL

from app.database.meta.database_config import DatabaseConfig
from app.database.meta.declarative import Base


class PostgresConfig(DatabaseConfig):
    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername=environ.get('POSTGRES_DRIVERNAME'),
            username=environ.get('POSTGRES_USER'),
            password=environ.get('POSTGRES_PASSWORD'),
            host=environ.get('POSTGRES_DB_HOSTNAME'),
            port=environ.get('POSTGRES_DB_PORT'),
            database=environ.get('POSTGRES_DB_DATABASE'),
        )

    @property
    def track_modifications(self) -> bool:
        return False

    @property
    def declarative_base(self):
        return Base
