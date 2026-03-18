#!/usr/bin/env bash
# Rails Doctor - Orchestrateur d'audit
# Usage: ./run_audit.sh <chemin_projet> [dossier_sortie]

set -e

PROJECT_PATH="${1:-.}"
OUTPUT_DIR="${2:-/tmp/rails-doctor-raw}"
OUTPUT_DIR="$(cd "$(dirname "$OUTPUT_DIR")" 2>/dev/null && pwd)/$(basename "$OUTPUT_DIR")" || true

mkdir -p "$OUTPUT_DIR"
ERRORS_LOG="$OUTPUT_DIR/errors.log"
: > "$ERRORS_LOG"

echo "Rails Doctor - Audit de $PROJECT_PATH"
echo "Sortie: $OUTPUT_DIR"
echo ""

# Vérifier projet Rails valide
if [[ ! -f "$PROJECT_PATH/Gemfile" ]] || [[ ! -f "$PROJECT_PATH/config/application.rb" ]]; then
  echo "Erreur: $PROJECT_PATH n'est pas un projet Rails valide (Gemfile ou config/application.rb manquant)"
  exit 2
fi

cd "$PROJECT_PATH"

# Métadonnées
RAILS_VERSION=$(bundle exec rails -v 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
RUBY_VERSION=$(ruby -v | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
START_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Brakeman
echo "[1/6] Brakeman..."
if bundle exec brakeman -q -f json -o "$OUTPUT_DIR/brakeman_report.json" --no-pager . 2>>"$ERRORS_LOG"; then
  echo "  OK"
else
  echo "  ECHEC (voir errors.log)" >> "$ERRORS_LOG"
fi

# bundle-audit
echo "[2/6] bundle-audit..."
if bundle exec bundle-audit check --update 2>"$OUTPUT_DIR/bundler_audit.txt"; then
  echo "  OK (0 vulnérabilités)"
else
  echo "  OK (vulnérabilités trouvées, voir bundler_audit.txt)"
fi

# RuboCop
echo "[3/6] RuboCop..."
if bundle exec rubocop --format json --out "$OUTPUT_DIR/rubocop_report.json" app lib 2>>"$ERRORS_LOG"; then
  echo "  OK"
else
  echo "  OK (offenses trouvées)"
fi

# Reek
echo "[4/6] Reek..."
if command -v reek &>/dev/null; then
  reek --format json app 2>>"$ERRORS_LOG" > "$OUTPUT_DIR/reek_report.json" || true
  echo "  OK"
else
  gem install reek --no-document 2>/dev/null
  reek --format json app 2>>"$ERRORS_LOG" > "$OUTPUT_DIR/reek_report.json" || true
  echo "  OK"
fi

# Flog
echo "[5/6] Flog..."
if command -v flog &>/dev/null; then
  flog app --all 2>>"$ERRORS_LOG" | head -80 > "$OUTPUT_DIR/flog_report.txt" || true
  echo "  OK"
else
  gem install flog --no-document 2>/dev/null
  flog app --all 2>>"$ERRORS_LOG" | head -80 > "$OUTPUT_DIR/flog_report.txt" || true
  echo "  OK"
fi

# rails_best_practices
echo "[6/6] rails_best_practices..."
if command -v rails_best_practices &>/dev/null; then
  rails_best_practices . --format json --output-file "$OUTPUT_DIR/rbp_report.json" 2>>"$ERRORS_LOG" || true
  echo "  OK"
else
  gem install rails_best_practices --no-document 2>/dev/null
  rails_best_practices . --format json --output-file "$OUTPUT_DIR/rbp_report.json" 2>>"$ERRORS_LOG" || true
  echo "  OK"
fi

END_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat > "$OUTPUT_DIR/audit_metadata.json" << EOF
{
  "timestamp_start": "$START_TIME",
  "timestamp_end": "$END_TIME",
  "rails_version": "$RAILS_VERSION",
  "ruby_version": "$RUBY_VERSION",
  "project_path": "$PROJECT_PATH"
}
EOF

echo ""
echo "Audit terminé. Rapports dans $OUTPUT_DIR"
exit 0
