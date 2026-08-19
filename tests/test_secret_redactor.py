"""Unit tests for SecretRedactor."""

import unittest
from backend.security.secret_redactor import SecretRedactor


class TestSecretRedactor(unittest.TestCase):

    def test_api_key_redaction(self):
        sample = 'api_key = "AIzaSyD-1234567890abcdefghijklmn"'
        sanitized, count = SecretRedactor.sanitize(sample)
        self.assertGreater(count, 0)
        self.assertNotIn("AIzaSyD-1234567890abcdefghijklmn", sanitized)
        self.assertIn("[REDACTED]", sanitized)

    def test_binance_secret_redaction(self):
        sample = 'binance_secret = "4f8a9b2c1d3e5f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a"'
        sanitized, count = SecretRedactor.sanitize(sample)
        self.assertGreater(count, 0)
        self.assertNotIn("4f8a9b2c1d3e5f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a", sanitized)
        self.assertIn("[REDACTED]", sanitized)

    def test_clean_text_no_redaction(self):
        sample = 'def calculate_pnl(price, qty):\n    return price * qty'
        sanitized, count = SecretRedactor.sanitize(sample)
        self.assertEqual(count, 0)
        self.assertEqual(sanitized, sample)


if __name__ == "__main__":
    unittest.main()
