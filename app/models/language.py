from pydantic import BaseModel, Field
from enum import Enum


class LanguageEnum(str, Enum):
    en = "en"  # English
    es = "es"  # Spanish
    fr = "fr"  # French
    de = "de"  # German
    pt = "pt" # Portuguese
    jp = "jp" # Japanese

