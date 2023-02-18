from typing import Optional
from core.config import Settings
from utils import DatabaseManager
from .shared import DetailsBaseClass, ListingsBaseClass, OrganizationListings, ListingTypes, AddressesBaseClass
from enum import Enum


class AdoptionStatus(Enum):
    AVAILABLE = "available"
    ADOPTED = "adopted"


class AdoptionDetails(DetailsBaseClass):
    energy: Optional[str] = None
    height: Optional[str] = None
    height_unit: Optional[str] = None
    weight: Optional[str] = None
    weight_unit: Optional[str] = None
    history: Optional[str] = None
    home_type: Optional[str] = None
    other_animals_friendly: Optional[str] = None
    children_friendly: Optional[str] = None
    family_friendly: Optional[str] = None
    stranger_friendly: Optional[str] = None
    notes: Optional[str] = None


class AdoptionOrganizations(OrganizationListings):

    pass


class AdoptionListings(ListingsBaseClass):
    age: int
    age_units: str
    breed: str
    img_url: Optional[str]
    status: AdoptionStatus = AdoptionStatus.AVAILABLE
    details_id: Optional[str] = None
    organization_id: Optional[str] = None
    is_verified: bool = False

    def __get_organization_data(self):
        od = DatabaseManager.read_from_db(
            db_name=Settings.ORGANIZATIONS_DB_NAME,
            key=self.organization_id
        )

        return AdoptionOrganizations(**od)

    organization_data: Optional[AdoptionOrganizations] = None

    db = Settings.ADOPTIONS_DB_NAME

    listing_type = ListingTypes.ADOPTIONS.value

    @property
    def organization(self):
        if not self.organization_data:
            self.organization_data = self.__get_organization_data()

        return self.organization_data

    @property
    def location(self) -> str:
        return self.organization.location
