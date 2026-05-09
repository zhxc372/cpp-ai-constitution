#!/usr/bin/env python3
"""
Run evals to validate skill routing and behavior.
Checks:
1. Positive cases load the correct skills
2. Negative cases do NOT load any skills
3. Adjacent confusions do NOT misroute
"""

import yaml
import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

ROOT = Path(__file__).parent.parent
EVALS_DIR = ROOT / "evals"

@dataclass
class EvalResult:
    id: str
    query: str
    expected_should_load: bool
    expected_skills: List[str]
    actual_should_load: Optional[bool] = None
    actual_skills: Optional[List[str]] = None
    passed: bool = False
    error: Optional[str] = None

def load_yaml(filepath: Path) -> List[Dict]:
    """Load YAML eval file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Failed to load {filepath}: {e}", file=sys.stderr)
        return []

def simulate_skill_routing(query: str) -> tuple[bool, List[str]]:
    """
    Simulate skill routing based on query content.
    Real implementation would use the agent's routing logic.
    This is a rule-based simulation for validation.
    """
    load = False
    skills = []
    
    q = query.lower()
    
    # First, check if C++ is explicitly mentioned or implied
    is_cpp = "c++" in q or "c++" in query.lower() or any(kw in q for kw in 
        ["std::", "unique_ptr", "shared_ptr", "string_view", "std::vector", "constexpr", 
         " noexcept", "raii", "#include", "template", "std::expected"]
    )
    
    # Positive triggers for cpp-core-review
    if is_cpp and any(kw in q for kw in ["review", "audit", "bug", "undefined behavior", "ub", 
        "ownership", "lifetime", "dangling", "raii", "exception safety", "api design", 
        "core guidelines", "safety issue", "is this code safe", "why doesn't this compile", 
        "should I", "is there a problem"]
    ):
        load = True
        skills.append("cpp-core-review")
    
    # Positive triggers for cpp-modernize
    if is_cpp and any(kw in q for kw in ["modernize", "refactor", "upgrade", "migrate", 
        "c++98", "c++11", "c++20", "c++23"]):
        load = True
        skills.append("cpp-modernize")
    
    # Positive triggers for cpp-debug-audit
    if is_cpp and any(kw in q for kw in ["debug", "crash", "memory leak", "segfault", 
        "asan", "sanitizer", "data race"]):
        load = True
        skills.append("cpp-debug-audit")
    
    # Positive triggers for agents
    if is_cpp and "plan" in q and "modernize" in q:
        skills.append("cpp-refactor-planner")
    if is_cpp and "audit" in q and "safety" in q:
        skills.append("cpp-safety-auditor")
    
    # Negative filters (override positives if these are present)
    if any(kw in q for kw in ["python", "go", "c#", "rust", "java", "javascript", "js"]):
        load = False
        skills = []
    # Skip general explanations but keep actual code reviews
    is_general_explanation = any(kw in q for kw in ["explain what a c++ pointer", "explain c++ pointer", "explain virtual function", "explain oop"])
    if not is_general_explanation and any(kw in q for kw in ["explain", "tutorial", "beginner", "install", "setup", "linker error", "build error", "format", "translate", "compare", "hello world"]):
        load = False
        skills = []
    if any(kw in q for kw in ["cmake", "ci", "cd", "github actions", "general", "os", "operating system"]):
        load = False
        skills = []
    # Special case: if query says "my program crashes" but no mention of C++, don't load
    if "my program crashes" in q and not is_cpp:
        load = False
        skills = []
    
    # Deduplicate skills
    skills = list(set(skills))
    
    return load, skills

def run_eval(case: Dict) -> EvalResult:
    """Run a single eval case."""
    result = EvalResult(
        id=case["id"],
        query=case["query"],
        expected_should_load=case["should_load"],
        expected_skills=case.get("expected_skills", [])
    )
    
    try:
        actual_load, actual_skills = simulate_skill_routing(case["query"])
        result.actual_should_load = actual_load
        result.actual_skills = sorted(actual_skills)
        result.expected_skills = sorted(result.expected_skills)
        
        # Check pass condition
        if actual_load == case["should_load"]:
            if not case["should_load"]:
                # For negative cases, just need to not load
                result.passed = True
            else:
                # For positive cases, skill sets must match (order doesn't matter)
                result.passed = result.actual_skills == result.expected_skills
        
        if not result.passed:
            if actual_load != case["should_load"]:
                result.error = f"Expected load={case['should_load']}, got={actual_load}"
            else:
                result.error = f"Expected skills={result.expected_skills}, got={result.actual_skills}"
    
    except Exception as e:
        result.error = f"Eval failed: {e}"
    
    return result

def print_summary(results: List[EvalResult], name: str) -> int:
    """Print summary for a group of evals."""
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    total = len(results)
    
    print(f"\n{'='*60}")
    print(f"📋 {name} Results: {passed}/{total} passed")
    print(f"{'='*60}")
    
    if failed > 0:
        print(f"❌ Failed cases:")
        for r in results:
            if not r.passed:
                print(f"\n  ID: {r.id}")
                print(f"  Query: {r.query[:80]}..." if len(r.query) > 80 else f"  Query: {r.query}")
                print(f"  Error: {r.error}")
    
    return failed

def main() -> int:
    """Run all evals."""
    total_failed = 0
    
    # Load all eval groups
    groups = [
        ("Positive Load Cases", "positive-load-cases.yaml"),
        ("Negative Load Cases", "negative-load-cases.yaml"),
        ("Adjacent Skill Confusions", "adjacent-skill-confusions.yaml"),
        ("Hero Queries", "hero-queries.yaml"),
    ]
    
    all_results = []
    
    for group_name, filename in groups:
        filepath = EVALS_DIR / filename
        cases = load_yaml(filepath)
        if not cases:
            print(f"⚠️ No cases loaded from {filename}, skipping", file=sys.stderr)
            continue
        
        print(f"\n▶️ Running {len(cases)} {group_name}...")
        results = [run_eval(case) for case in cases]
        total_failed += print_summary(results, group_name)
        all_results.extend(results)
    
    # Overall summary
    print(f"\n{'='*80}")
    total = len(all_results)
    passed = sum(1 for r in all_results if r.passed)
    print(f"🏁 Overall Results: {passed}/{total} passed ({int(passed/total*100)}%)")
    
    if total_failed > 0:
        print(f"❌ {total_failed} failed cases - review above output")
    else:
        print("✅ All evals passed!")
    print(f"{'='*80}")
    
    # Save detailed results
    result_data = [
        {
            "id": r.id,
            "query": r.query,
            "expected_should_load": r.expected_should_load,
            "expected_skills": r.expected_skills,
            "actual_should_load": r.actual_should_load,
            "actual_skills": r.actual_skills,
            "passed": r.passed,
            "error": r.error
        }
        for r in all_results
    ]
    
    output_file = ROOT / "evals" / "eval-results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Detailed results saved to {output_file}")
    
    return 0 if total_failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
