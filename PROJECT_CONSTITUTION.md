# cpp-ai-constitution Project Constitution

> AI expands the search space. Human compresses the decision space.  
> Scripts verify the deterministic space. Adapters only translate, never invent.

---

## 0. Mission

This project exists to **reduce high-impact C++ mistakes made by AI coding agents**.

It is not a C++ textbook, not a compressed copy of C++ Core Guidelines, and not a style-enforcement package.

**Core mission:**

> 阻止 AI 在 C++ 项目里乱改、误改、过度现代化、忽视所有权、破坏 ABI、混合安全修复和风格重写。

**Final output:**

> AI-readable engineering constraints that make agents more cautious, tool-aware, and less likely to perform unsafe C++ changes.

---

## 1. Core Principle

Strong constraints reduce AI entropy.

This project must make AI coding agents more cautious, more tool-aware, and less likely to perform unsafe C++ changes.

Every rule must answer:

- Does this rule reduce a common high-cost AI mistake in C++?
- Does this rule come from real failure, tool detection, project constraint, or eval failure?
- Is this rule worth the token cost?

If it's just general C++ knowledge, it doesn't belong here.

---

## 2. Single Source of Truth

Core rules must live in one place.

```
core/ (this repo) is the single source of truth.
adapters/ may only translate or route rules for specific agents.
```

**Adapters must not invent new engineering rules.**

If OpenCode, Claude Code, Cursor, Codex CLI, Gemini CLI, or OpenClaw need different formats, they get different file layouts — but the same rules.

---

## 3. Tool First

Mechanical checks must precede subjective review.

```text
1. Find the build system
2. Find compile_commands.json
3. Check .clang-tidy config
4. Run compiler warnings
5. Run clang-tidy
6. Run tests
7. Run sanitizers
8. Then do subjective review
```

Without tool context, AI output must be downgraded to "risk indicator", not certainty.

---

## 4. Change Discipline

Never mix:

1. Safety fixes (do first)
2. Behavior-preserving refactors
3. Modernization
4. Style changes (do last)
5. Performance changes

Safety comes first. Style comes last.

---

## 5. Rule Admission Standard

A new rule may be added only if it comes from at least one of:

- Repeated AI failure
- Known C++ safety hazard
- Project-specific engineering constraint
- Eval failure
- Tool-detectable issue
- Real bug pattern

Each rule must document:

```yaml
source: AI failure | safety hazard | project constraint | eval failure | tool-detectable
scope: ownership | lifetime | concurrency | exceptions | API | performance | style
token_cost: root-skill | reference-only
validation: eval | script | test | manual-review
```

---

## 6. Human Decision Rights

AI may identify risks, propose patches, run scripts, and generate review reports.

**Human must approve:**

- Ownership model changes
- ABI-impacting changes
- Exception policy changes
- Large refactors
- Core rule changes
- Adapter rule changes
- Constitution changes

**AI must not:**

- Mechanically replace raw pointers
- Modernize before preserving behavior
- Mix safety and style changes
- Change ABI assumptions without approval
- Change exception policy without approval
- Treat missing build context as certainty
- Modify this constitution without human review
- Approve its own rule changes

---

## 7. Adapter Policy

Adapters exist only to translate the same core rules into platform-specific formats.

**Adapters may:**

- Change file layout required by the platform
- Add platform-specific invocation examples
- Map trigger phrases
- Reference core rules
- Load references conditionally

**Adapters must not:**

- Invent new C++ engineering rules
- Weaken safety rules
- Skip tool-first requirements
- Remove ownership classification
- Combine modernization with safety fixes
- Silently diverge from this constitution

Every adapter entry file must declare:

```
This adapter is not a source of truth. Follow PROJECT_CONSTITUTION.md and core references.
```

---

## 8. Failure Deposition

Every failure must produce at least one of:

- Gotcha entry in GOTCHAS.md
- Eval case in evals/
- Rule patch in references/
- Checklist item
- Script check
- Documentation update

Gotcha-driven evolution is the primary rule growth mechanism:

```text
发现 AI 失败案例
  → 加入 GOTCHAS.md 候选
  → 添加 eval case
  → 判断是否进入 references
  → 必要时进入 root SKILL
  → 人类 review 合并
```

---

## Project Motto

> 核心唯一，适配只翻译。  
> 工具优先，规则有来源。  
> AI 不自我批准。  
> 人类决定高风险修改。
