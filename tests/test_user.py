import unittest
from datetime import datetime
from models.user import User

class TestUser(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.user = User(email="test@example.com", first_name="John", last_name="Doe")

    def test_user_initialization(self):
        """Test user initialization"""
        self.assertIsNotNone(self.user.id)
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertIsInstance(self.user.created_at, datetime)
        self.assertIsInstance(self.user.updated_at, datetime)

    def test_password_setter(self):
        """Test password setter"""
        self.user.password = "password123"
        self.assertNotEqual(self.user._password, "password123")
        self.assertEqual(len(self.user._password), 64)

    def test_password_getter(self):
        """Test password getter"""
        self.user.password = "password123"
        self.assertEqual(self.user.password, self.user._password)

    def test_is_valid_password(self):
        """Test password validation"""
        self.user.password = "password123"
        self.assertTrue(self.user.is_valid_password("password123"))
        self.assertFalse(self.user.is_valid_password("wrongpassword"))

    def test_display_name(self):
        """Test display name"""
        self.assertEqual(self.user.display_name(), "John Doe")
        self.user.first_name = None
        self.assertEqual(self.user.display_name(), "Doe")
        self.user.last_name = None
        self.assertEqual(self.user.display_name(), "test@example.com")
        self.user.email = None
        self.assertEqual(self.user.display_name(), "")

if __name__ == '__main__':
    unittest.main()
