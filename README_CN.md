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
├── assets/                     # 模板
├── hooks/                      # Git钩子
├── config/                     # 工具配置
├── prompts/                    # AI提示词
└── evals/                      # Skill路由测试
```

## 快速开始

```bash
cp -r SKILL.md CLAUDE.md GOTCHAS.md references/ scripts/ assets/ hooks/ config/ prompts/ /你的项目/
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

## 致谢

- C++ Core Guidelines — Bjarne Stroustrup, Herb Sutter 等
- [Perplexity: Designing, Refining, and Maintaining Agent Skills](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity)
