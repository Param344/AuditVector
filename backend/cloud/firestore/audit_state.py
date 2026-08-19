"""Persistent & In-Memory Audit State Management for Google Cloud Firestore and Local Execution."""

import datetime
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, Optional, List
from ...config.settings import settings


class AuditStage(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    INVESTIGATING = "INVESTIGATING"
    VERIFYING = "VERIFYING"
    REPORTING = "REPORTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AuditJobRecord:
    def __init__(
        self,
        audit_id: str,
        project_name: str,
        repo_path: str,
        data_file: str,
        report_file: str,
        stage: AuditStage = AuditStage.CREATED,
        progress_pct: int = 0,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        retry_count: int = 0
    ):
        self.audit_id = audit_id
        self.project_name = project_name
        self.repo_path = repo_path
        self.data_file = data_file
        self.report_file = report_file
        self.stage = stage
        self.progress_pct = progress_pct
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.updated_at = updated_at or self.created_at
        self.result = result
        self.error = error
        self.retry_count = retry_count

    def update_stage(self, stage: AuditStage, progress_pct: int = 0):
        self.stage = stage
        self.progress_pct = progress_pct
        self.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    def record_failure(self, error_message: str):
        self.stage = AuditStage.FAILED
        self.error = error_message
        self.retry_count += 1
        self.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "project_name": self.project_name,
            "repo_path": self.repo_path,
            "data_file": self.data_file,
            "report_file": self.report_file,
            "stage": self.stage.value if isinstance(self.stage, AuditStage) else self.stage,
            "progress_pct": self.progress_pct,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "result": self.result,
            "error": self.error,
            "retry_count": self.retry_count
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditJobRecord":
        return cls(
            audit_id=data["audit_id"],
            project_name=data.get("project_name", "Unknown"),
            repo_path=data.get("repo_path", ""),
            data_file=data.get("data_file", ""),
            report_file=data.get("report_file", ""),
            stage=AuditStage(data.get("stage", AuditStage.CREATED)),
            progress_pct=data.get("progress_pct", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            result=data.get("result"),
            error=data.get("error"),
            retry_count=data.get("retry_count", 0)
        )


class BaseAuditStateStore(ABC):
    """Abstract interface for audit state storage."""

    @abstractmethod
    def create_audit(self, audit_id: str, project_name: str, repo_path: str, data_file: str, report_file: str) -> AuditJobRecord:
        pass

    @abstractmethod
    def get_audit(self, audit_id: str) -> Optional[AuditJobRecord]:
        pass

    @abstractmethod
    def update_audit(self, record: AuditJobRecord):
        pass

    @abstractmethod
    def list_audits(self) -> List[Dict[str, Any]]:
        pass


class InMemoryAuditStateStore(BaseAuditStateStore):
    """In-memory audit state store for local development and hermetic CI testing."""

    def __init__(self):
        self._audits: Dict[str, AuditJobRecord] = {}

    def create_audit(self, audit_id: str, project_name: str, repo_path: str, data_file: str, report_file: str) -> AuditJobRecord:
        record = AuditJobRecord(audit_id, project_name, repo_path, data_file, report_file)
        self._audits[audit_id] = record
        return record

    def get_audit(self, audit_id: str) -> Optional[AuditJobRecord]:
        return self._audits.get(audit_id)

    def update_audit(self, record: AuditJobRecord):
        self._audits[record.audit_id] = record

    def list_audits(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self._audits.values()]


class FirestoreAuditStateStore(BaseAuditStateStore):
    """Real Google Cloud Firestore persistent state backend."""

    def __init__(self, project_id: Optional[str] = None, collection_name: Optional[str] = None):
        from google.cloud import firestore
        self.project_id = project_id or settings.GCP_PROJECT_ID
        self.collection_name = collection_name or settings.FIRESTORE_COLLECTION
        self.db = firestore.Client(project=self.project_id)

    def create_audit(self, audit_id: str, project_name: str, repo_path: str, data_file: str, report_file: str) -> AuditJobRecord:
        record = AuditJobRecord(audit_id, project_name, repo_path, data_file, report_file)
        doc_ref = self.db.collection(self.collection_name).document(audit_id)
        doc_ref.set(record.to_dict())
        return record

    def get_audit(self, audit_id: str) -> Optional[AuditJobRecord]:
        doc_ref = self.db.collection(self.collection_name).document(audit_id)
        doc = doc_ref.get()
        if not doc.exists:
            return None
        return AuditJobRecord.from_dict(doc.to_dict())

    def update_audit(self, record: AuditJobRecord):
        doc_ref = self.db.collection(self.collection_name).document(record.audit_id)
        doc_ref.set(record.to_dict(), merge=True)

    def list_audits(self) -> List[Dict[str, Any]]:
        docs = self.db.collection(self.collection_name).stream()
        return [doc.to_dict() for doc in docs]


# Factory selector
def get_audit_state_store() -> BaseAuditStateStore:
    """Returns the appropriate state store based on runtime configuration."""
    if settings.is_gcp_runtime():
        try:
            return FirestoreAuditStateStore()
        except Exception:
            # Fallback to in-memory if GCP credentials unavailable
            return InMemoryAuditStateStore()
    return InMemoryAuditStateStore()


# Compatibility alias for existing code
AuditStateManager = InMemoryAuditStateStore
