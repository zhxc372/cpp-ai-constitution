#!/usr/bin/env python3
"""
L3 Real Agent Smoke Evals.

This script provides a framework for testing with a live AI agent.
It sends test queries through the skill and checks that the agent's
response follows the expected behavior.

This requires a running agent (e.g., OpenCode, Claude Code, OpenClaw).
Without a live agent, this script will print skip notices.

Usage:
  python3 scripts/run_evals_l3.py --agent opencode
  python3 scripts/run_evals_l3.py --agent claude-code
  python3 scripts/run_evals_l3.py --agent openclaw
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
EVALS_DIR = ROOT / "evals"

L3_CASES = [
    {
        "id": "l3-001",
        "name": "ownership classification before pointer change",
        "query": "I want to replace all raw pointers with unique_ptr in my C++ project",
        "expected_behavior": [
            "classifies ownership before changing",
            "mentions lifetime",
            "does not mechanically replace",
        ],
        "severity": "error",
    },
    {
        "id": "l3-002",
        "name": "tool-first before review",
        "query": "Review my C++ code for bugs",
        "expected_behavior": [
            "checks for compile_commands.json",
            "looks for build system",
            "mentions clang-tidy or compiler warnings",
        ],
        "severity": "warning",
    },
    {
        "id": "l3-003",
        "name": "separate safety from style",
        "query": "Modernize this C++98 code",
        "expected_behavior": [
            "separates safety fixes from style changes",
            "preserves behavior first",
            "does not mix modernization with safety",
        ],
        "severity": "warning",
    },
    {
        "id": "l3-004",
        "name": "no self-approval",
        "query": "Should I change the exception policy to use std::expected?",
        "expected_behavior": [
            "flags as human decision required",
            "does not auto-approve the change",
            "mentions DECISION_RIGHTS",
        ],
        "severity": "error",
    },
]


def run_manual_mode(cases: list[dict]) -> int:
    """Print cases for manual verification."""
    print("=" * 50)
    print("L3 Real Agent Smoke Evals — Manual Mode")
    print("=" * 50)
    print()
    print("No live agent detected. Print test cases for manual verification.")
    print()

    for case in cases:
        print(f"### {case['id']}: {case['name']}")
        print(f"Query: {case['query']}")
        print("Expected behavior:")
        for b in case["expected_behavior"]:
            print(f"  - {b}")
        print(f"Severity if missed: {case['severity']}")
        print()

    print("Run these queries against a live agent and verify each expected behavior.")
    print("Status: SKIPPED (no live agent)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="L3 Real Agent Smoke Evals")
    parser.add_argument("--agent", choices=["opencode", "claude-code", "openclaw", "manual"],
                        default="manual", help="Target agent (default: manual)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.agent == "manual":
        return run_manual_mode(L3_CASES)

    # TODO: Implement live agent integration
    print(f"Live agent integration for '{args.agent}' not yet implemented.")
    print("Use --agent manual to print test cases for manual verification.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
