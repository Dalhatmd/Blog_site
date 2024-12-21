import unittest
from models.user import User
import bcrypt

class TestUser(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.user = User()


    def test_user_inheritance(self):
        """Test user inheritance"""
        self.assertIsInstance(self.user, User)
        self.assertTrue(hasattr(self.user, 'id'))
        self.assertTrue(hasattr(self.user, 'created_at'))

    def test_password_property(self):
        """Test password property"""
        self.user.password = "my_secret_password"
        self.assertTrue(bcrypt.checkpw("my_secret_password".encode().hexdigest().lower(), self.user._password.encode().hexdigest(.lower())))

    def test_is_valid_password(self):
        """Test is_valid_password method"""
        password = "my_secret_password"
        self.user.password = password
        self.assertTrue(self.user.is_valid_password(password))

    def test_to_json(self):
        """Test to_json method"""
        self.assertIsInstance(self.user.to_json(), dict)

if __name__ == '__main__':
    unittest.main()
