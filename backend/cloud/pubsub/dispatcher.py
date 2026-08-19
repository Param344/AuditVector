"""Asynchronous Pub/Sub Job Dispatcher Boundary."""

import threading
import uuid
from typing import Dict, Any
from ..firestore.audit_state import AuditStateManager, AuditStage
from ...workers.audit_worker import AuditWorker


class PubSubJobDispatcher:
    """Dispatches background audit jobs cleanly at the job boundary."""

    def __init__(self, state_manager: AuditStateManager):
        self.state_manager = state_manager

    def dispatch_audit_job(
        self,
        project_name: str,
        repo_path: str,
        data_file: str,
        report_file: str,
        claimed_fee_bps: float = 5.0
    ) -> str:
        audit_id = f"audit-{uuid.uuid4().hex[:8]}"
        record = self.state_manager.create_audit(
            audit_id=audit_id,
            project_name=project_name,
            repo_path=repo_path,
            data_file=data_file,
            report_file=report_file
        )
        record.update_stage(AuditStage.QUEUED, progress_pct=10)

        # Run background worker thread (simulating Pub/Sub Cloud Run worker invocation)
        worker_thread = threading.Thread(
            target=self._worker_execution_loop,
            args=(record, claimed_fee_bps),
            daemon=True
        )
        worker_thread.start()

        return audit_id

    def _worker_execution_loop(self, record, claimed_fee_bps: float):
        try:
            record.update_stage(AuditStage.RUNNING, progress_pct=25)
            
            record.update_stage(AuditStage.INVESTIGATING, progress_pct=50)

            record.update_stage(AuditStage.VERIFYING, progress_pct=75)

            # Execute full audit worker
            result = AuditWorker.execute_audit(
                project_name=record.project_name,
                repo_path=record.repo_path,
                data_file=record.data_file,
                report_file=record.report_file,
                claimed_fee_bps=claimed_fee_bps
            )

            record.update_stage(AuditStage.REPORTING, progress_pct=90)
            record.result = result
            record.update_stage(AuditStage.COMPLETED, progress_pct=100)

        except Exception as e:
            record.error = str(e)
            record.update_stage(AuditStage.FAILED, progress_pct=100)
