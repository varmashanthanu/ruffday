from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ValidationError, validator
from utils import DatabaseManager


class ResourceBase(BaseModel):

    db: str
    key: str
    created_date: Optional[datetime]
    updated_date: Optional[datetime]

    @classmethod
    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()

    """
    Private DB accessor methods
    """
    def _save_listing(self):
        return DatabaseManager.write_to_db(
            db_name=self.db,
            resource=self.dict()
        )

    def _does_listing_exist(self):
        response = DatabaseManager.read_from_db(
            db_name=self.db,
            key=self.key
        )

        return True if response else False

    """
    CRUD Methods
    """

    def update(self):
        try:
            if not self._does_listing_exist():
                raise ValueError(f"Resource with ID {self.key} does not exist!")

            return self._save_listing()

        except Exception as e:
            raise e

    def save(self):
        try:
            if self._does_listing_exist():
                raise ValueError(f"Resource with ID {self.key} already exists!")

            return self._save_listing()

        except Exception as e:
            raise e
