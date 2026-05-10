# Adapter Policy

> 适配层存在的唯一目的：将核心规则翻译为平台特定格式。

---

## 1. Purpose

Adapters exist only to translate the same core rules into platform-specific formats (OpenCode, Claude Code, Cursor, Codex CLI, Gemini CLI, OpenClaw, etc.).

---

## 2. Allowed

Adapters may:

- Change file layout required by the platform
- Add platform-specific invocation examples
- Map trigger phrases
- Reference core rules
- Load references conditionally
- Wrap tool commands for platform invocation

---

## 3. Forbidden

Adapters must not:

- Invent new C++ engineering rules
- Weaken safety rules
- Skip tool-first requirements
- Remove ownership classification
- Combine modernization with safety fixes
- Silently diverge from PROJECT_CONSTITUTION.md
- Produce different rule standards for different platforms

---

## 4. Required Header

Every adapter entry file must include this declaration:

```html
<!-- Adapter Notice: This file is not a source of truth. Follow PROJECT_CONSTITUTION.md and core references. -->
```

Or in comment format:

```
# Adapter Notice: This file is not a source of truth. Follow PROJECT_CONSTITUTION.md and core references.
```

---

## 5. Validation

Every adapter must:

- Pass shared eval cases (evals/)
- Stay in sync with canonical SKILL.md (checked by validate_repo.py)
- Include the required header
- Not contain rules not found in core/references/

Adapter consistency is verified by `evals/adapter-consistency.yaml`.
