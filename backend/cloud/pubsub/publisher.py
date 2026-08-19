"""Google Cloud Pub/Sub and Local Job Publisher for Asynchronous Audit Dispatch."""

import json
import logging
import threading
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ...config.settings import settings
from ..firestore.audit_state import AuditJobRecord, AuditStage, BaseAuditStateStore
from ...workers.audit_worker import AuditWorker

logger = logging.getLogger("AuditVector.PubSub")


class BaseAuditJobPublisher(ABC):
    """Abstract publisher interface for dispatching audit jobs."""

    @abstractmethod
    def publish_audit_job(self, record: AuditJobRecord, claimed_fee_bps: float = 5.0) -> str:
        pass


class LocalThreadPublisher(BaseAuditJobPublisher):
    """Local async publisher using background threads for development and offline testing."""

    def __init__(self, state_store: BaseAuditStateStore):
        self.state_store = state_store

    def publish_audit_job(self, record: AuditJobRecord, claimed_fee_bps: float = 5.0) -> str:
        record.update_stage(AuditStage.QUEUED, progress_pct=10)
        self.state_store.update_audit(record)

        thread = threading.Thread(
            target=self._run_local_worker,
            args=(record, claimed_fee_bps),
            daemon=True
        )
        thread.start()
        return f"local-msg-{record.audit_id}"

    def _run_local_worker(self, record: AuditJobRecord, claimed_fee_bps: float):
        try:
            record.update_stage(AuditStage.RUNNING, progress_pct=25)
            self.state_store.update_audit(record)

            record.update_stage(AuditStage.INVESTIGATING, progress_pct=50)
            self.state_store.update_audit(record)

            record.update_stage(AuditStage.VERIFYING, progress_pct=75)
            self.state_store.update_audit(record)

            result = AuditWorker.execute_audit(
                project_name=record.project_name,
                repo_path=record.repo_path,
                data_file=record.data_file,
                report_file=record.report_file,
                claimed_fee_bps=claimed_fee_bps,
                audit_id=record.audit_id
            )

            record.update_stage(AuditStage.REPORTING, progress_pct=90)
            record.result = result
            record.update_stage(AuditStage.COMPLETED, progress_pct=100)
            self.state_store.update_audit(record)

        except Exception as e:
            logger.error(f"Worker failure for audit {record.audit_id}: {e}")
            record.record_failure(str(e))
            self.state_store.update_audit(record)


class GCPPubSubPublisher(BaseAuditJobPublisher):
    """Real Google Cloud Pub/Sub publisher for Cloud Run production environment."""

    def __init__(self, project_id: Optional[str] = None, topic_name: Optional[str] = None):
        from google.cloud import pubsub_v1
        self.project_id = project_id or settings.GCP_PROJECT_ID
        self.topic_name = topic_name or settings.PUBSUB_TOPIC
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_name)

    def publish_audit_job(self, record: AuditJobRecord, claimed_fee_bps: float = 5.0) -> str:
        # Minimal metadata message schema (NO secrets, NO source code)
        message_data = {
            "audit_id": record.audit_id,
            "project_name": record.project_name,
            "repo_path": record.repo_path,
            "data_file": record.data_file,
            "report_file": record.report_file,
            "claimed_fee_bps": claimed_fee_bps,
            "created_at": record.created_at
        }
        
        payload_bytes = json.dumps(message_data).encode("utf-8")
        future = self.publisher.publish(self.topic_path, payload_bytes)
        message_id = future.result()
        logger.info(f"Published audit {record.audit_id} to Pub/Sub topic {self.topic_path} with message_id: {message_id}")
        return message_id


def get_audit_publisher(state_store: BaseAuditStateStore) -> BaseAuditJobPublisher:
    """Returns the configured publisher based on runtime mode."""
    if settings.is_gcp_runtime():
        try:
            return GCPPubSubPublisher()
        except Exception as e:
            logger.warning(f"Falling back to LocalThreadPublisher due to GCP init error: {e}")
            return LocalThreadPublisher(state_store)
    return LocalThreadPublisher(state_store)
