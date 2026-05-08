#!/usr/bin/env bash
set -e

FILES=$(find . -name "*.cpp" -o -name "*.hpp")

if [ -z "$FILES" ]; then
  echo "No C++ files found."
  exit 0
fi

for f in $FILES; do
  echo "Checking $f"
  clang-tidy "$f" --config-file=config/.clang-tidy -- -std=c++20
done
