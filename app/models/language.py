from pydantic import BaseModel, Field
from enum import Enum


class LanguageEnum(str, Enum):
    PORTUGUESE = "portuguese"
    ENGLISH = "english"
    SPANISH = "spanish"
    FRENCH = "french"

