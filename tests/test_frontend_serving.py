"""Integration tests for Frontend static serving via FastAPI."""

import unittest
from fastapi.testclient import TestClient
from backend.api.server import app


class TestFrontendServing(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_serve_index_html_at_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers.get("content-type", ""))
        self.assertIn("AUDITVECTOR", response.text)
        self.assertIn("ADK MULTI-AGENT PIPELINE", response.text)

    def test_serve_static_css(self):
        response = self.client.get("/static/styles.css")
        self.assertEqual(response.status_code, 200)
        self.assertIn("AUDITVECTOR", response.text.upper())
        self.assertIn("--bg-base", response.text)

    def test_serve_static_javascript(self):
        response = self.client.get("/static/app.js")
        self.assertEqual(response.status_code, 200)
        self.assertIn("AUDITVECTOR", response.text.upper())
        self.assertIn("DOMContentLoaded", response.text)


if __name__ == "__main__":
    unittest.main()
