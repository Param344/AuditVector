"""API Integration Tests for AuditVector FastAPI endpoints."""

import time
import unittest
from fastapi.testclient import TestClient
from backend.api.server import app


class TestAuditAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "HEALTHY")

    def test_nonexistent_audit_returns_404(self):
        response = self.client.get("/api/audits/non-existent-id")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Audit not found")

    def test_nonexistent_audit_report_returns_404(self):
        response = self.client.get("/api/audits/non-existent-id/report")
        self.assertEqual(response.status_code, 404)

    def test_invalid_create_audit_request_returns_422(self):
        response = self.client.post("/api/audits", json={"invalid_payload": True})
        self.assertEqual(response.status_code, 422)

    def test_demo_alpha_audit_lifecycle(self):
        # Trigger demo alpha audit
        response = self.client.post("/api/audits/demo/alpha")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("audit_id", data)
        audit_id = data["audit_id"]

        # Poll status until COMPLETED (runs in local thread quickly)
        for _ in range(25):
            status_res = self.client.get(f"/api/audits/{audit_id}")
            self.assertEqual(status_res.status_code, 200)
            status_data = status_res.json()
            if status_data["stage"] == "COMPLETED":
                break
            time.sleep(0.05)

        self.assertEqual(status_data["stage"], "COMPLETED")
        self.assertIsNotNone(status_data["result"])
        
        # Test markdown report retrieval
        report_res = self.client.get(f"/api/audits/{audit_id}/report")
        self.assertEqual(report_res.status_code, 200)
        self.assertIn("markdown", report_res.json())
        self.assertIn("AUDITVECTOR FINANCIAL INTEGRITY REPORT", report_res.json()["markdown"])

    def test_demo_control_audit_lifecycle(self):
        # Trigger demo control audit
        response = self.client.post("/api/audits/demo/control")
        self.assertEqual(response.status_code, 200)
        audit_id = response.json()["audit_id"]

        # Poll status until COMPLETED
        for _ in range(25):
            status_res = self.client.get(f"/api/audits/{audit_id}")
            self.assertEqual(status_res.status_code, 200)
            status_data = status_res.json()
            if status_data["stage"] == "COMPLETED":
                break
            time.sleep(0.05)

        self.assertEqual(status_data["stage"], "COMPLETED")
        self.assertEqual(status_data["result"]["report"]["verdict"], "✅ FINANCIAL INTEGRITY VERIFIED")

    def test_list_audits_endpoint(self):
        response = self.client.get("/api/audits")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)


if __name__ == "__main__":
    unittest.main()
