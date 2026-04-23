#!/usr/bin/env bash
# docs-organizer diagnose script
# Scans docs/ directory and reports compliance issues
# Usage: bash diagnose.sh [docs_path] [--config path/to/config.yaml]

set -euo pipefail

DOCS_PATH="${1:-docs}"
CONFIG_PATH=""

# Parse arguments
for arg in "$@"; do
  case "$arg" in
    --config=*) CONFIG_PATH="${arg#--config=}" ;;
  esac
done

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Standard directories
STANDARD_DIRS="prd tech design handover research reports planning archive raw-source"

# Protected directories (from config or default)
PROTECTED_DIRS=""
if [[ -f "$CONFIG_PATH" ]]; then
  # Extract protected_dirs from yaml (simple grep, no yq dependency)
  PROTECTED_DIRS=$(grep -A 20 'protected_dirs:' "$CONFIG_PATH" | grep '^\s*-' | sed 's/^\s*- //' | tr '\n' ' ')
fi

# Counters
COMPLIANT=0
NONCOMPLIANT=0
PROTECTED=0

# Check if docs/ exists
if [[ ! -d "$DOCS_PATH" ]]; then
  echo -e "${RED}Error: $DOCS_PATH/ directory not found${NC}"
  exit 1
fi

echo "Scanning $DOCS_PATH/ ..."
echo ""

# Check for naming issues in a filename
check_naming() {
  local filename="$1"
  local issues=""

  # Check for spaces
  if [[ "$filename" =~ [[:space:]] ]]; then
    issues="${issues}contains-spaces "
  fi

  # Check for parentheses
  if [[ "$filename" =~ [\(\)\[\]] ]]; then
    issues="${issues}has-parens "
  fi

  # Check for uppercase (English part only)
  local basename="${filename%.*}"
  if [[ "$basename" =~ [A-Z] ]]; then
    # Allow Chinese characters mixed with English
    if ! [[ "$basename" =~ [^\x00-\x7F] ]]; then
      issues="${issues}has-uppercase "
    fi
  fi

  # Check for version suffixes
  if [[ "$filename" =~ v[0-9]+$ ]] || [[ "$filename" =~ [Ff]inal ]] || [[ "$filename" =~ 最新 ]]; then
    issues="${issues}has-version "
  fi

  # Check for underscores (non-code files)
  if [[ "$filename" =~ _ ]] && [[ "$filename" != *.ts ]] && [[ "$filename" != *.js ]] && [[ "$filename" != *.py ]]; then
    issues="${issues}has-underscores "
  fi

  echo "$issues"
}

# Determine expected directory based on filename pattern
guess_expected_dir() {
  local filename="$1"
  local basename="${filename%.*}"

  # tech/ patterns
  if [[ "$basename" == *-design ]] || [[ "$basename" == *-logic ]] || \
     [[ "$basename" == *-lesson ]] || [[ "$basename" == *-reference ]] || \
     [[ "$basename" == *-guide ]] || [[ "$basename" == *-setup ]] || \
     [[ "$basename" == database-* ]] || [[ "$basename" == data-fields-* ]]; then
    echo "tech"
    return
  fi

  # prd/ patterns
  if [[ "$basename" == *-requirements ]] || [[ "$basename" == *-spec ]]; then
    echo "prd"
    return
  fi

  # research/ patterns
  if [[ "$basename" == *-research ]] || [[ "$basename" == *-feasibility ]] || \
     [[ "$basename" == *-poc ]] || [[ "$basename" == *-analysis ]]; then
    echo "research"
    return
  fi

  # reports/ patterns
  if [[ "$basename" == *-code-review ]] || [[ "$basename" == *-progress-report ]]; then
    echo "reports"
    return
  fi

  # planning/ patterns
  if [[ "$basename" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}-.*-plan ]]; then
    echo "planning"
    return
  fi

  # design/ patterns
  if [[ "$basename" == design-token-* ]] || [[ "$basename" == color-scheme-* ]] || \
     [[ "$basename" == *-interaction ]] || [[ "$basename" == *-wireframe ]] || \
     [[ "$filename" == *.png ]] || [[ "$filename" == *.svg ]]; then
    echo "design"
    return
  fi

  echo ""
}

