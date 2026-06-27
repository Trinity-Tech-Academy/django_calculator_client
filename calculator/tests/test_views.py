# calculator/tests/test_views.py
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
 
 
class TestIndexView(TestCase):
    @patch('calculator.views.services.get_operations')
    @patch('calculator.views.services.compute')
    def test_post_shows_result(self, mock_compute, mock_ops):
        mock_ops.return_value = ['add', 'multiply']
        mock_compute.return_value = {
            'operation': 'add', 'symbol': '+',
            'a': 3.0, 'b': 4.0, 'result': 7.0
        }
        url = reverse('calculator:index')
        response = self.client.post(url, {'operation': 'add', 'a': 3, 'b': 4})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '7.0')
 
    @patch('calculator.views.services.get_operations')
    def test_get_renders_form(self, mock_ops):
        mock_ops.return_value = ['add']
        response = self.client.get(reverse('calculator:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Operation')