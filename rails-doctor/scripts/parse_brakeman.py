#!/usr/bin/env python3
"""Parse Brakeman JSON report into structured findings."""
import argparse
import json
import sys
from pathlib import Path

SEVERITY_MAP = {"High": "critical", "Medium": "major", "Weak": "minor"}


def parse_brakeman(input_path: Path) -> dict:
    """Parse brakeman_report.json and return structured data."""
    if not input_path.exists():
        return {"tool": "brakeman", "total_warnings": 0, "by_severity": {}, "by_type": {}, "findings": []}

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    findings = []
    by_severity = {"critical": 0, "major": 0, "minor": 0}
    by_type = {}

    for i, w in enumerate(data.get("warnings", []), 1):
        conf = w.get("confidence", "Weak")
        severity = SEVERITY_MAP.get(conf, "minor")
        by_severity[severity] = by_severity.get(severity, 0) + 1

        wtype = w.get("warning_type", "Unknown")
        by_type[wtype] = by_type.get(wtype, 0) + 1

        findings.append({
            "id": f"BRAK-{i:03d}",
            "type": wtype,
            "severity": severity,
            "confidence": conf,
            "file": w.get("file", ""),
            "line": w.get("line", 0),
            "message": w.get("message", ""),
            "code_snippet": w.get("code", ""),
            "recommendation": w.get("link", ""),
            "reference_url": w.get("link", ""),
        })

    return {
        "tool": "brakeman",
        "total_warnings": len(findings),
        "by_severity": by_severity,
        "by_type": by_type,
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="Path to brakeman_report.json")
    parser.add_argument("--output", required=True, type=Path, help="Output JSON path")
    args = parser.parse_args()

    result = parse_brakeman(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Parsed {result['total_warnings']} Brakeman warnings -> {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