# Process files
declare -a COMPLIANT_FILES=()
declare -a NONCOMPLIANT_FILES=()
declare -a PROTECTED_FILES=()

while IFS= read -r -d '' file; do
  # Skip README.md and docs-guide.md
  localpath="${file#$DOCS_PATH/}"
  filename=$(basename "$file")

  [[ "$filename" == "README.md" ]] && continue
  [[ "$filename" == "docs-guide.md" ]] && continue

  # Check if in protected directory
  in_protected=false
  for pdir in $PROTECTED_DIRS; do
    if [[ "$localpath" == "$pdir"* ]]; then
      PROTECTED_FILES+=("$localpath")
      in_protected=true
      ((PROTECTED++)) || true
      break
    fi
  done
  $in_protected && continue

  # Check naming
  naming_issues=$(check_naming "$filename")

  # Check if in correct directory
  topdir=$(echo "$localpath" | cut -d'/' -f1)
  expected=$(guess_expected_dir "$filename")

  if [[ -n "$naming_issues" ]]; then
    suggestion=""
    if [[ -n "$expected" && "$topdir" != "$expected" ]]; then
      suggestion=" → move to $expected/ and rename"
    else
      suggestion=" → rename to fix: $naming_issues"
    fi
    NONCOMPLIANT_FILES+=("  $DOCS_PATH/$localpath$suggestion")
    ((NONCOMPLIANT++)) || true
  elif [[ -n "$expected" && "$topdir" != "$expected" && "$topdir" != "$DOCS_PATH" ]]; then
    NONCOMPLIANT_FILES+=("  $DOCS_PATH/$localpath → should be in $expected/")
    ((NONCOMPLIANT++)) || true
  else
    COMPLIANT_FILES+=("  $DOCS_PATH/$localpath")
    ((COMPLIANT++)) || true
  fi
done < <(find "$DOCS_PATH" -type f -print0 2>/dev/null)

# Print report
TOTAL=$((COMPLIANT + NONCOMPLIANT + PROTECTED))
echo -e "Scanned $DOCS_PATH/ — ${TOTAL} files found:"
echo ""

if [[ ${#COMPLIANT_FILES[@]} -gt 0 ]]; then
  echo -e "${GREEN}✓ Compliant (${COMPLIANT}):${NC}"
  for f in "${COMPLIANT_FILES[@]}"; do
    echo -e "${GREEN}$f${NC}"
  done
  echo ""
fi

if [[ ${#NONCOMPLIANT_FILES[@]} -gt 0 ]]; then
  echo -e "${YELLOW}⚠ Non-compliant (${NONCOMPLIANT}):${NC}"
  for f in "${NONCOMPLIANT_FILES[@]}"; do
    echo -e "${YELLOW}$f${NC}"
  done
  echo ""
fi

if [[ ${#PROTECTED_FILES[@]} -gt 0 ]]; then
  echo -e "${BLUE}⊘ Protected (${PROTECTED}):${NC}"
  for f in "${PROTECTED_FILES[@]}"; do
    echo -e "${BLUE}  $DOCS_PATH/$f (framework directory, skipped)${NC}"
  done
  echo ""
fi

# Check for missing README.md indexes
echo -e "${BLUE}Directory index check:${NC}"
for dir in $STANDARD_DIRS; do
  if [[ -d "$DOCS_PATH/$dir" ]]; then
    if [[ -f "$DOCS_PATH/$dir/README.md" ]]; then
      echo -e "  ${GREEN}✓${NC} $dir/README.md exists"
    else
      echo -e "  ${YELLOW}⚠${NC} $dir/README.md missing"
    fi
  fi
done

echo ""
echo "Summary: ${GREEN}${COMPLIANT} compliant${NC}, ${YELLOW}${NONCOMPLIANT} non-compliant${NC}, ${BLUE}${PROTECTED} protected${NC}"
