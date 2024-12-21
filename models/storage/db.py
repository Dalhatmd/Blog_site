from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from os import getenv
from models.user import User, Base
import logging

class UserDB:
    """Database manager for User objects using SQLAlchemy"""
    
    def __init__(self):
        """Initialize database connection and create tables"""
        # Set up logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        
        try:
            # Get database credentials from environment variables
            mysql_host = getenv('MYSQL_HOST', 'localhost')
            mysql_user = getenv('MYSQL_USER', 'root')
            mysql_pwd = getenv('MYSQL_PWD')
            mysql_db = getenv('MYSQL_DB')
            
            self.logger.info(f"Database configuration - Host: {mysql_host}, User: {mysql_user}, DB: {mysql_db}")
            
            if not all([mysql_host, mysql_user, mysql_pwd, mysql_db]):
                raise ValueError("Missing required environment variables for database connection")
            
            # Create database URL
            self.database_url = f'mysql+mysqldb://{mysql_user}:{mysql_pwd}@{mysql_host}/{mysql_db}'
            self.logger.debug(f"Database URL created: {self.database_url.replace(mysql_pwd, '****')}")
            
            # Initialize engine with debugging
            self._engine = create_engine(
                self.database_url,
                pool_pre_ping=True,
                echo=True
            )
            self.logger.info("Database engine created successfully")
            
            # Create session maker
            self._Session = sessionmaker(bind=self._engine)
            self.logger.info("Session maker created successfully")
            
            # Create tables
            Base.metadata.create_all(self._engine)
            self.logger.info("Database tables created/verified successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
            raise
    
    def add_user(self, user: User) -> bool:
        """Add a new user to the database"""
        session = None
        try:
            self.logger.info(f"Attempting to add user with email: {user.email}")
            session = self._Session()
            
            # Log user details (excluding password)
            self.logger.debug(f"User details - ID: {user.id}, Email: {user.email}, "
                            f"Name: {user.first_name} {user.last_name}")
            
            # Add user to session
            session.add(user)
            self.logger.debug("User added to session")
            
            # Flush to detect any issues before commit
            session.flush()
            self.logger.debug("Session flushed successfully")
            
            # Commit the transaction
            session.commit()
            self.logger.info("User successfully added to database")
            return True
            
        except SQLAlchemyError as e:
            self.logger.error(f"SQLAlchemy error while adding user: {str(e)}", exc_info=True)
            if session:
                session.rollback()
            return False
            
        except Exception as e:
            self.logger.error(f"Unexpected error while adding user: {str(e)}", exc_info=True)
            if session:
                session.rollback()
            return False
            
        finally:
            if session:
                session.close()
                self.logger.debug("Database session closed")

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email"""
        try:
            session = self._Session()
            user = session.query(User).filter(User.email == email).first()
            if user:
                self.logger.info(f"Found user with email: {email}")
            else:
                self.logger.info(f"No user found with email: {email}")
            return user
        except SQLAlchemyError as e:
            self.logger.error(f"Error retrieving user by email: {str(e)}")
            return None
        finally:
            session.close()