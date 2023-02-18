from enum import Enum
from deta import Deta
from core.config import Settings
from utils import DatabaseManager
from .model_base import ResourceBase
import os


class DetailsBaseClass(ResourceBase):
    parent_id: str
    pass
