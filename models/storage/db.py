from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from os import getenv
from models.blogs import Blog
from models.user import User, Base
from datetime import datetime

models = {'User': User}

class DB:
    """Database manager for User objects using SQLAlchemy"""
    
    def __init__(self):
        """Initialize database connection and create tables"""
        
        try:
            # Get database credentials from environment variables
            mysql_host = getenv('MYSQL_HOST', 'localhost')
            mysql_user = getenv('MYSQL_USER', 'root')
            mysql_pwd = getenv('MYSQL_PWD')
            mysql_db = getenv('MYSQL_DB')
            mysql_mode = getenv('MYSQL_MODE')
            
            if not all([mysql_host, mysql_user, mysql_pwd, mysql_db]):
                raise ValueError("Missing required environment variables for database connection")
            
            # Create database URL
            self.database_url = f'mysql+mysqldb://{mysql_user}:{mysql_pwd}@{mysql_host}/{mysql_db}'
            
            # Initialize engine with debugging
            self._engine = create_engine(
                self.database_url,
                pool_pre_ping=True,
                echo=True
            )
            if mysql_mode == 'test':
                Base.metadata.drop_all(self._engine)
            
            # Create session maker
            self._Session = sessionmaker(bind=self._engine, expire_on_commit=False)
            
            # Create tables
            Base.metadata.create_all(self._engine)
            
        except Exception as e:
            raise

    def add_user(self, user: User) -> bool:
        """Add a new user to the database"""
        session = None
        try:
            session = self._Session()
            
            # Add user to session
            session.add(user)            
            # Flush to detect any issues before commit
            session.flush()
            
            # Commit the transaction
            session.commit()
            return True
            
        except SQLAlchemyError as e:
            if session:
                session.rollback()
            return False
            
        except Exception as e:
            if session:
                session.rollback()
            return False
            
        finally:
            if session:
                session.close()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email"""
        try:
            session = self._Session()
            user = session.query(User).filter(User.email == email).first()
            return user
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()

    def create_blog(self, user_id: str, title: str, content: str) -> Optional[Blog]:
        """Create a new blog post for a user"""
        try:
            session = self._Session()
            user = session.query(User).filter(User.id == user_id).first()
            
            if not user:
                return None
                
            blog = Blog(
                title=title,
                content=content,
                user_id=user_id
            )
            
            session.add(blog)
            session.commit()
            return blog
            
        except SQLAlchemyError as e:
            session.rollback()
            return None
        finally:
            session.close()
    
    def get_user_blogs(self, user_id: str) -> List[Blog]:
        """Get all blogs for a user"""
        try:
            session = self._Session()
            blogs = session.query(Blog).filter(Blog.user_id == user_id).all()
            return blogs
        except SQLAlchemyError as e:
            return []
        finally:
            session.close()
    
    def get_blog(self, blog_id: str) -> Optional[Blog]:
        """Get a specific blog by ID"""
        try:
            session = self._Session()
            blog = session.query(Blog).filter(Blog.id == blog_id).first()
            return blog
        except SQLAlchemyError as e:
            return None
        finally:
            session.close()
    
    def update_blog(self, blog_id: str, title: str = None, content: str = None) -> bool:
        """Update a blog post"""
        try:
            session = self._Session()
            blog = session.query(Blog).filter(Blog.id == blog_id).first()
            
            if not blog:
                return False
                
            if title:
                blog.title = title
            if content:
                blog.content = content
                
            blog.updated_at = datetime.now()
            session.commit()
            return True
            
        except SQLAlchemyError as e:
            session.rollback()
            return False
        finally:
            session.close()
    
    def delete_blog(self, blog_id: str) -> bool:
        """Delete a blog post"""
        try:
            session = self._Session()
            blog = session.query(Blog).filter(Blog.id == blog_id).first()
            
            if not blog:
                return False
                
            session.delete(blog)
            session.commit()
            return True
            
        except SQLAlchemyError as e:
            session.rollback()
            return False
        finally:
            session.close()
