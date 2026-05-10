# Adapter Matrix

> Every adapter must follow ADAPTER_POLICY.md. This file documents support status per platform.

---

## Support Level Definitions

| Level | Meaning |
|-------|---------|
| **Officially Supported** | Has entry files, auto-load, eval tests, and manual verification |
| **Supported** | Has entry files and sync verification |
| **Recipe Only** | Has entry files but no automated verification |
| **Planned** | No entry files yet, but architecture supports it |
| **Unverified** | Community reported, not tested by maintainers |

---

## Platform Matrix

### OpenCode (Officially Supported)

| Item | Detail |
|------|--------|
| Entry files | `.opencode/skills/cpp-core-review/SKILL.md`, `.opencode/skills/cpp-debug-audit/SKILL.md`, `.opencode/skills/cpp-modernize/SKILL.md` |
| Agent files | `.opencode/agents/cpp-safety-auditor.md`, `.opencode/agents/cpp-refactor-planner.md`, `.opencode/agents/cpp-reviewer.md` |
| Install | `cp AGENTS.md /your-project/AGENTS.md && cp -r .opencode/ /your-project/.opencode/` |
| Auto-load | ✅ OpenCode auto-loads `.opencode/skills/` and `.opencode/agents/` |
| Test | `python3 scripts/validate_repo.py` (checks frontmatter + sync) |
| Limitations | None known |

### Claude Code (Supported)

| Item | Detail |
|------|--------|
| Entry files | `.claude/skills/cpp-core-review/SKILL.md`, `CLAUDE.md` |
| Install | `cp CLAUDE.md /your-project/CLAUDE.md && cp -r .claude/ /your-project/.claude/` |
| Auto-load | ✅ Claude Code reads `CLAUDE.md` and `.claude/skills/` |
| Test | `python3 scripts/validate_repo.py` (checks sync) |
| Limitations | Only core-review skill synced; no debug/modernize variants |

### Cursor (Recipe Only)

| Item | Detail |
|------|--------|
| Entry files | None (use AGENTS.md as `.cursorrules`) |
| Install | `cp AGENTS.md /your-project/.cursorrules` |
| Auto-load | ⚠️ Manual — Cursor reads `.cursorrules` but format differs |
| Test | Manual verification only |
| Limitations | No skill directory support; rules flatten to single file |

### Codex CLI (Recipe Only)

| Item | Detail |
|------|--------|
| Entry files | None (use AGENTS.md as `AGENTS.md`) |
| Install | `cp AGENTS.md /your-project/AGENTS.md` |
| Auto-load | ⚠️ Codex CLI reads `AGENTS.md` from project root |
| Test | Manual verification only |
| Limitations | No skill directory; no reference loading |

### Gemini CLI (Recipe Only)

| Item | Detail |
|------|--------|
| Entry files | None (use AGENTS.md) |
| Install | `cp AGENTS.md /your-project/AGENTS.md` |
| Auto-load | ⚠️ Gemini CLI reads project root config |
| Test | Manual verification only |
| Limitations | No skill directory; no reference loading |

### OpenClaw (Supported)

| Item | Detail |
|------|--------|
| Entry files | `SKILL.md` (canonical), `.agents/skills/cpp-core-review/SKILL.md` |
| Install | Copy `SKILL.md` to OpenClaw skill directory |
| Auto-load | ✅ OpenClaw loads skills via SKILL.md |
| Test | `python3 scripts/validate_repo.py` (checks sync) |
| Limitations | Only core-review skill synced |

### Any LLM (Level 1: Manual Copy)

| Item | Detail |
|------|--------|
| Entry files | None — copy SKILL.md content directly |
| Install | Copy SKILL.md text into chat prompt |
| Auto-load | ❌ Manual paste |
| Test | Not applicable |
| Limitations | No reference loading; no conditional rules; no tool execution |

---

## Sync Status

All adapter SKILL.md copies are auto-synced from canonical `SKILL.md` via:

```bash
python3 scripts/sync_skill_targets.py
```

Sync includes automatic adapter header injection per ADAPTER_POLICY.md.

---

## Adding a New Adapter

1. Create platform directory (e.g., `.codex/`)
2. Add entry file referencing canonical rules
3. Include required header: `<!-- Adapter Notice: This file is not a source of truth. Follow PROJECT_CONSTITUTION.md and core references. -->`
4. Add to `scripts/sync_skill_targets.py` TARGETS list
5. Add to `scripts/validate_repo.py` adapter file list
6. Update this matrix
7. Run `python3 scripts/validate_repo.py` to verify
