"""Integration & Forensic Tests for Milestone 3 Cloud Runtime (Firestore, Pub/Sub, Worker, Idempotency)."""

import os
import json
import base64
import unittest
from fastapi.testclient import TestClient
from backend.api.server import app
from backend.cloud.firestore.audit_state import (
    AuditStage,
    AuditJobRecord,
    InMemoryAuditStateStore
)
from backend.cloud.pubsub.worker import PubSubAuditWorker
from backend.cloud.pubsub.publisher import LocalThreadPublisher


class TestCloudRuntimeForensics(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.integritylab_dir = os.path.join(self.base_dir, "integritylab")
        self.source_dir = os.path.join(self.integritylab_dir, "source")
        self.data_alpha = os.path.join(self.integritylab_dir, "data", "trades_alpha_failure.csv")
        self.report_alpha = os.path.join(self.integritylab_dir, "reports", "alpha_performance_report.json")
        self.data_control = os.path.join(self.integritylab_dir, "data", "trades_control_case.csv")
        self.report_control = os.path.join(self.integritylab_dir, "reports", "control_performance_report.json")
        self.client = TestClient(app)

    def test_in_memory_state_store_lifecycle(self):
        store = InMemoryAuditStateStore()
        record = store.create_audit("test-1", "TestProj", "/path/repo", "/path/data.csv", "/path/report.json")
        self.assertEqual(record.stage, AuditStage.CREATED)
        self.assertEqual(record.progress_pct, 0)

        record.update_stage(AuditStage.INVESTIGATING, progress_pct=50)
        store.update_audit(record)

        fetched = store.get_audit("test-1")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.stage, AuditStage.INVESTIGATING)
        self.assertEqual(fetched.progress_pct, 50)

        # Test failure recording
        fetched.record_failure("Verification timeout")
        store.update_audit(fetched)
        failed_record = store.get_audit("test-1")
        self.assertEqual(failed_record.stage, AuditStage.FAILED)
        self.assertEqual(failed_record.error, "Verification timeout")
        self.assertEqual(failed_record.retry_count, 1)

    def test_pubsub_worker_pipeline_execution(self):
        store = InMemoryAuditStateStore()
        msg_payload = {
            "audit_id": "ps-worker-test-alpha",
            "project_name": "IntegrityLab-Alpha-Worker",
            "repo_path": self.source_dir,
            "data_file": self.data_alpha,
            "report_file": self.report_alpha,
            "claimed_fee_bps": 5.0
        }
        
        success = PubSubAuditWorker.process_message(msg_payload, store)
        self.assertTrue(success)

        record = store.get_audit("ps-worker-test-alpha")
        self.assertIsNotNone(record)
        self.assertEqual(record.stage, AuditStage.COMPLETED)
        self.assertEqual(record.progress_pct, 100)
        self.assertIsNotNone(record.result)
        self.assertEqual(record.result["findings_count"], 4)

    def test_pubsub_worker_idempotency_duplicate_delivery(self):
        """A duplicate Pub/Sub message must not re-execute an already COMPLETED or RUNNING audit."""
        store = InMemoryAuditStateStore()
        msg_payload = {
            "audit_id": "ps-idempotent-test",
            "project_name": "IdempotencyCheck",
            "repo_path": self.source_dir,
            "data_file": self.data_control,
            "report_file": self.report_control,
            "claimed_fee_bps": 5.0
        }

        # 1st delivery
        success_1 = PubSubAuditWorker.process_message(msg_payload, store)
        self.assertTrue(success_1)
        record = store.get_audit("ps-idempotent-test")
        self.assertEqual(record.stage, AuditStage.COMPLETED)
        first_completed_at = record.updated_at

        # 2nd duplicate delivery
        success_2 = PubSubAuditWorker.process_message(msg_payload, store)
        self.assertTrue(success_2)
        # Verify stage remains COMPLETED and timestamp was not changed by re-execution
        self.assertEqual(record.stage, AuditStage.COMPLETED)
        self.assertEqual(record.updated_at, first_completed_at)

    def test_pubsub_worker_idempotency_when_already_running(self):
        store = InMemoryAuditStateStore()
        record = store.create_audit(
            audit_id="ps-running-test",
            project_name="RunningCheck",
            repo_path=self.source_dir,
            data_file=self.data_control,
            report_file=self.report_control
        )
        record.update_stage(AuditStage.RUNNING, progress_pct=25)
        store.update_audit(record)

        msg_payload = {
            "audit_id": "ps-running-test",
            "project_name": "RunningCheck",
            "repo_path": self.source_dir,
            "data_file": self.data_control,
            "report_file": self.report_control
        }

        # Delivery while RUNNING: should return True immediately without resetting state
        success = PubSubAuditWorker.process_message(msg_payload, store)
        self.assertTrue(success)
        self.assertEqual(record.stage, AuditStage.RUNNING)
        self.assertEqual(record.progress_pct, 25)

    def test_cloudrun_pubsub_push_endpoint(self):
        """Tests Cloud Run push webhook endpoint POST /api/audits/pubsub/push."""
        payload = {
            "audit_id": "push-test-1",
            "project_name": "PushWebhookAudit",
            "repo_path": self.source_dir,
            "data_file": self.data_control,
            "report_file": self.report_control,
            "claimed_fee_bps": 5.0
        }
        b64_data = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")

        push_body = {
            "message": {
                "data": b64_data,
                "messageId": "msg-12345"
            }
        }

        response = self.client.post("/api/audits/pubsub/push", json=push_body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "SUCCESS")
        self.assertEqual(response.json()["audit_id"], "push-test-1")


if __name__ == "__main__":
    unittest.main()
