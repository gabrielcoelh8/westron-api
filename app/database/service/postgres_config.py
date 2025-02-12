from os import environ

from sqlalchemy.engine import URL

from app.database.meta.database_config import DatabaseConfig
from app.database.meta.declarative_base import postgres_base


class PostgresConfig(DatabaseConfig):
    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername=environ.get('POSTGRES_DRIVERNAME'),
            username=environ.get('FUNDACOES_DB_USERNAME'),
            password=environ.get('FUNDACOES_DB_PASSWORD'),
            host=environ.get('FUNDACOES_DB_HOSTNAME'),
            port=environ.get('FUNDACOES_DB_PORT'),
            database=environ.get('FUNDACOES_DB_DATABASE'),
        )

    @property
    def track_modifications(self) -> bool:
        return False

    @property
    def declarative_base(self):
        return postgres_base
