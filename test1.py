#!/usr/bin/python3
import logging
from models.storage.db import UserDB
from models.user import User

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    # Initialize database
    logger.info("Initializing database connection")
    db = UserDB()

    # Create a new user
    logger.info("Creating new user object")
    new_user = User(
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )
    new_user.password = "securepassword"

    # Add user to database
    logger.info("Attempting to add user to database")
    if db.add_user(new_user):
        logger.info("User added successfully")
        print("User added successfully")
    else:
        logger.error("Failed to add user")
        print("Failed to add user")

except Exception as e:
    logger.error(f"Test failed with error: {str(e)}", exc_info=True)