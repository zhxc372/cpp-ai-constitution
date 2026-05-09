#!/usr/bin/env bash
set -e

# AI code scan: find potential issues in C++ files
# Excludes .git, build, and common non-source directories

FILES=$(find . -type f \( -name "*.cpp" -o -name "*.hpp" -o -name "*.cc" -o -name "*.h" \) \
    -not -path "./.git/*" \
    -not -path "./build/*" \
    -not -path "./cmake-build-*/*" \
    -not -path "./node_modules/*" \
    2>/dev/null)

if [ -z "$FILES" ]; then
    echo "No C++ files found."
    exit 0
fi

TOTAL_ERRORS=0

for f in $FILES; do
    echo "Scanning $f"

    # Check for raw new/delete
    if grep -nE '\bnew\s+\w+' "$f" | grep -v '//\|/\*' > /dev/null 2>&1; then
        echo "  ⚠ raw 'new' found (use RAII/smart pointer)"
        TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    fi

    if grep -nE '\bdelete\s+\w+' "$f" | grep -v '//\|/\*' > /dev/null 2>&1; then
        echo "  ⚠ raw 'delete' found (use RAII/smart pointer)"
        TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    fi

    # Check for malloc/free
    if grep -nE '\bmalloc\(|\bfree\(' "$f" | grep -v '//\|/\*' > /dev/null 2>&1; then
        echo "  ⚠ malloc/free found (use RAII)"
        TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    fi

    # Check for detached threads
    if grep -nE '\.detach\(\)' "$f" | grep -v '//\|/\*' > /dev/null 2>&1; then
        echo "  ⚠ detached thread found"
        TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    fi

    # Check for mutable globals
    if grep -nE '^\s*(inline\s+)?(static\s+)?(mutable\s+)?\w+\s*\*?\s*\w+\s*=' "$f" | grep -v 'const\|constexpr\|inline static const' > /dev/null 2>&1; then
        echo "  ⚠ possible mutable global state"
    fi
done

echo ""
echo "Scan complete. Issues found: $TOTAL_ERRORS"
exit $TOTAL_ERRORS
