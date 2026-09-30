import os
import unittest
from unittest.mock import patch

from gemini_client import get_api_key, generate_text


class GeminiClientTests(unittest.TestCase):
    def test_get_api_key_reads_environment(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=True):
            self.assertEqual(get_api_key(), "test-key")

    @patch("gemini_client.genai.Client")
    def test_generate_text_uses_client_response(self, mock_client):
        mock_response = type("Response", (), {"text": "hello from gemini"})()
        mock_client.return_value.models.generate_content.return_value = mock_response

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=True):
            self.assertEqual(generate_text("hello"), "hello from gemini")


if __name__ == "__main__":
    unittest.main()
