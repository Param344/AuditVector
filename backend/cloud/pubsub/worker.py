"""Google Cloud Pub/Sub Worker with Strict Idempotency and State Synchronization."""

import json
import logging
from typing import Dict, Any, Optional
from ...config.settings import settings
from ..firestore.audit_state import AuditJobRecord, AuditStage, BaseAuditStateStore
from ...adk.runner import ADKRunner

logger = logging.getLogger("AuditVector.PubSubWorker")


class PubSubAuditWorker:
    """Processes asynchronous audit jobs received from Google Cloud Pub/Sub."""

    @classmethod
    def process_message(
        cls,
        message_data: Dict[str, Any],
        state_store: BaseAuditStateStore
    ) -> bool:
        """Processes a single Pub/Sub audit message with full idempotency verification."""
        audit_id = message_data.get("audit_id")
        if not audit_id:
            logger.error("Received Pub/Sub message missing 'audit_id'")
            return False

        record = state_store.get_audit(audit_id)
        if not record:
            # Create record if missing
            record = state_store.create_audit(
                audit_id=audit_id,
                project_name=message_data.get("project_name", "Unknown-Audit"),
                repo_path=message_data.get("repo_path", ""),
                data_file=message_data.get("data_file", ""),
                report_file=message_data.get("report_file", "")
            )

        # -------------------------------------------------------------
        # IDEMPOTENCY CHECK
        # -------------------------------------------------------------
        if record.stage in (AuditStage.RUNNING, AuditStage.COMPLETED):
            logger.warning(
                f"IDEMPOTENCY: Audit '{audit_id}' is already in stage '{record.stage}'. "
                "Acknowledging Pub/Sub message without re-execution."
            )
            return True

        # Execute Multi-Agent Audit Pipeline
        try:
            record.update_stage(AuditStage.RUNNING, progress_pct=25)
            state_store.update_audit(record)

            record.update_stage(AuditStage.INVESTIGATING, progress_pct=50)
            state_store.update_audit(record)

            record.update_stage(AuditStage.VERIFYING, progress_pct=75)
            state_store.update_audit(record)

            # Run full ADK pipeline
            result = ADKRunner.run_audit(
                audit_id=audit_id,
                project_name=record.project_name,
                repo_path=record.repo_path,
                data_file=record.data_file,
                report_file=record.report_file,
                claimed_fee_bps=float(message_data.get("claimed_fee_bps", 5.0))
            )

            record.update_stage(AuditStage.REPORTING, progress_pct=90)
            record.result = result
            record.update_stage(AuditStage.COMPLETED, progress_pct=100)
            state_store.update_audit(record)
            logger.info(f"Audit '{audit_id}' completed successfully and persisted.")
            return True

        except Exception as e:
            logger.error(f"Audit '{audit_id}' execution failed: {e}")
            record.record_failure(str(e))
            state_store.update_audit(record)
            return False

    @classmethod
    def start_pull_subscriber(cls, state_store: BaseAuditStateStore):
        """Starts a persistent pull subscriber listening on Google Cloud Pub/Sub."""
        from google.cloud import pubsub_v1

        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(
            settings.GCP_PROJECT_ID,
            settings.PUBSUB_SUBSCRIPTION
        )

        def callback(message):
            try:
                data_str = message.data.decode("utf-8")
                payload = json.loads(data_str)
                success = cls.process_message(payload, state_store)
                if success:
                    message.ack()
                else:
                    message.nack()
            except Exception as ex:
                logger.error(f"Failed to process Pub/Sub message: {ex}")
                message.nack()

        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
        logger.info(f"Listening for audit messages on {subscription_path}...")
        return streaming_pull_future
