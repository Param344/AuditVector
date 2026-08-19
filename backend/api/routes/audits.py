"""Audit API Routes for Cloud Run & Local Runtime."""

import os
import json
import base64
import uuid
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from ...cloud.firestore.audit_state import get_audit_state_store, AuditStage
from ...cloud.pubsub.publisher import get_audit_publisher
from ...cloud.pubsub.worker import PubSubAuditWorker
from ...agents.report_agent import ReportAgent

router = APIRouter(prefix="/api/audits", tags=["Audits"])

# Configured state store and publisher
state_store = get_audit_state_store()
publisher = get_audit_publisher(state_store)

# Base repo paths for presets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
INTEGRITYLAB_DIR = os.path.join(BASE_DIR, "integritylab")


class CreateAuditRequest(BaseModel):
    project_name: str
    repo_path: str
    data_file: str
    report_file: str
    claimed_fee_bps: Optional[float] = 5.0


@router.post("")
def create_audit(req: CreateAuditRequest):
    audit_id = f"audit-{uuid.uuid4().hex[:8]}"
    record = state_store.create_audit(
        audit_id=audit_id,
        project_name=req.project_name,
        repo_path=req.repo_path,
        data_file=req.data_file,
        report_file=req.report_file
    )
    
    # Dispatch via Pub/Sub or local thread
    publisher.publish_audit_job(record, claimed_fee_bps=req.claimed_fee_bps or 5.0)
    
    return {"audit_id": audit_id, "status": "QUEUED", "message": "Audit dispatched to async queue"}


@router.get("")
def list_audits():
    return state_store.list_audits()


@router.get("/{audit_id}")
def get_audit(audit_id: str):
    record = state_store.get_audit(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail="Audit not found")
    return record.to_dict()


@router.get("/{audit_id}/report")
def get_audit_report_markdown(audit_id: str):
    record = state_store.get_audit(audit_id)
    if not record:
        raise HTTPException(status_code=404, detail="Audit not found")
    if not record.result:
        raise HTTPException(status_code=400, detail="Audit is still in progress")
    md = ReportAgent.render_markdown(record.result["report"])
    return {"audit_id": audit_id, "markdown": md}


@router.post("/demo/alpha")
def trigger_demo_alpha():
    """Preset trigger for IntegrityLab Alpha failure audit."""
    repo_path = os.path.join(INTEGRITYLAB_DIR, "source")
    data_file = os.path.join(INTEGRITYLAB_DIR, "data", "trades_alpha_failure.csv")
    report_file = os.path.join(INTEGRITYLAB_DIR, "reports", "alpha_performance_report.json")
    
    audit_id = f"audit-{uuid.uuid4().hex[:8]}"
    record = state_store.create_audit(
        audit_id=audit_id,
        project_name="IntegrityLab-Alpha",
        repo_path=repo_path,
        data_file=data_file,
        report_file=report_file
    )
    publisher.publish_audit_job(record, claimed_fee_bps=5.0)
    return {"audit_id": audit_id, "demo": "Alpha Failure Test Fixture", "status": "QUEUED"}


@router.post("/demo/control")
def trigger_demo_control():
    """Preset trigger for IntegrityLab Control case audit."""
    repo_path = os.path.join(INTEGRITYLAB_DIR, "source")
    data_file = os.path.join(INTEGRITYLAB_DIR, "data", "trades_control_case.csv")
    report_file = os.path.join(INTEGRITYLAB_DIR, "reports", "control_performance_report.json")
    
    audit_id = f"audit-{uuid.uuid4().hex[:8]}"
    record = state_store.create_audit(
        audit_id=audit_id,
        project_name="IntegrityLab-Control",
        repo_path=repo_path,
        data_file=data_file,
        report_file=report_file
    )
    publisher.publish_audit_job(record, claimed_fee_bps=5.0)
    return {"audit_id": audit_id, "demo": "Control Case Clean Fixture", "status": "QUEUED"}


@router.post("/pubsub/push")
async def handle_pubsub_push(request: Request):
    """Webhook endpoint for receiving Google Cloud Pub/Sub push subscription messages on Cloud Run."""
    body = await request.json()
    message = body.get("message", {})
    data_b64 = message.get("data")
    
    if not data_b64:
        raise HTTPException(status_code=400, detail="Invalid Pub/Sub message payload")
        
    data_str = base64.b64decode(data_b64).decode("utf-8")
    payload = json.loads(data_str)
    
    success = PubSubAuditWorker.process_message(payload, state_store)
    if not success:
        raise HTTPException(status_code=500, detail="Worker processing failed")
        
    return {"status": "SUCCESS", "audit_id": payload.get("audit_id")}
