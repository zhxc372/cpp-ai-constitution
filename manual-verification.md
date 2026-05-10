# Manual Verification Log

> 真实平台运行验证记录。Structure Verified 只保证文件结构和声明正确，不代表实际运行测试。

---

## OpenCode

| 项目 | 结果 | 日期 | 备注 |
|------|------|------|------|
| Skills auto-load | ⬜ 未测试 | - | 需要本地 OpenCode 环境 |
| C++ review trigger | ⬜ 未测试 | - | 需要真实 C++ 项目 |
| Reference loading | ⬜ 未测试 | - | 需要验证按需加载 |

## Claude Code

| 项目 | 结果 | 日期 | 备注 |
|------|------|------|------|
| CLAUDE.md auto-load | ⬜ 未测试 | - | 需要本地 Claude Code |
| Skill trigger | ⬜ 未测试 | - | 需要真实 C++ 项目 |

## OpenClaw

| 项目 | 结果 | 日期 | 备注 |
|------|------|------|------|
| SKILL.md load | ⬜ 未测试 | - | 需要部署到 OpenClaw |
| Trigger phrases | ⬜ 未测试 | - | 需要 OpenClaw 对话测试 |

## Cursor / Codex CLI / Gemini CLI

| 项目 | 结果 | 日期 | 备注 |
|------|------|------|------|
| Basic rules load | ⬜ 未测试 | - | Recipe only, 手动复制验证 |

---

## 验证方法

### Structure Verified（自动）
```bash
python3 scripts/validate_repo.py    # 文件结构、frontmatter、sync、header
python3 scripts/run_evals_l2.py     # adapter 一致性
```

### Real Platform Verified（手动）
1. 在目标平台打开一个 C++ 项目
2. 触发 review 场景（如 "review this C++ code"）
3. 验证：ownership classification、tool-first、safety/style 分离
4. 记录结果到本文件
