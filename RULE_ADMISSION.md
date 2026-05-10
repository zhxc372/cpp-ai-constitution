# Rule Admission Standard

> 每条新规则必须证明自己值得进入这个项目。

---

## 1. Admission Criteria

A new rule may be added **only if** it comes from at least one of:

| Source | Description |
|--------|-------------|
| Repeated AI failure | AI agent repeatedly makes this mistake |
| Known C++ safety hazard | UB, memory corruption, data race, lifetime bug |
| Project-specific constraint | Build system, ABI, exception policy, ownership model |
| Eval failure | A test case exposed the problem |
| Tool-detectable issue | clang-tidy, compiler warning, sanitizer can catch it |
| Real bug pattern | Observed in production or review |

**General C++ knowledge is not enough.** If a competent C++ developer would already know it, it doesn't belong here.

---

## 2. Required Documentation

Each new rule must document:

```yaml
rule: "Brief description"
source: "AI failure | safety hazard | project constraint | eval failure | tool-detectable | real bug"
scope: "ownership | lifetime | concurrency | exceptions | API | performance | style"
token_cost: "root-skill | reference-only"
validation: "eval | script | test | manual-review"
example: "Concrete example of the mistake this prevents"
```

---

## 3. Token Cost Review

Rules should be placed where they deliver maximum value per token:

| Location | When to use |
|----------|-------------|
| Root SKILL.md | High-frequency, life-saving rules |
| references/*.md | Specialized rules for specific scenarios |
| GOTCHAS.md | Failure patterns that might become rules |

Periodic review:

- If models have learned this rule → consider removing
- If rule only applies to special scenarios → move to references
- If rule frequently prevents disasters → keep in root SKILL

---

## 4. Admission Flow

```text
Identify failure case
  → Document in GOTCHAS.md as candidate
  → Add eval case
  → Assess token cost vs. value
  → Decide: root SKILL / reference / reject
  → Human review and approve
  → Merge
```

---

## 5. Rejection Criteria

A rule will be rejected if:

- It's just "good practice" without evidence of AI failure
- It duplicates C++ Core Guidelines without AI-specific context
- It can't be tied to a concrete failure mode
- Its token cost exceeds its preventive value
- It mixes style preference with safety requirement
