import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "books.settings")
django.setup()
from django.test import TestCase
from store.logic import operations

class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(1, 1, '+')
        self.assertEqual(2, result)

    def test_plus_char(self):
        result = operations('1', '1', '+')
        self.assertEqual('11', result)
        
    def test_multiply(self):
        result = operations(25, 11, '*')
        self.assertEqual(275 , result)