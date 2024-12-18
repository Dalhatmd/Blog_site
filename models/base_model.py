#!/usr/bin/python3
""" Basemodel class module """
import uuid
from datetime import datetime

class BaseModel:
    """ Basemodel class """
    def __init__(self, *args, **kwargs):
        """ Basemodel class constructor """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key,
                            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                elif key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """ Returns string representation of Basemodel class """
        return f"BaseModel: {self.id} created_at: {self.created_at} updated_at: {self.updated_at}"

    def to_json(self):
        """ Returns dictionary representation of Basemodel class """
        json_dict = self.__dict__.copy()
        json_dict["created_at"] = self.created_at.isoformat()
        json_dict["updated_at"] = self.updated_at.isoformat()
        json_dict["__class__"] = self.__class__.__name__
        return json_dict
    
    def save(self):
        """Updates the updated at time"""
        self.updated_at = datetime.now()

    