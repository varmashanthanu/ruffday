from typing import Optional

from pydantic import BaseModel, ValidationError
from enum import Enum
from core.config import Settings
from .model_base import ResourceBase
from . import AddressesBaseClass
from utils import DatabaseManager


class ListingTypes(Enum):
    ADOPTIONS = "adoptions"
    ORGANIZATIONS = "organizations"


class ListingsBaseClass(ResourceBase):
    name: str
    listing_type: str


class OrganizationListings(ListingsBaseClass):
    address_id: Optional[str] = None
    phone: str = None
    email: str = None
    is_verified: bool = False

    address: AddressesBaseClass

    db = Settings.ORGANIZATIONS_DB_NAME

    listing_type = ListingTypes.ORGANIZATIONS.value

    @property
    def location(self) -> str:
        return self.address.__repr__()
