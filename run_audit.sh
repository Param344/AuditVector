#!/usr/bin/env bash
# AuditVector CLI Runner

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$DIR/.venv/bin/python"

if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

DEMO_TYPE=""
REPO_PATH="$DIR/integritylab/source"
DATA_FILE="$DIR/integritylab/data/trades_alpha_failure.csv"
REPORT_FILE="$DIR/integritylab/reports/alpha_performance_report.json"
PROJECT_NAME="IntegrityLab-Alpha"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --demo)
            DEMO_TYPE="$2"
            shift 2
            ;;
        --repo)
            REPO_PATH="$2"
            shift 2
            ;;
        --data)
            DATA_FILE="$2"
            shift 2
            ;;
        --report)
            REPORT_FILE="$2"
            shift 2
            ;;
        --project)
            PROJECT_NAME="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: ./run_audit.sh [--demo alpha|control] [--repo <path>] [--data <path>] [--report <path>]"
            exit 1
            ;;
    esac
done

if [ "$DEMO_TYPE" == "control" ]; then
    DATA_FILE="$DIR/integritylab/data/trades_control_case.csv"
    REPORT_FILE="$DIR/integritylab/reports/control_performance_report.json"
    PROJECT_NAME="IntegrityLab-Control"
fi

echo "============================================================"
echo " AUDITVECTOR — AUTONOMOUS FINANCIAL INTEGRITY AGENT"
echo " Tagline: AI reasons. Code proves. Evidence explains."
echo "============================================================"
echo "Project: $PROJECT_NAME"
echo "Source:  $REPO_PATH"
echo "Dataset: $DATA_FILE"
echo "Report:  $REPORT_FILE"
echo "------------------------------------------------------------"

"$PYTHON_BIN" -c "
import sys
from backend.adk.runner import ADKRunner
from backend.agents.report_agent import ReportAgent

res = ADKRunner.run_audit(
    audit_id='cli-run',
    project_name='$PROJECT_NAME',
    repo_path='$REPO_PATH',
    data_file='$DATA_FILE',
    report_file='$REPORT_FILE'
)

print(ReportAgent.render_markdown(res['report']))
print('\n[Execution Status: ' + res['status'] + ' | Mode: ' + res['mode'] + ' | Duration: ' + str(res['duration_seconds']) + 's]')
"
