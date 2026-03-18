# Rails Doctor — Scripts d'audit

Ce dossier contient les scripts et résultats bruts de l'audit Rails Doctor.

## Structure

- `scripts/` — Scripts d'analyse :
  - `run_audit.sh` — Orchestrateur (Brakeman, bundle-audit, RuboCop, Reek, Flog, rails_best_practices)
  - `parse_brakeman.py` — Parse le JSON Brakeman
  - `parse_bundle_audit.py` — Parse la sortie bundle-audit
  - `detect_antipatterns.py` — Détection anti-patterns (Fat Model, Callback Hell, etc.)
  - `generate_report.py` — Génération des rapports (base pour automatisation)
- Rapports générés dans `../rails-doctor-report/`
