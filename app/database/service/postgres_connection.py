from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.schema import CreateSchema

from app.database.meta.database_connection import DatabaseConnection
from app.database.service.postgres_config import PostgresConfig
from app.database.meta.schema import schema


class PostgresConnection(DatabaseConnection):
    def __init__(self):
        self._config = PostgresConfig()
        self._engine = self._build_engine()
        self._create_schema(self._engine)
        self._session_maker = self._create_session(self._engine)
        self._create_all()

    @property
    def session(self) -> Session:
        return self._session_maker()

    def _build_engine(self):
        """Cria e retorna o engine para conexão com o banco de dados."""
        url = self._config.database_url
        return create_engine(url, echo=False, pool_size=5, max_overflow=10, pool_pre_ping=True)

    def _create_session(self, engine):
        """Cria e retorna a fábrica de sessões."""
        return sessionmaker(bind=engine)

    def _get_url(self):
        """Obtém a URL do banco de dados."""
        return self._config.database_url

    def _create_schema(self, engine):
        """Cria o esquema do banco de dados se não existir."""
        with engine.connect() as connection:
            connection.execute(CreateSchema(schema, if_not_exists=True))
            connection.commit()

    def _create_all(self):
        """Cria todas as tabelas no banco de dados."""
        Base = self._config.declarative_base
        Base.metadata.create_all(self._engine)

    def disconnect(self):
        """Fecha a sessão e limpa o recurso."""
        if self._session_maker:
            self._session_maker().close()
        self._engine.dispose()

    def get_engine(self):
        """Retorna o engine de conexão."""
        return self._engine

