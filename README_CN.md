# cpp-ai-constitution

[English](README.md) | **中文**

面向AI编程Agent的C++工具无关约束系统。

不是压缩版教材——是判断引擎。

灵感来自 C++ Core Guidelines 和 [Perplexity的Skill设计方法论](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)。

**OpenCode优先，Agent中立，OpenClaw兼容。**

## 兼容性

- OpenCode（主要）
- Claude Code
- Cursor
- Codex CLI
- Gemini CLI
- OpenClaw
- 任何支持rules/skills的Agent

## 这是什么

AI可读的工程约束系统，帮助Agent：

- 识别高影响的C++错误（不是背诵C++常识）
- 修改指针类型前先分类所有权
- 先跑工具检查再主观审查
- 安全修复和风格修改分开
- 知道什么时候"现代C++"规则有例外

## 这不是什么

- C++教程
- C++ Core Guidelines压缩版
- "全部现代化"强制执行工具
- 加载一次就忘的东西

## 设计原则

来自[Perplexity的Skill研究](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)：

> 如果很容易解释，模型已经知道了。删掉它。
> 陷阱才是特殊情况。它们是最高价值的内容。

## 目录结构

```text
cpp-ai-constitution/
├── AGENTS.md                   # Agent中立主入口
├── SKILL.md                    # 根Skill：路由、优先级、宪法
├── CLAUDE.md                   # Claude Code精简摘要
├── GOTCHAS.md                  # AI在C++中的失败模式
├── opencode.json.example       # OpenCode配置示例
├── references/                 # 详细规则（按需加载）
├── .opencode/skills/           # OpenCode技能（3个）
├── .opencode/agents/           # OpenCode角色（3个）
├── .claude/skills/             # Claude Code兼容
├── .agents/skills/             # 通用Agent兼容
├── scripts/                    # 自动化脚本
├── assets/                     # 模板
├── hooks/                      # Git钩子
├── config/                     # clang工具配置（3档）
├── prompts/                    # AI提示词
└── evals/                      # Skill路由测试
```

## 集成方式

### OpenCode（推荐）

```bash
cp AGENTS.md /你的项目/AGENTS.md
cp opencode.json.example /你的项目/opencode.json
cp -r .opencode/ /你的项目/.opencode/
```

### Claude Code

```bash
cp CLAUDE.md /你的项目/CLAUDE.md
cp -r .claude/skills/ /你的项目/.claude/skills/
```

### 通用AI编程

复制 `AGENTS.md` 和需要的 `references/*.md` 到你的Agent上下文。

### OpenClaw

使用 `SKILL.md` 和规则文件作为可复用项目技能。

## 多技能体系

本项目包含3个专用技能：

| 技能 | 用途 |
|---|---|
| `cpp-core-review` | 代码审查、安全审计、AI输出验证 |
| `cpp-modernize` | C++迁移、系统性现代化 |
| `cpp-debug-audit` | 崩溃调试、内存错误、sanitizer审计 |

3个Agent角色：

| 角色 | 职责 |
|---|---|
| `cpp-reviewer` | 只读严格审查 |
| `cpp-refactor-planner` | 制定安全现代化计划 |
| `cpp-safety-auditor` | 系统性安全审计 |

## 渐进加载

不是所有规则都适用所有项目。按需加载：

| 条件 | 读取 |
|---|---|
| 所有权/生命周期 | `references/lifetime.md` |
| 多线程代码 | `references/concurrency.md` |
| 自定义错误处理 | `references/error-handling.md` |
| 模板元编程 | `references/templates.md` |
| 性能关键路径 | `references/performance.md` |

## clang-tidy配置分档

| 配置 | 用途 |
|---|---|
| `clang-tidy.minimal.yml` | CI基线，低误报 |
| `clang-tidy.migration.yml` | 老项目迁移 |
| `clang-tidy.strict.yml` | 新项目或严格审查 |

```bash
clang-tidy file.cpp --config-file=config/clang-tidy.minimal.yml -- -std=c++20
```

## 同步脚本

维护多平台兼容时：

```bash
python3 scripts/sync_skill_targets.py
```

将源 `SKILL.md` 同步到 `.opencode/`、`.claude/`、`.agents/` 目录。

## Token预算

| 层级 | 内容 | 大致成本 |
|---|---|---|
| Index | name + description | ~50 tokens |
| Load | SKILL.md正文 | ~1,500 tokens |
| Runtime | references、scripts、assets | ~0-8,000 tokens（按需） |

## 致谢

- C++ Core Guidelines — Bjarne Stroustrup, Herb Sutter 等
- [Perplexity: Designing, Refining, and Maintaining Agent Skills](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)
