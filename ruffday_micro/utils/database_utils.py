from enum import Enum
from typing import Dict, Any
from urllib.error import HTTPError

import deta
from pydantic import BaseModel, ValidationError
from deta import Deta


class DatabaseManager:
    deta = Deta()

    @classmethod
    def clean_resource(cls, resource: Dict) -> Dict:
        """

        Args:
            resource:

        Returns:

        """
        for key, value in resource.items():
            if isinstance(value, Enum):
                resource.update({key: value.value})
            elif isinstance(value, Dict):
                resource.update({key: cls.clean_resource(resource=value)})

        return resource

    @classmethod
    def write_to_db(
        cls,
        db_name: Any,
        resource: Dict
    ):
        """
        Method to write object to the Deta.Base
        Args:
            db_name:
            resource:

        Returns:

        """
        db = deta.Base(db_name)
        cleaned_resource = cls.clean_resource(resource=resource)
        try:
            return db.insert(data=cleaned_resource)

        except HTTPError as e:
            return db.put(data=cleaned_resource)

        except Exception as e:
            raise e

    @classmethod
    def read_from_db(
        cls,
        db_name: str,
        key: str
    ):
        """

        Args:
            db_name:
            key:

        Returns:

        """
        db = deta.Base(db_name)
        return db.get(key=key)

    @classmethod
    def search_db(
        cls,
        db_name: str,
        search_params: Dict
    ):
        """

        Args:
            db_name:
            search_params:

        Returns:

        """
        db = deta.Base(db_name)
        return db.fetch(query=search_params)

    @classmethod
    def delete_from_db(
        cls,
        db_name: Any,
        key: str
    ):
        db = deta.Base(db_name)
        try:
            if cls.read_from_db(db_name=db_name, key=key):
                db.delete(key=key)
            else:
                raise ValueError(f"Could not find {db_name} with ID {key}")

        except Exception as e:

            raise e
