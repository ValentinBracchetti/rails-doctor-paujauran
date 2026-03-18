#!/usr/bin/env python3
"""Detect Rails anti-patterns via static analysis."""
import argparse
import json
import re
import sys
from pathlib import Path


def count_lines(path: Path) -> int:
    return len(path.read_text(encoding="utf-8", errors="replace").splitlines())


def count_public_methods(path: Path) -> int:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        return len(re.findall(r"^\s+def\s+(\w+)\s*[^(]*\([^)]*\)", content, re.MULTILINE))
    except Exception:
        return 0


def count_callbacks(path: Path) -> int:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        return len(re.findall(r"^\s+(?:before_|after_|around_)\w+", content, re.MULTILINE))
    except Exception:
        return 0


def has_default_scope(path: Path) -> bool:
    try:
        return "default_scope" in path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False


def count_methods_total(path: Path) -> int:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        return len(re.findall(r"^\s+def\s+\w+", content, re.MULTILINE))
    except Exception:
        return 0


def detect_antipatterns(project_path: Path) -> dict:
    findings = []
    models_dir = project_path / "app" / "models"
    controllers_dir = project_path / "app" / "controllers"
    views_dir = project_path / "app" / "views"

    if not project_path.exists():
        return {"tool": "antipattern_detector", "total_findings": 0, "findings": []}

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(project_path))
        except ValueError:
            return str(p)

    # AP-001 Fat Model
    for rb in models_dir.rglob("*.rb") if models_dir.exists() else []:
        if "concern" in str(rb).lower():
            continue
        lines = count_lines(rb)
        methods = count_public_methods(rb)
        if lines > 300 or methods > 20:
            findings.append({
                "id": "AP-001",
                "pattern": "Fat Model",
                "severity": "major",
                "file": rel(rb),
                "detail": f"Model has {lines} lines and {methods} public methods",
                "recommendation": "Extraire la logique en Service Objects et Concerns ciblés",
            })

    # AP-002 Fat Controller
    for rb in controllers_dir.rglob("*.rb") if controllers_dir.exists() else []:
        if "concern" in str(rb).lower():
            continue
        lines = count_lines(rb)
        if lines > 200:
            findings.append({
                "id": "AP-002",
                "pattern": "Fat Controller",
                "severity": "major",
                "file": rel(rb),
                "detail": f"Controller has {lines} lines",
                "recommendation": "Extraire la logique en Services et déléguer",
            })

    # AP-003 Callback Hell
    for rb in models_dir.rglob("*.rb") if models_dir.exists() else []:
        cbs = count_callbacks(rb)
        if cbs > 5:
            findings.append({
                "id": "AP-003",
                "pattern": "Callback Hell",
                "severity": "major",
                "file": rel(rb),
                "detail": f"Model has {cbs} callbacks",
                "recommendation": "Réduire les callbacks, privilégier des services explicites",
            })

    # AP-004 default_scope
    for rb in models_dir.rglob("*.rb") if models_dir.exists() else []:
        if has_default_scope(rb):
            findings.append({
                "id": "AP-004",
                "pattern": "default_scope",
                "severity": "major",
                "file": rel(rb),
                "detail": "default_scope utilisé (presque toujours un anti-pattern)",
                "recommendation": "Remplacer par des scopes explicites",
            })

    # AP-007 God Object
    for rb in models_dir.rglob("*.rb") if models_dir.exists() else []:
        if "concern" in str(rb).lower():
            continue
        total = count_methods_total(rb)
        if total > 50:
            findings.append({
                "id": "AP-007",
                "pattern": "God Object",
                "severity": "critical",
                "file": rel(rb),
                "detail": f"Model has {total} methods",
                "recommendation": "Décomposer en plusieurs classes et concerns",
            })

    return {
        "tool": "antipattern_detector",
        "total_findings": len(findings),
        "findings": findings,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-path", required=True, type=Path, help="Path to Rails project")
    parser.add_argument("--output", required=True, type=Path, help="Output JSON path")
    args = parser.parse_args()

    result = detect_antipatterns(args.project_path)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Detected {result['total_findings']} anti-patterns -> {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
