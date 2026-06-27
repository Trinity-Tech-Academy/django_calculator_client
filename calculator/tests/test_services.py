# calculator/tests/test_services.py
from unittest.mock import patch, Mock
from django.test import TestCase
from calculator import services
 
 
class TestGetOperations(TestCase):
    @patch('calculator.services.requests.get')
    def test_returns_list(self, mock_get):
        mock_get.return_value = Mock(
            json=lambda: {'operations': ['add', 'subtract']},
            raise_for_status=lambda: None,
        )
        result = services.get_operations()
        self.assertEqual(result, ['add', 'subtract'])
 
 
class TestCompute(TestCase):
    @patch('calculator.services.requests.post')
    def test_multiply(self, mock_post):
        mock_post.return_value = Mock(
            json=lambda: {
                'operation': 'multiply', 'symbol': '*',
                'a': 6.0, 'b': 7.0, 'result': 42.0
            },
            raise_for_status=lambda: None,
        )
        result = services.compute('multiply', 6, 7)
        self.assertEqual(result['result'], 42.0)
        