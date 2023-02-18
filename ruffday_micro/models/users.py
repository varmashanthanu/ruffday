from datetime import datetime
from typing import Optional
from pydantic import EmailStr

from .shared.model_base import ResourceBase


class User(ResourceBase):
    email: EmailStr
    username: Optional[str]
    email_verified: bool = False
    is_active: bool = True


