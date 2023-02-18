from enum import Enum
from deta import Deta
from core.config import Settings
from utils import DatabaseManager
from pydantic import BaseModel
import os


class AddressesBaseClass(BaseModel):
    line_1: str
    line_2: str
    city: str
    state: str
    country: str
    zip_code: str

    def __repr__(self):
        return f"{self.city}, {self.country}"
