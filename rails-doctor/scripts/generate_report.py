#!/usr/bin/env python3
"""
Generate Rails Doctor report from findings JSON files.
Usage: python generate_report.py --findings-dir ./rails-doctor --templates-dir ./templates --output-dir ./rails-doctor-report
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def calculate_score(findings: dict) -> dict:
    """Calculate health score per domain (simplified)."""
    security = 30
    quality = 20
    perf = 20
    arch = 20
    deps = 10

    # Apply penalties from findings (simplified)
    brakeman = findings.get("brakeman_parsed", {})
    for f in brakeman.get("findings", []):
        s = f.get("severity", "")
        if s == "critical":
            security -= 10
        elif s == "major":
            security -= 5
        elif s == "minor":
            security -= 2

    bundle_audit = findings.get("bundle_audit_parsed", {})
    for f in bundle_audit.get("findings", []):
        security -= 3
        deps -= 2

    security = max(0, security)
    deps = max(0, deps)

    return {
        "security": security,
        "quality": quality,
        "performance": perf,
        "architecture": arch,
        "dependencies": deps,
        "total": security + quality + perf + arch + deps,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--findings-dir", type=Path, default=Path("rails-doctor"))
    parser.add_argument("--templates-dir", type=Path, default=Path("templates"))
    parser.add_argument("--output-dir", type=Path, default=Path("rails-doctor-report"))
    parser.add_argument("--project-profile", type=Path, default=None)
    args = parser.parse_args()

    findings_dir = args.findings_dir
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load findings
    brakeman_raw = load_json(findings_dir / "brakeman_report.json")
    bundle_audit_txt = (findings_dir / "bundler_audit.txt").read_text(encoding="utf-8", errors="replace") if (findings_dir / "bundler_audit.txt").exists() else ""
    rubocop = load_json(findings_dir / "rubocop_report.json")
    reek = load_json(findings_dir / "reek_report.json")
    rbp = load_json(findings_dir / "rbp_report.json")

    # Parse brakeman if we have parse script
    brakeman_parsed = {"findings": []}
    if brakeman_raw and "warnings" in brakeman_raw:
        for i, w in enumerate(brakeman_raw["warnings"], 1):
            conf = w.get("confidence", "Weak")
            sev = "critical" if conf == "High" else "major" if conf == "Medium" else "minor"
            brakeman_parsed["findings"].append({
                "id": f"BRAK-{i:03d}",
                "severity": sev,
                "file": w.get("file", ""),
                "line": w.get("line", 0),
                "message": w.get("message", ""),
            })

    findings = {
        "brakeman_parsed": brakeman_parsed,
        "bundle_audit_parsed": {"findings": []},  # Would need parse_bundle_audit
    }

    score = calculate_score(findings)
    date_str = datetime.now().strftime("%d %B %Y")

    # Create minimal 00_project_profile if not exists
    profile_path = output_dir / "00_project_profile.md"
    if not profile_path.exists():
        profile_path.write_text(f"""# Rails Doctor — Profil du Projet

**Date de l'audit** : {date_str}
**Projet** : pjr-rails

## Score santé : {score['total']}/100

*Généré par generate_report.py. Exécutez la Phase 1 Discovery pour un profil complet.*
""", encoding="utf-8")

    print(f"Score calculé: {score['total']}/100")
    print(f"Rapports dans {output_dir}")
    print("Note: Les rapports 01-06 ont été générés manuellement. Ce script fournit une base pour automatisation future.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
