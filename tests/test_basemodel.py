import unittest
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.model = BaseModel()
        self.model2 = BaseModel()

    def test_initialization(self):
        self.assertIsInstance(self.model, BaseModel)

    def test_id(self):
        self.assertTrue(hasattr(self.model, 'id'))
        self.assertIsInstance(self.model.id, str)

    def test_to_json(self):
        result = self.model.to_json()
        self.assertIsInstance(result, dict)

    def test_str(self):
        result = self.model.__str__()
        self.assertIsInstance(result, str)

    def test_created_at(self):
        self.assertTrue(hasattr(self.model, 'created_at'))

    def test_updated_at(self):
        self.assertTrue(hasattr(self.model, 'updated_at'))

    def test_unique_id(self):
        self.assertNotEqual(self.model.id, self.model2.id)


    def tearDown(self):
        del self.model
        del self.model2

if __name__ == '__main__':
    unittest.main()