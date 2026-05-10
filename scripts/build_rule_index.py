#!/usr/bin/env python3
"""
Build rule index (data/rule_index.json) from reference docs.
AI reads this index first to determine which reference docs to load.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).parent.parent
REFERENCES_DIR = ROOT / "references"
OUTPUT_JSON = ROOT / "data" / "rule_index.json"

# Mapping of filename to rule category
FILE_CATEGORIES = {
    "rule-map.md": "index",
    "lifetime.md": "ownership, lifetime, dangling, references, pointers",
    "resource-management.md": "raii, ownership, smart pointers, resources, memory",
    "concurrency.md": "thread, concurrency, data race, lock, async, thread safety",
    "error-handling.md": "exception, error, try-catch, std::expected, error code, noexcept",
    "interfaces.md": "api, interface, design, public, function, method, ABI",
    "classes.md": "class, constructor, destructor, inheritance, virtual, object",
    "templates.md": "template, concept, generic, metaprogramming, TMP",
    "performance.md": "performance, optimization, speed, memory, cache, hot path, profile"
}

# Keywords to extract from each file
KEYWORD_PATTERNS = [
    r"`std::(\w+)`",
    r"`(\w+)`",
    r"\*\*(\w+)\*\*",
]

def extract_keywords_from_file(filepath: Path) -> Set[str]:
    """Extract relevant keywords from a reference doc."""
    keywords = set()
    
    try:
        content = filepath.read_text(encoding='utf-8').lower()
        
        # Extract from patterns
        for pattern in KEYWORD_PATTERNS:
            matches = re.findall(pattern, content)
            for m in matches:
                if len(m) > 2 and not m.isdigit():
                    keywords.add(m.strip())
        
        # Also add all words from section headers
        for line in content.split('\n'):
            if line.startswith('#'):
                header_words = re.findall(r'\w+', line.lower())
                keywords.update(header_words)
    
    except Exception as e:
        print(f"⚠️ Failed to read {filepath}: {e}", file=sys.stderr)
    
    return keywords

def build_index() -> Dict:
    """Build the rule index."""
    index = {
        "categories": {},
        "file_mapping": {},
        "keyword_mapping": {}
    }
    
    # First pass: process each reference file
    for filename, tags_str in FILE_CATEGORIES.items():
        filepath = REFERENCES_DIR / filename
        if not filepath.exists():
            print(f"⚠️ Missing reference file: {filename}", file=sys.stderr)
            continue
        
        categories = [t.strip() for t in tags_str.split(',')]
        keywords = extract_keywords_from_file(filepath)
        
        # Update file mapping
        index["file_mapping"][filename] = {
            "categories": categories,
            "keywords": list(keywords),
            "path": str(filepath.relative_to(ROOT))
        }
        
        # Update category mapping
        for cat in categories:
            if cat not in index["categories"]:
                index["categories"][cat] = []
            index["categories"][cat].append(filename)
    
    # Second pass: build keyword reverse mapping
    keyword_map = {}
    for filename, info in index["file_mapping"].items():
        for kw in info["keywords"]:
            if kw not in keyword_map:
                keyword_map[kw] = []
            keyword_map[kw].append(filename)
    
    # Only keep keywords that appear in at least 2 files (more discriminative)
    # Or very specific keywords regardless of frequency
    # Filter out meaningless keywords
    noise_keywords = {
        "and", "this", "ai", "common", "mistakes", "rules", "patterns", "vs",
        "do", "not", "the", "for", "that", "with", "are", "but", "also",
        "can", "has", "its", "may", "use", "used", "using", "will",
        "all", "any", "one", "two", "get", "set", "has", "new",
        "code", "check", "time", "data", "type", "value", "make",
        "before", "after", "during", "when", "where", "which", "what",
        "more", "only", "very", "each", "per", "such", "other",
        "see", "note", "add", "fix", "much", "many", "few",
        "always", "never", "often", "sometimes", "usually",
        "change", "changing", "changed", "changes",
        "work", "working", "works",
        "good", "bad", "better", "important",
        "example", "examples",
        "rules", "rule",
        "version", "versions",
        "must", "should", "need", "needs",
    }
    
    filtered_kw = {}
    prioritized_kws = {"dangling", "lifetime", "raii", "data race", "undefined behavior", 
                      "segfault", "memory leak", "shared_ptr", "unique_ptr", "weak_ptr",
                      "constexpr", "noexcept", "virtual", "std::expected", "abi"}
    
    for kw, files in keyword_map.items():
        if kw in noise_keywords:
            continue
        if kw in prioritized_kws or len(files) >= 2:
            filtered_kw[kw] = files
    
    index["keyword_mapping"] = filtered_kw
    
    # Add metadata
    index["metadata"] = {
        "total_files": len(index["file_mapping"]),
        "total_categories": len(index["categories"]),
        "total_keywords": len(index["keyword_mapping"]),
        "generated_by": "scripts/build_rule_index.py"
    }
    
    return index

def main() -> int:
    """Main function."""
    index = build_index()
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated rule index: {OUTPUT_JSON}")
    print(f"📊 Stats:")
    print(f"  - {index['metadata']['total_files']} reference files")
    print(f"  - {index['metadata']['total_categories']} categories")
    print(f"  - {index['metadata']['total_keywords']} indexed keywords")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
