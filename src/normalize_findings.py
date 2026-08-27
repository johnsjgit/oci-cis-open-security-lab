"""Normalize safe sample security findings for the OCI CIS Open Security Lab."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

TOOL_MAPPINGS = {
    "lynis": {"domain": "host-hardening", "control": "CIS Control 4", "oci_service": "OCI Logging"},
    "openscap": {"domain": "baseline-assessment", "control": "CIS Control 4", "oci_service": "OCI Logging"},
    "trivy": {"domain": "workload-vulnerability", "control": "CIS Control 7", "oci_service": "OCI Cloud Guard"},
    "wazuh": {"domain": "security-monitoring", "control": "CIS Control 8", "oci_service": "OCI Cloud Guard"},
}


def normalize(finding: dict[str, Any]) -> dict[str, Any]:
    """Convert one tool finding into a portable evidence record."""
    tool = str(finding.get("tool", "unknown")).lower()
    mapping = TOOL_MAPPINGS.get(tool, {"domain": "unclassified", "control": "Unmapped", "oci_service": "Manual review"})
    return {
        "asset": finding.get("asset", "unknown-asset"),
        "tool": tool,
        "severity": finding.get("severity", "unknown"),
        "status": finding.get("status", "open"),
        "summary": finding.get("summary", "No summary provided."),
        "security_domain": mapping["domain"],
        "control_reference": mapping["control"],
        "recommended_oci_context": mapping["oci_service"],
        "requires_human_review": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to a findings JSON document")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        findings = payload.get("findings", [])
        if not isinstance(findings, list):
            raise ValueError("findings must be a JSON list")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))

    report = {
        "report_type": "oci-cis-open-security-lab",
        "finding_count": len(findings),
        "findings": [normalize(item) for item in findings if isinstance(item, dict)],
        "notice": "Sample output only. No OCI API calls or remediation actions were performed.",
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
