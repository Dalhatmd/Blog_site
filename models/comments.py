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

    def to_dict(self):
        """ dictionary representation of comments"""
        comment_dict = {
            'content': self.content,
            'user_id': self.user_id,
            'blog_id': self.blog_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'comment_id': self.id
        }
        return comment_dict
