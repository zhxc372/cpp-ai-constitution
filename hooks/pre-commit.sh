#!/usr/bin/env bash
set -e

echo "[pre-commit] running clang-format..."
find . -name "*.cpp" -o -name "*.hpp" | xargs clang-format -i

echo "[pre-commit] running clang-tidy..."
./hooks/ai-check.sh

echo "[pre-commit] done."
