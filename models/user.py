from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import hashlib
from models.base_model import BaseModel


class User(BaseModel):
    """ User class for SQLAlchemy
    """
    __tablename__ = 'users'

    id = Column(String(60), primary_key=True)
    email = Column(String(255), nullable=True, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    _password = Column('password', String(128), nullable=True)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    username = Column(String(128), nullable=True, unique=True)

    blogs = relationship("Blog", back_populates="user", cascade="all, delete-orphan")
    
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        super().__init__()
        
        if kwargs.get('id') is None:
            from uuid import uuid4
            self.id = str(uuid4())
            
        from datetime import datetime
        if kwargs.get('created_at') is None:
            self.created_at = datetime.now()
        if kwargs.get('updated_at') is None:
            self.updated_at = datetime.now()

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def password(self) -> str:
        """ Getter of the password
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """ Setter of a new password: encrypt in SHA256
        """
        if pwd is None or not isinstance(pwd, str):
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate a password
        """
        if pwd is None or not isinstance(pwd, str):
            return False
        if self.password is None:
            return False
        pwd_e = pwd.encode()
        return hashlib.sha256(pwd_e).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """ Display User name based on email/first_name/last_name
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None and self.username is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)

