# Phase 0 模板：用 C++ AI 宪法启动真实项目

> 本模板是 cpp-ai-constitution 的实战启动指南。
> 目标：验证宪法能否约束 AI 进行可靠开发，而不是完成整个项目。

---

## 使用方法

1. 把本模板复制到你的 C++ 项目根目录
2. 按 Phase 0 执行，验证宪法生效
3. 完成后再进入后续 Phase

---

## Phase 0 目标

验证 C++ AI 宪法是否能约束 AI 进行可靠开发。

## 非目标

- ❌ 完成整个项目
- ❌ 实现外围 UI、配置系统、插件系统、复杂框架
- ❌ 大规模编码
- ❌ 用 TODO 冒充完成

---

## 第一步：建立最小项目骨架

请 AI 执行以下结构创建：

```
project/
├── constitution.md              # 项目级宪法（从 cpp-ai-constitution 适配）
├── project_rules.compiled.md    # 编译后的项目规则
├── docs/
│   ├── spec.md                  # 功能规格
│   ├── plan.md                  # 开发计划
│   └── phase_0.md               # Phase 0 定义
├── CMakeLists.txt               # 构建系统
├── src/                         # 源码
├── include/                     # 头文件
├── tests/                       # 测试
└── scripts/
    └── validate.sh              # 验证脚本
```

---

## 第二步：定义 phase_0.md

phase_0.md 必须包含：

| 字段 | 内容 |
|------|------|
| 本阶段目标 | 一句话说明 Phase 0 要完成什么 |
| 非目标 | 明确列出不在本阶段做的事 |
| 可交付物 | 文件列表 + 每个文件的验收条件 |
| 验收标准 | 可运行、可测试、可验证的具体标准 |
| 禁止事项 | 不允许的行为（如 TODO 冒充、绕过测试等） |

---

## 第三步：实现第一个最小闭环

- 第一条功能必须是最小核心闭环
- 不允许实现外围功能
- 所有代码必须：可编译、有测试、可运行验证脚本
- 不允许用 TODO 冒充完成

---

## 执行原则（AI 必须遵守）

1. **不扩功能**，不做大而全架构
2. 每次修改代码后，必须说明：
   - 修改了哪些文件
   - 为什么修改
   - 如何验证
   - 是否违反 constitution.md
3. 如果需求不清楚，**不允许自由发挥**，只能先生成 spec 草案和待确认问题
4. 遵循 cpp-ai-constitution 的全部约束：
   - Tool First（先找构建系统、先跑 clang-tidy）
   - Ownership Classification（改指针前先分类）
   - Safety Before Style
   - 不混合 modernization 和 safety fix

---

## 第四步：验证

完成后运行：

```bash
# 构建
cmake -B build -S .
cmake --build build

# 测试
ctest --test-dir build --output-on-failure

# 静态检查（如果有 clang-tidy）
python3 /path/to/cpp-ai-constitution/scripts/run_clang_tidy.py --build-dir build

# 项目验证
bash scripts/validate.sh
```

---

## Prompt 模板

直接复制以下内容给 AI 开始：

```
你现在要帮助我用 cpp-ai-constitution 实战启动一个真实 C++ 项目。

本轮目标不是完成整个项目，而是完成 Phase 0：验证 C++ AI 宪法是否能约束 AI 进行可靠开发。

请严格执行以下原则：

1. 不扩功能，不做大而全架构。
2. 先建立最小项目骨架：
   - constitution.md
   - project_rules.compiled.md
   - docs/spec.md
   - docs/plan.md
   - docs/phase_0.md
   - CMakeLists.txt
   - src/
   - include/
   - tests/
   - scripts/validate.sh
3. phase_0.md 必须定义：
   - 本阶段目标
   - 非目标
   - 可交付物
   - 验收标准
   - 禁止事项
4. 第一条功能必须是最小核心闭环，不允许实现外围 UI、配置系统、插件系统、复杂框架。
5. 所有代码必须：
   - 可编译
   - 有测试
   - 可运行验证脚本
   - 不允许用 TODO 冒充完成
6. AI 每次修改代码后，必须说明：
   - 修改了哪些文件
   - 为什么修改
   - 如何验证
   - 是否违反 constitution.md
7. 如果需求不清楚，不允许自由发挥，只能先生成 spec 草案和待确认问题。
8. 完成后运行：
   - cmake configure
   - build
   - tests
   - clang-tidy 或等价静态检查
   - scripts/validate.sh

请先生成 Phase 0 项目骨架与第一个最小任务，不要直接开始大规模编码。
```

---

## 宪法适配说明

将 cpp-ai-constitution 的核心约束复制到项目的 `constitution.md`，并根据项目特点调整：

- 如果项目禁用异常 → 在 project_rules.compiled.md 明确
- 如果项目有特殊 ABI 约束 → 明确
- 如果项目是 C++17 → 明确标准版本

**核心规则只做减法，不做加法。** 宪法约束越少越好，但每条都必须有理由。
