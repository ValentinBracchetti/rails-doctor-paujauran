#!/usr/bin/env python3
"""Parse bundle-audit text output into structured CVEs."""
import argparse
import json
import re
import sys
from pathlib import Path


def parse_bundle_audit(input_path: Path) -> dict:
    """Parse bundler_audit.txt and return structured advisories."""
    if not input_path.exists():
        return {"tool": "bundler-audit", "total_advisories": 0, "findings": []}

    text = input_path.read_text(encoding="utf-8", errors="replace")
    findings = []
    current = {}

    for line in text.splitlines():
        line = line.strip()
        if not line:
            if current:
                findings.append(_build_finding(current))
                current = {}
            continue
        if line.startswith("Name:"):
            current["gem"] = line.split(":", 1)[1].strip()
        elif line.startswith("Version:"):
            current["installed_version"] = line.split(":", 1)[1].strip()
        elif line.startswith("CVE:") or line.startswith("Advisory:"):
            current["cve"] = line.split(":", 1)[1].strip()
        elif line.startswith("GHSA:"):
            current["ghsa"] = line.split(":", 1)[1].strip()
        elif line.startswith("Criticality:"):
            crit = line.split(":", 1)[1].strip().lower()
            current["severity"] = "critical" if crit == "critical" else "major" if crit == "high" else "minor"
        elif line.startswith("URL:"):
            current["url"] = line.split(":", 1)[1].strip()
        elif line.startswith("Title:"):
            current["title"] = line.split(":", 1)[1].strip()
        elif line.startswith("Solution:"):
            sol = line.split(":", 1)[1].strip()
            current["patched_versions"] = [sol]
            current["recommendation"] = f"Mettre à jour {current.get('gem', '')} vers {sol}"

    if current:
        findings.append(_build_finding(current))

    return {
        "tool": "bundler-audit",
        "total_advisories": len(findings),
        "findings": findings,
    }


def _build_finding(c: dict) -> dict:
    return {
        "id": c.get("cve", c.get("ghsa", "UNKNOWN")),
        "gem": c.get("gem", ""),
        "installed_version": c.get("installed_version", ""),
        "patched_versions": c.get("patched_versions", []),
        "severity": c.get("severity", "major"),
        "title": c.get("title", ""),
        "url": c.get("url", ""),
        "recommendation": c.get("recommendation", ""),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="Path to bundler_audit.txt")
    parser.add_argument("--output", required=True, type=Path, help="Output JSON path")
    args = parser.parse_args()

    result = parse_bundle_audit(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Parsed {result['total_advisories']} bundle-audit advisories -> {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
