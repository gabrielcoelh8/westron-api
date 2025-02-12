from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base


class Base(DeclarativeBase):
    pass

postgres_base = declarative_base()