# cpp-ai-constitution

[English](README.md) | **中文**

C++ review skill for AI编程Agent。装一次，到处用。

灵感来自 [superpowers](https://github.com/obra/superpowers) — markdown skills、thin adapters、no runtime。

---

## 安装

```bash
pipx install git+https://github.com/zhxc372/cpp-ai-constitution.git#subdirectory=cli
cd /你的/cpp/项目
cpp-constitution install .
```

然后让AI做review：
```
review src/main.cpp
```

### 免安装（一次性）

```bash
uvx --from git+https://github.com/zhxc372/cpp-ai-constitution.git#subdirectory=cli cpp-constitution install .
```

---

## 它做了什么

**零侵入。** `cpp-constitution install .` 把所有文件放在平台的skill目录内：

```
your-project/
├── .opencode/skills/cpp-core-review/    # ← 所有文件在这里
│   ├── SKILL.md                         # review逻辑
│   ├── project-config.md                # C++版本、构建系统、异常开关
│   ├── references/                      # 详细规则（9个文件）
│   ├── config/                          # clang-tidy配置
│   └── GOTCHAS.md                       # AI常见失败模式
└── opencode.json                        # 平台配置（仅OpenCode）
```

根目录没有配置文件。所有内容在平台的skill目录内。零污染。

---

## 平台支持

| 平台 | 类型 | 安装目标 |
|------|------|---------|
| **OpenCode** | Skill | skill目录 |
| **Claude Code** | Skill | skill目录 |
| **Trae** | Skill | skill目录 |
| **CodeBuddy** | Skill | skill目录 |
| **Gemini CLI** | Skill | skill目录 |
| **Cursor** | Rule | rule文件 |
| **Windsurf** | Rule | rule文件 |
| **GitHub Copilot** | Rule | rule文件 |
| **Amazon Q** | Rule | rule文件 |
| **通义灵码** | Rule | rule文件 |
| **Void** | Rule | rule文件 |
| **Codex CLI** | Generic | AGENTS.md |
| **通用** | Generic | AGENTS.md |

> 具体路径由CLI生成，详见 [INSTALL.md](.opencode/INSTALL.md)。

**Skill型**：SKILL.md + references按需加载（更丰富、结构化）。
**Rule型**：自包含单文件（无需skill加载机制）。
**Generic**：根目录AGENTS.md（仅用于不支持skill/rule的平台）。

---

## 静态分析优先

skill鼓励AI在做主观review之前先跑静态分析：

| 工具 | 检测范围 | 命令 |
|------|---------|------|
| **clang-tidy** | Bug-prone模式、现代化、可读性 | `clang-tidy -p build <file>` |
| **cppcheck** | 缓冲区溢出、内存泄漏、UB | `cppcheck --enable=all <file>` |
| **clazy** | Qt特定反模式 | `clazy -p build <file>` |
| **include-what-you-use** | 不必要的include、前向声明 | `iwyu -p build <file>` |

没装工具？skill会告诉用户：*"纯AI review — 对机械性问题的置信度较低。建议安装 clang-tidy 或 cppcheck。"*

---

## 设计哲学

1. **工具优先** — 静态分析在肉眼审查之前
2. **安全优先于风格** — UB、生命周期、所有权 > 命名、格式
3. **渐进加载** — SKILL.md保持简短，详细规则按需加载
4. **零侵入** — 所有文件在skill目录内，根目录零污染
5. **单一真相源** — 分发仓库从本仓库自动生成

---

## 这不是什么

- 不是C++教程
- 不是C++ Core Guidelines压缩版
- 不是"全部现代化"强制执行工具
- 不是clang-tidy、sanitizer或测试的替代品
- 不是agent framework

每条规则必须证明它的token成本是值得的。

---

## 验证

```bash
# CLI测试
cd cli && python3 tests/test_cli.py

# 仓库验证
python3 scripts/validate_repo.py

# 生成测试项目
cpp-constitution install /tmp/demo --platform opencode --std c++20 --build xmake --no-interact

# 验证零侵入
ls /tmp/demo/  # 应该只有 .opencode/ 和 opencode.json
```

---

## 分发

| 仓库 | 角色 |
|------|------|
| `cpp-ai-constitution` | 真相源：规则、skills、CLI源码 |
| `cpp-constitution` | 分发镜像（自动同步） |

| 渠道 | 状态 |
|------|------|
| `pipx install git+...#subdirectory=cli` | ✅ 主要方式 |
| `uvx --from git+...#subdirectory=cli` | ✅ 支持 |
| PyPI (`pip install cpp-constitution`) | 计划中 |
| ClawHub skill | 计划中（5月23日后） |
| `npx cpp-constitution` | 计划中 |

---

## 许可证

MIT-0
