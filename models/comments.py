from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship

class Comment(BaseModel):
    """Comment model for blog posts"""
    __tablename__ = 'comments'

    content = Column(Text, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    blog_id = Column(String(60), ForeignKey('blogs.id'), nullable=False)

    user = relationship("User", back_populates="comments")
    blog = relationship("Blog", back_populates="comments")
