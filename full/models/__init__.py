from .base import db
from .user import UserData
from .rights import UserRights
from .contact import UsersContacts
from .faculty import Faculty, UserFaculty

__all__ = [
    "db",
    "UserData",
    "UserRights",
    "UsersContacts",
    "Faculty",
    "UserFaculty"
]
