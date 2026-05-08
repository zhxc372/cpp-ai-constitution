# cpp-ai-constitution

[English](README.md) | **中文**

一个轻量级的面向 AI 的 C++ 工程宪法，灵感来自 C++ Core Guidelines。

本项目**不是** C++ 教程。

它是一个工程约束系统，专为以下工具设计：
- Claude Code
- Cursor
- OpenCode
- OpenClaw
- Gemini CLI
- Codex CLI
- AI 辅助软件工程工作流

目标是：
- 降低 AI 随机性
- 提高一致性
- 强制所有权语义
- 稳定架构
- 降低评审成本
- 减少幻觉编码模式

---

# 理念

强约束降低熵。

大型软件系统通常因为以下原因失败：
- 所有权混乱
- 接口不一致
- 架构漂移
- 隐藏的副作用
- 并发错误
- 风格碎片化

而**不是**因为开发者缺少奇技淫巧。

本仓库将 C++ Core Guidelines 的部分内容转化为：
- AI 可读的规则
- 静态分析约束
- 工程工作流钩子

---

# 目录结构

```text
cpp-ai-constitution/
├── CLAUDE.md              # 最简约束摘要
├── README.md              # 英文说明
├── README_CN.md           # 中文说明
├── docs/rules/            # 详细工程规则
│   ├── core-subset.md     # 核心子集
│   ├── ownership.md       # 所有权规则
│   ├── concurrency.md     # 并发规则
│   ├── error-handling.md  # 错误处理规则
│   └── forbidden-patterns.md  # 禁止模式
├── hooks/                 # 自动化脚本
│   ├── pre-commit.sh      # 提交前检查
│   └── ai-check.sh        # AI 代码扫描
├── config/                # 配置文件
│   ├── .clang-format      # 代码格式化规则
│   └── .clang-tidy        # 静态分析配置
└── prompts/               # AI 提示词
    ├── system-prompt.md   # 系统提示词
    └── review-prompt.md   # 评审提示词
```

---

# 各文件说明

## CLAUDE.md

最简短、最重要的规则摘要。

用途：
- 加载到 AI 上下文中
- 控制代码生成行为
- 降低随机性

可以理解为：
- 工程宪法
- 编码契约
- AI 行为限制器

**此文件应保持简短。**

建议：
- 20~80 行
- 只包含高价值约束

---

## docs/rules/

详细工程规则，按领域划分：
- 所有权（ownership）
- 并发（concurrency）
- API 设计
- 错误处理
- 禁止模式

用途：
- 人类可读
- AI 可引用
- 可逐步扩展

这些文件故意比 CLAUDE.md 长。

---

## config/.clang-format

自动代码格式化规则。

用途：
- 统一风格
- 减少差异噪音
- 简化评审

使用：

```bash
clang-format -i file.cpp
```

---

## config/.clang-tidy

静态分析配置。

用途：
- 检测危险模式
- 强制现代 C++
- 减少缺陷

检查包括：
- cppcoreguidelines
- modernize
- performance
- concurrency
- bugprone

使用：

```bash
clang-tidy file.cpp --config-file=config/.clang-tidy -- -std=c++20
```

---

## hooks/

自动化脚本。

用途：
- 自动运行检查
- 减少人工评审负担
- 为 AI 创建反馈闭环

### pre-commit.sh

运行：
- clang-format
- clang-tidy

### ai-check.sh

扫描所有 cpp/hpp 文件。

使用：

```bash
chmod +x hooks/*.sh
./hooks/pre-commit.sh
```

---

## prompts/

AI 代理可复用的提示词。

### system-prompt.md

定义：
- 编码风格
- 生成约束
- 工程优先级

### review-prompt.md

定义：
- 评审检查清单
- 架构评审逻辑
- 所有权/并发检查

---

# 推荐工作流

## 第一步 — 复制文件到你的项目

复制：

```text
CLAUDE.md
docs/rules/
config/
hooks/
```

到你的仓库根目录。

示例：

```text
my-project/
├── CLAUDE.md
├── src/
├── docs/
├── config/
└── hooks/
```

---

## 第二步 — 配置你的 AI 编码工具

### Claude Code

告诉 Claude：

```text
Follow CLAUDE.md and docs/rules/*.md.
```

### Cursor

创建：

```text
.cursor/rules/cpp.mdc
```

引用：
- CLAUDE.md
- docs/rules/

### OpenCode / OpenClaw

注入：
- CLAUDE.md
- prompts/system-prompt.md

到系统上下文中。

---

## 第三步 — 安装工具链

Linux/macOS：

```bash
sudo apt install clang-format clang-tidy
```

或者：

```bash
brew install llvm
```

验证：

```bash
clang-format --version
clang-tidy --version
```

---

## 第四步 — 运行钩子

```bash
chmod +x hooks/*.sh
./hooks/pre-commit.sh
```

流程：

```text
AI 生成代码
↓
clang-format
↓
clang-tidy
↓
构建/测试
↓
AI 修复问题
↓
提交
```

---

# 推荐的 AI 工作方式

## 好的模式

```text
需求规格
↓
架构设计
↓
CLAUDE.md
↓
小任务拆分
↓
AI 生成
↓
检查
↓
评审
```

## 坏的模式

```text
巨大而模糊的提示词
↓
AI 写了 5000 行
↓
没有任何检查
↓
架构混乱
```

---

# 重要设计原则

**不要**把整个 C++ Core Guidelines 放进上下文。

太大。太吵。太哲学。

应该这样做：

```text
CppCoreGuidelines
↓
筛选
↓
压缩
↓
转化为工程约束
↓
AI 可读的宪法
```

---

# 最佳实践

使用**三层**结构：

| 层级 | 用途 |
|---|---|
| CLAUDE.md | 简短的高价值约束 |
| docs/rules | 详细工程规则 |
| 原始 Guidelines | 仅作为人类参考 |

---

# 未来扩展

可以演进为：
- 嵌入式宪法
- 游戏服务器宪法
- 异步/协程宪法
- Qt 宪法
- 低延迟宪法
- 分布式系统宪法
- 代理中立宪法

---

# 最后的话

软件工程的未来不是：

"AI 写一切。"

而是：

"人类定义约束。
AI 在约束内运作。"
