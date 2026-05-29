import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import is_valid_username, is_valid_password, internship_belongs_to_user
import unittest

class TestBusinessLogic(unittest.TestCase):

    # Tests for is_valid_username
    def test_username_valid(self):
        self.assertTrue(is_valid_username('ahmad'))

    def test_username_too_short(self):
        self.assertFalse(is_valid_username('ab'))

    def test_username_exactly_3(self):
        self.assertTrue(is_valid_username('abc'))

    # Tests for is_valid_password
    def test_password_valid(self):
        self.assertTrue(is_valid_password('mypassword'))

    def test_password_too_short(self):
        self.assertFalse(is_valid_password('123'))

    def test_password_exactly_6(self):
        self.assertTrue(is_valid_password('123456'))

    # Tests for internship_belongs_to_user
    def test_internship_belongs_to_user(self):
        self.assertTrue(internship_belongs_to_user(1, 1))

    def test_internship_not_belongs_to_user(self):
        self.assertFalse(internship_belongs_to_user(1, 2))


if __name__ == '__main__':
    unittest.main()