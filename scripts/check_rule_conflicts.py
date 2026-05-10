#!/usr/bin/env python3
"""
Detect conflicting rules across reference docs.
Looks for contradictory statements or opposite recommendations.
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

ROOT = Path(__file__).parent.parent
REFERENCES_DIR = ROOT / "references"
GOTCHAS_FILE = ROOT / "GOTCHAS.md"

# Contradiction patterns: pairs of opposite statements
CONTRADICTION_PAIRS = [
    # Ownership
    (r"use raw pointers", r"don't use raw pointers"),
    (r"use std::shared_ptr", r"avoid std::shared_ptr"),
    (r"prefer unique_ptr", r"prefer shared_ptr"),
    # Performance
    (r"always optimize", r"don't optimize prematurely"),
    (r"use custom containers", r"use standard containers"),
    # Modernization
    (r"always modernize", r"don't break ABI"),
    (r"replace all C arrays", r"keep C arrays at API boundaries"),
    # Error handling
    (r"use exceptions", r"don't use exceptions"),
    (r"use std::expected", r"don't use std::expected"),
    # Concurrency
    (r"use lock-free", r"don't use lock-free without proof"),
    (r"detach threads", r"never detach threads"),
    # Class design
    (r"use inheritance", r"prefer composition over inheritance"),
    (r"use virtual methods", r"avoid virtual methods in hot paths"),
    # Const correctness
    (r"use const everywhere", r"don't const objects you need to move"),
]

# Common false positive triggers
FALSE_POSITIVES = [
    "at API boundaries",
    "in hot paths",
    "when performance matters",
    "unless you need ownership",
    "except for observers",
    "by default",
    "by default, prefer",
    "generally",
    "prefer",
    "recommended",
]

class RuleConflict:
    """Represents a detected rule conflict."""
    def __init__(self, file1: str, line1: int, text1: str,
                 file2: str, line2: int, text2: str,
                 pattern: Tuple[str, str]):
        self.file1 = file1
        self.line1 = line1
        self.text1 = text1.strip()
        self.file2 = file2
        self.line2 = line2
        self.text2 = text2.strip()
        self.pattern = pattern
        self.severity = self._calculate_severity()
    
    def _calculate_severity(self) -> str:
        """Calculate severity of conflict."""
        # If same file, higher severity
        if self.file1 == self.file2:
            return "CRITICAL"
        # If contradiction is clear and no conditional
        t1 = self.text1.lower()
        t2 = self.text2.lower()
        has_condition = any(f.lower() in t1 or f.lower() in t2 for f in FALSE_POSITIVES)
        return "HIGH" if not has_condition else "MEDIUM"
    
    def __str__(self) -> str:
        return f"""[{self.severity}] Conflict detected:
File 1: {self.file1}:{self.line1}
Text 1: {self.text1}
File 2: {self.file2}:{self.line2}
Text 2: {self.text2}
Pattern: "{self.pattern[0]}" vs "{self.pattern[1]}"
"""

def extract_rules_from_file(filepath: Path) -> List[Tuple[int, str]]:
    """Extract all rule-like statements from a file."""
    rules = []
    if not filepath.exists():
        return rules
    
    content = filepath.read_text(encoding='utf-8')
    for i, line in enumerate(content.split('\n'), 1):
        line = line.strip()
        # Only look at non-empty, non-header lines
        if not line or line.startswith('#'):
            continue
        # Ignore code blocks
        if line.startswith('```') or line.startswith('    '):
            continue
        # Look for lines with recommendation language
        if any(kw in line.lower() for kw in ["use", "don't", "avoid", "prefer", "always", "never", "should", "shouldn't", "recommend"]):
            rules.append((i, line))
    return rules

def check_for_conflicts(rules1: List[Tuple[int, str]], file1: str,
                       rules2: List[Tuple[int, str]], file2: str) -> List[RuleConflict]:
    """Check for conflicts between two sets of rules."""
    conflicts = []
    lower_rules1 = [(line, text.lower()) for line, text in rules1]
    lower_rules2 = [(line, text.lower()) for line, text in rules2]
    
    for pat_a, pat_b in CONTRADICTION_PAIRS:
        pat_a_low = pat_a.lower()
        pat_b_low = pat_b.lower()
        
        matches_a = []
        for line, text in lower_rules1:
            if re.search(pat_a_low, text, re.IGNORECASE):
                # Get original case text
                original_text = next(t for l, t in rules1 if l == line)
                matches_a.append((line, original_text))
        
        matches_b = []
        for line, text in lower_rules2:
            if re.search(pat_b_low, text, re.IGNORECASE):
                original_text = next(t for l, t in rules2 if l == line)
                matches_b.append((line, original_text))
        
        # Generate conflicts for all combinations
        for line1, text1 in matches_a:
            for line2, text2 in matches_b:
                # Skip if same line (false positive from same line)
                if file1 == file2 and line1 == line2:
                    continue
                # Check if it's a false positive
                if any(f in text1.lower() and f in text2.lower() for f in FALSE_POSITIVES):
                    continue
                # Create conflict
                conflicts.append(RuleConflict(
                    file1, line1, text1,
                    file2, line2, text2,
                    (pat_a, pat_b)
                ))
    
    return conflicts

def main() -> int:
    """Main function."""
    # Load all reference files
    all_files = list(REFERENCES_DIR.glob("*.md"))
    all_files.append(GOTCHAS_FILE)
    
    if not all_files:
        print("❌ No reference files found", file=sys.stderr)
        return 1
    
    print(f"🔍 Checking {len(all_files)} files for rule conflicts...")
    
    all_rules: Dict[str, List[Tuple[int, str]]] = {}
    for f in all_files:
        rel_path = str(f.relative_to(ROOT))
        all_rules[rel_path] = extract_rules_from_file(f)
        print(f"  {rel_path}: {len(all_rules[rel_path])} rules extracted")
    
    # Check all pairs of files
    conflicts = []
    files = list(all_rules.keys())
    for i in range(len(files)):
        f1 = files[i]
        rules1 = all_rules[f1]
        for j in range(i, len(files)):
            f2 = files[j]
            rules2 = all_rules[f2]
            new_conflicts = check_for_conflicts(rules1, f1, rules2, f2)
            conflicts.extend(new_conflicts)
    
    # Report results
    print(f"\n📊 Results:")
    if not conflicts:
        print("✅ No conflicts detected! All rules are consistent.")
        return 0
    
    print(f"⚠️ Found {len(conflicts)} potential conflicts:")
    for i, conf in enumerate(conflicts, 1):
        print(f"\n--- Conflict {i} ---")
        print(conf)
    
    # Count by severity
    severity_count = {
        "CRITICAL": sum(1 for c in conflicts if c.severity == "CRITICAL"),
        "HIGH": sum(1 for c in conflicts if c.severity == "HIGH"),
        "MEDIUM": sum(1 for c in conflicts if c.severity == "MEDIUM"),
    }
    
    print(f"\nSeverity breakdown:")
    for sev, count in severity_count.items():
        if count > 0:
            print(f"  {sev}: {count}")
    
    print(f"\n💡 Note: Not all conflicts are actual errors. Many are conditional rules that apply in different contexts.")
    
    return 1 if severity_count["CRITICAL"] > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
