# cpp-ai-constitution

[English](README.md) | **中文**

面向AI编程Agent的C++工具无关约束系统。不是压缩版教材——是判断引擎。

**OpenCode优先，Agent中立，OpenClaw兼容。**

灵感来自 C++ Core Guidelines 和 [Perplexity的Skill设计方法论](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)。

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

## 兼容性

- OpenCode（主要）
- Claude Code
- Cursor
- Codex CLI
- Gemini CLI
- OpenClaw
- 任何支持rules/skills的Agent

## 快速开始

### 1. OpenCode（推荐）

```bash
# 复制宪法到你的C++项目
cp AGENTS.md /你的项目/AGENTS.md
cp opencode.json.example /你的项目/opencode.json
cp -r .opencode/ /你的项目/.opencode/
cp -r references/ /你的项目/references/
cp -r scripts/ /你的项目/scripts/
cp -r config/ /你的项目/config/
cp -r assets/ /你的项目/assets/
cp GOTCHAS.md /你的项目/GOTCHAS.md
```

在OpenCode中，技能会自动加载：

```
@cpp-reviewer review src/foo.cpp
@cpp-safety-auditor audit src/
```

### 2. Claude Code

```bash
cp CLAUDE.md /你的项目/CLAUDE.md
cp -r .claude/skills/ /你的项目/.claude/skills/
cp -r references/ /你的项目/references/
cp -r scripts/ /你的项目/scripts/
cp -r config/ /你的项目/config/
```

告诉Claude："Follow CLAUDE.md and references/*.md."

### 3. OpenClaw

```bash
clawhub install cpp-ai-constitution
```

### 4. 通用AI编程

复制 `AGENTS.md` 和需要的 `references/*.md` 到Agent上下文。

### 5. Cursor

创建 `.cursor/rules/cpp.mdc`，引用 `AGENTS.md` 和 `references/`。

## 渐进加载

根 `SKILL.md`（~1,500 tokens）是默认唯一加载的。其他按需加载：

| 条件 | 加载 |
|---|---|
| 审查所有权/生命周期代码 | `references/lifetime.md` |
| 多线程代码 | `references/concurrency.md` |
| 自定义错误处理 | `references/error-handling.md` |
| 模板元编程 | `references/templates.md` |
| 性能关键路径 | `references/performance.md` |
| 完整审计 | 所有相关 `references/*.md` |

## Token预算

| 层级 | 内容 | 成本 |
|---|---|---|
| Index | name + description | ~50 tokens |
| Load | SKILL.md正文 | ~1,500 tokens |
| Runtime | references、scripts、assets | ~0-8,000 tokens（按需） |

## 多技能体系

| 技能 | 用途 | 什么时候用 |
|---|---|---|
| `cpp-core-review` | 代码审查、安全审计 | 审查任何非简单C++代码 |
| `cpp-modernize` | C++迁移、重构 | 从C++98/11升级到现代C++ |
| `cpp-debug-audit` | 崩溃调试、内存错误 | 调试UB、泄漏、数据竞争 |

## Agent角色

| 角色 | 做什么 | 怎么调用 |
|---|---|---|
| `cpp-reviewer` | 只读严格审查 | `@cpp-reviewer review src/foo.cpp` |
| `cpp-refactor-planner` | 制定安全现代化计划 | `@cpp-refactor-planner plan modernization` |
| `cpp-safety-auditor` | 系统性安全审计 | `@cpp-safety-auditor audit src/` |

## clang-tidy配置分档

| 配置 | 用途 | 命令 |
|---|---|---|
| `minimal` | CI基线，低误报 | `--config-file=config/clang-tidy.minimal.yml` |
| `migration` | 老项目迁移 | `--config-file=config/clang-tidy.migration.yml` |
| `strict` | 新项目或严格审查 | `--config-file=config/clang-tidy.strict.yml` |

## 脚本

确定性任务用脚本跑，不烧AI token：

```bash
python3 scripts/detect_cpp_project.py       # 识别项目结构
python3 scripts/find_compile_commands.py     # 查找编译数据库
python3 scripts/run_clang_tidy.py            # 运行静态分析+汇总
python3 scripts/sync_skill_targets.py        # 多平台同步
python3 scripts/validate_repo.py             # 仓库完整性校验
```

## 审查输出格式

发现按严重度分类：

- **Critical**：未定义行为、内存损坏、数据竞争、悬空引用
- **Major**：脆弱API、不一致的错误处理、隐藏副作用
- **Minor**：可读性、命名、风格
- **Do Not Change**：因ABI/遗留/性能约束应保留的代码

## 设计哲学

> 强约束降低熵。

每条规则必须证明它的token成本是值得的。如果模型已经知道了，删掉它。

## 致谢

- C++ Core Guidelines — Bjarne Stroustrup, Herb Sutter 等
- [Perplexity: Designing, Refining, and Maintaining Agent Skills](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)
