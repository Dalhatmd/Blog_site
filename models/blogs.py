from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from models.user import Base

class Blog(Base):
    """Blog class for SQLAlchemy"""
    __tablename__ = 'blogs'

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    
    # Establish the relationship with User
    user = relationship("User", back_populates="blogs")
    
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Blog instance"""
        super().__init__()
        
        # Set ID if not provided
        self.id = str(uuid4()) if not kwargs.get('id') else kwargs['id']
        
        # Always set timestamps on creation
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Set other attributes from kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> dict:
        """Return dictionary representation of Blog"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id
        }
