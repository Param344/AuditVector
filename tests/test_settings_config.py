"""Unit tests for Settings & Model Configuration."""

import unittest
from backend.config.settings import Settings


class TestSettings(unittest.TestCase):

    def test_default_model_configuration_is_gemini_35_plus(self):
        self.assertEqual(Settings.GEMINI_MODEL, "gemini-3.5-flash")
        self.assertTrue(Settings.get_resolved_model().startswith("gemini-3.5") or "gemini-3" in Settings.get_resolved_model())

    def test_validation_without_api_key_raises_error(self):
        original_key = Settings.GOOGLE_API_KEY
        Settings.GOOGLE_API_KEY = None
        try:
            with self.assertRaises(ValueError):
                Settings.validate_for_live_execution()
        finally:
            Settings.GOOGLE_API_KEY = original_key


if __name__ == "__main__":
    unittest.main()
