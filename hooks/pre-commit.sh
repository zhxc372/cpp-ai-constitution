#!/usr/bin/env bash
set -e

# Find C++ files, excluding .git, build, and common non-source directories
FILES=$(find . -type f \( -name "*.cpp" -o -name "*.hpp" -o -name "*.cc" -o -name "*.h" \) \
    -not -path "./.git/*" \
    -not -path "./build/*" \
    -not -path "./cmake-build-*/*" \
    -not -path "./node_modules/*" \
    2>/dev/null)

if [ -z "$FILES" ]; then
    echo "[pre-commit] No C++ files found."
    exit 0
fi

echo "[pre-commit] Running clang-format..."
echo "$FILES" | xargs clang-format -i

echo "[pre-commit] Running clang-tidy..."
for f in $FILES; do
    echo "  Checking $f"
    clang-tidy "$f" --config-file=config/.clang-tidy -- -std=c++20 2>/dev/null || true
done

echo "[pre-commit] Done."
