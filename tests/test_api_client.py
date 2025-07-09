# Tests básicos para api_client 

import unittest
from unittest.mock import patch, Mock
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.api_client import health_check, ready_check, query_rag_api


class TestAPIClient(unittest.TestCase):

    @patch('utils.api_client.requests.get')
    def test_health_check_success(self, mock_get):
        # Mock de respuesta exitosa
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = health_check()
        self.assertTrue(result)
        mock_get.assert_called_once()

    @patch('utils.api_client.requests.get')
    def test_health_check_failure(self, mock_get):
        # Mock de respuesta fallida
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = health_check()
        self.assertFalse(result)

    @patch('utils.api_client.requests.get')
    def test_ready_check_success(self, mock_get):
        # Mock de respuesta exitosa
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = ready_check()
        self.assertTrue(result)
        mock_get.assert_called_once()

    @patch('utils.api_client.requests.get')
    def test_ready_check_failure(self, mock_get):
        # Mock de respuesta fallida
        mock_response = Mock()
        mock_response.status_code = 503
        mock_get.return_value = mock_response

        result = ready_check()
        self.assertFalse(result)

    @patch('utils.api_client.requests.post')
    def test_query_rag_api_success(self, mock_post):
        # Mock de respuesta exitosa
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "answer": "Test answer",
            "sources": [],
            "metadata": {}
        }
        mock_post.return_value = mock_response

        result = query_rag_api("test query")
        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result["answer"], "Test answer")
        mock_post.assert_called_once()

    @patch('utils.api_client.requests.post')
    def test_query_rag_api_failure(self, mock_post):
        # Mock de respuesta fallida
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_post.return_value = mock_response

        result = query_rag_api("test query")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main() 