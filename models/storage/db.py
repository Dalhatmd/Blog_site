from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Type, Any, Dict
from os import getenv
from models.blogs import Blog
from models.user import User
from models.base_model import BaseModel
from models.base_model import Base
from models.comments import Comment


# Define models dictionary - can be expanded with more models
models: Dict[str, Type[BaseModel]] = {
    'User': User,
    'Blog': Blog,
    'Comment': Comment
}

class DB:
    """Generic database manager for SQLAlchemy models"""
    
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
                echo=False
            )
            if mysql_mode == 'test':
                Base.metadata.drop_all(self._engine)
            
            # Create session maker
            self._Session = sessionmaker(bind=self._engine, expire_on_commit=False)
            
            # Create tables
            Base.metadata.create_all(self._engine)
            
        except Exception as e:
            raise

    def _get_model(self, model_name: str) -> Type[BaseModel]:
        """Get model class by name"""
        if model_name not in models:
            raise ValueError(f"Model {model_name} not found in registered models")
        return models[model_name]

    def add(self, model_name: str, instance: BaseModel) -> Optional[BaseModel]:
        """Add a new instance to the database"""
        session = None
        try:
            model_class = self._get_model(model_name)
            if not isinstance(instance, model_class):
                raise ValueError(f"Instance must be of type {model_class.__name__}")
                
            session = self._Session()
            session.add(instance)
            session.flush()
            session.commit()
            return instance
            
        except (SQLAlchemyError, Exception) as e:
            if session:
                session.rollback()
            return None
            
        finally:
            if session:
                session.close()

    def get_by_field(self, model_name: str, field_name: str, value: Any) -> Optional[BaseModel]:
        """Retrieve an instance by field value"""
        try:
            model_class = self._get_model(model_name)
            session = self._Session()
            
            if not hasattr(model_class, field_name):
                raise ValueError(f"Field {field_name} not found in model {model_name}")
                
            instance = session.query(model_class).filter(
                getattr(model_class, field_name) == value
            ).first()
            return instance
            
        except (SQLAlchemyError, Exception) as e:
            return None
            
        finally:
            session.close()

    def get_all_by_field(self, model_name: str, field_name: str, value: Any) -> List[BaseModel]:
        """Retrieve all instances matching a field value"""
        try:
            model_class = self._get_model(model_name)
            session = self._Session()
            
            if not hasattr(model_class, field_name):
                raise ValueError(f"Field {field_name} not found in model {model_name}")
                
            instances = session.query(model_class).filter(
                getattr(model_class, field_name) == value
            ).all()
            return instances
            
        except (SQLAlchemyError, Exception) as e:
            return []
            
        finally:
            session.close()

    def update(self, model_name: str, instance_id: str, **kwargs) -> bool:
        """Update an instance with provided fields"""
        try:
            model_class = self._get_model(model_name)
            session = self._Session()
            
            instance = session.query(model_class).filter(
                model_class.id == instance_id
            ).first()
            
            if not instance:
                return False
                
            for field, value in kwargs.items():
                if hasattr(instance, field):
                    setattr(instance, field, value)
            
            session.commit()
            return True
            
        except (SQLAlchemyError, Exception) as e:
            session.rollback()
            return False
            
        finally:
            session.close()

    def delete(self, model_name: str, instance_id: str) -> bool:
        """Delete an instance by ID"""
        try:
            model_class = self._get_model(model_name)
            session = self._Session()
            
            instance = session.query(model_class).filter(
                model_class.id == instance_id
            ).first()
            
            if not instance:
                return False
                
            session.delete(instance)
            session.commit()
            return True
            
        except (SQLAlchemyError, Exception) as e:
            session.rollback()
            return False
            
        finally:
            session.close()