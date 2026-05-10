# Decision Rights

> 本文件定义 AI、人类、脚本、适配层在 cpp-ai-constitution 项目中的权力边界。

---

## AI May

- Inspect project structure（检查项目结构）
- Run deterministic scripts（运行确定性脚本）
- Summarize clang-tidy / compiler / sanitizer findings（总结工具发现）
- Classify ownership candidates（分类 ownership）
- Identify UB / lifetime / concurrency risks（识别风险）
- Propose refactor plans（提出重构方案）
- Generate review reports（生成审查报告）
- Propose rule patches（提出规则修改建议）
- Generate eval case candidates（生成测试用例候选）

## AI Must Not

- Mechanically replace raw pointers（机械替换裸指针）
- Modernize before preserving behavior（行为未保先现代化）
- Mix safety and style changes（混合安全和风格修改）
- Change ABI assumptions without approval（未经批准改 ABI）
- Change exception policy without approval（未经批准改异常策略）
- Treat missing build context as certainty（把缺构建上下文当确定性）
- Modify core constitution without human review（未经审查改宪法）
- Approve its own rule changes（自我批准规则变更）
- Delete or relax safety constraints（删除或放宽安全约束）

## Human Must Decide

- Ownership model changes（所有权模型变更）
- API compatibility trade-offs（API 兼容性权衡）
- ABI constraints（ABI 约束）
- Exception strategy（异常策略）
- Performance trade-offs（性能权衡）
- Whether to apply suggested patches（是否应用建议的补丁）
- Whether to accept a new core rule（是否接受新核心规则）
- Constitution changes（宪法变更）

## Scripts Should Decide

- Whether code compiles（是否编译通过）
- Whether tests pass（是否测试通过）
- Whether clang-tidy passes（是否通过 clang-tidy）
- Whether format is correct（格式是否正确）
- Whether required files exist（必需文件是否存在）
- Whether adapters are in sync（适配器是否同步）

## Adapters Should Only

- Translate core rules to platform format（翻译核心规则为平台格式）
- Wrap commands for platform invocation（包装命令调用）
- Adjust trigger phrases for platform（调整触发短语）
- Map directory structure for platform（映射目录结构）

Adapters must never:

- Invent new principles（发明新原则）
- Delete core principles（删除核心原则）
- Bypass tests（绕过测试）
- Produce different rule standards per platform（每个平台产生不同规则标准）
