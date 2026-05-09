# cpp-ai-constitution

[English](README.md) | **中文**

面向AI Agent的C++代码审查行为系统。不是压缩版教材——是判断引擎。

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
- 加载一次就忘的东西

## 设计原则

来自[Perplexity的Skill研究](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)：

> 如果很容易解释，模型已经知道了。删掉它。
> 陷阱才是特殊情况。它们是最高价值的内容。

本项目遵循这些原则：

- 跳过模型已经知道的东西
- 聚焦AI失败模式（gotchas）
- 渐进加载（不是一次全塞）
- 工具检查优先于主观审查

## 目录结构

```text
cpp-ai-constitution/
├── SKILL.md                    # 根：路由、优先级、宪法
├── CLAUDE.md                   # 精简规则摘要
├── GOTCHAS.md                  # AI在C++中的失败模式
├── references/                 # 详细规则（按需加载）
│   ├── rule-map.md             # 什么情况读什么规则
│   ├── lifetime.md             # 所有权和生命周期陷阱
│   ├── resource-management.md  # RAII模式和陷阱
│   ├── concurrency.md          # 线程安全规则
│   ├── error-handling.md       # 异常和错误策略
│   ├── interfaces.md           # API设计规则
│   ├── classes.md              # 类设计规则
│   ├── templates.md            # 模板和concepts规则
│   └── performance.md          # 性能审查清单
├── scripts/                    # 自动化脚本
│   ├── detect_cpp_project.py   # 识别C++项目结构
│   ├── find_compile_commands.py # 查找或生成compile_commands.json
│   └── run_clang_tidy.py       # 运行clang-tidy并汇总结果
├── assets/                     # 模板
│   ├── review-report-template.md  # 审查报告模板
│   ├── refactor-plan-template.md  # 重构计划模板
│   └── risk-levels.md             # 风险等级定义
├── hooks/                      # Git钩子
│   ├── pre-commit.sh           # 格式化+静态分析
│   └── ai-check.sh             # 基于模式的问题扫描
├── config/                     # 工具配置
│   ├── .clang-format           # 代码格式化规则
│   └── .clang-tidy             # 静态分析配置
├── prompts/                    # AI提示词
│   ├── system-prompt.md        # 系统提示词
│   └── review-prompt.md        # 审查提示词
└── evals/                      # Skill路由测试
    ├── positive-load-cases.md     # 应该加载的场景
    ├── negative-load-cases.md     # 不应该加载的场景
    ├── adjacent-skill-confusions.md # 邻近Skill混淆场景
    └── hero-queries.md            # 关键测试用例
```

## 快速开始

### 复制到你的项目

```bash
cp -r SKILL.md CLAUDE.md GOTCHAS.md references/ scripts/ assets/ hooks/ config/ prompts/ /你的项目/
```

### 配置你的AI工具

**Claude Code**：指向 `CLAUDE.md` + `SKILL.md`。

**Cursor**：创建 `.cursor/rules/cpp.mdc`，引用 `SKILL.md` 和 `references/`。

**OpenClaw**：将 `SKILL.md` + `prompts/system-prompt.md` 注入系统上下文。

### 运行工具

```bash
python3 scripts/detect_cpp_project.py
python3 scripts/find_compile_commands.py
python3 scripts/run_clang_tidy.py
```

## 渐进加载

不是所有规则都适用所有项目。`SKILL.md`指示Agent按需加载：

| 条件 | 读取 |
|---|---|
| 多线程代码 | `references/concurrency.md` |
| 自定义错误处理 | `references/error-handling.md` |
| 模板元编程 | `references/templates.md` |
| 性能关键路径 | `references/performance.md` |
| 所有权问题 | `references/lifetime.md` |
| API/接口设计 | `references/interfaces.md` |
| 类层次设计 | `references/classes.md` |
| 资源管理 | `references/resource-management.md` |

## Token预算

| 层级 | 内容 | 大致成本 |
|---|---|---|
| Index | name + description | ~50 tokens |
| Load | SKILL.md正文 | ~1,500 tokens |
| Runtime | references、scripts、assets | ~0-8,000 tokens（按需） |

## 审查输出格式

发现按严重度分类：

- **UB/安全**：未定义行为、内存损坏、数据竞争
- **所有权**：生命周期bug、资源泄漏、悬空引用
- **正确性**：逻辑错误、API使用错误
- **现代化**：现代C++机会、风格改进
- **风格**：命名、格式、可读性

只有可操作的评论。没有工程价值的风格挑剔不算。

## 致谢

- C++ Core Guidelines — Bjarne Stroustrup, Herb Sutter 等
- [Perplexity: Designing, Refining, and Maintaining Agent Skills](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)
