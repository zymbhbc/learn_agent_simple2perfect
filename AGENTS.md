# AGENTS.md

## 项目定位

本项目用于系统学习并实现一套教学型 Agent Harness，同时维护可运行代码、自动化测试、Agent 行为评测、设计文档、学习教程和验收证据。

首版采用 Python 3.12+，核心实现覆盖模型适配、工具系统、Agent Loop、状态管理、上下文工程、权限控制、持久化、可观测性和评测。

## 全局规则

- 与用户沟通、项目文档和学习记录使用中文，优先使用英文标点符号。
- Python 标识符、模块名、类型名、命令名和配置键使用英文。
- 代码注释与 docstring 使用简洁英文，说明意图、约束和非显然原因。
- 文档、注释、标题和交付说明采用最终态表达，直接描述当前对象、能力、条件和操作。
- 只读取当前任务需要的文件，只创建当前任务需要的内容，保持改动范围聚焦。
- 保留用户已有改动；出现重叠修改时先理解内容，再进行最小范围编辑。
- 未经用户明确要求，不创建提交、标签、分支或发布版本。

## 指令路由

根规则始终适用。任务涉及以下目录时，在操作前读取对应的 `AGENTS.md`：

| 任务范围 | 目录规则 |
| --- | --- |
| 计划、教程、设计和 ADR | `docs/AGENTS.md` |
| 用户个人笔记 | `notes/AGENTS.md` |
| 论文、规范和外部资料 | `references/AGENTS.md` |
| 每日学习与开发日志 | `logs/AGENTS.md` |
| 功能和知识验收 | `verification/AGENTS.md` |
| Python 产品代码 | `src/AGENTS.md` |
| 确定性自动化测试 | `tests/AGENTS.md` |
| Agent 行为评测 | `evals/AGENTS.md` |
| 可运行示例 | `examples/AGENTS.md` |
| 开发与数据脚本 | `scripts/AGENTS.md` |

同一任务涉及多个范围时，读取全部相关目录规则。目录规则只补充本目录约束；发生冲突时，以更深目录规则和用户当前要求为准。

## 仓库结构

```text
learn_agent_simple2perfect/
├── AGENTS.md
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── docs/{plans,tutorials,design/adr}/
├── notes/
├── references/
├── logs/YYYY/MM/
├── verification/{code,knowledge}/
├── src/agent_harness/{core,providers,tools,policy,context,storage,telemetry,cli}/
├── tests/{unit,integration,security}/
├── evals/{cases,fixtures,evaluators}/
├── examples/
└── scripts/
```

运行时数据、缓存、密钥、本地数据库、大模型原始输出和临时产物进入被 Git 忽略的 `.local/` 或系统临时目录。

## 通用命名

- Python 包、模块、函数和变量使用 `snake_case`，类使用 `PascalCase`，常量使用 `UPPER_SNAKE_CASE`。
- Markdown 文件名使用小写 `kebab-case`，日期使用 ISO 8601 格式 `YYYY-MM-DD`。
- 配置、事件和持久化 schema 包含显式版本字段。
- 同一概念在代码、文档、测试和 CLI 中使用统一术语。

## 安全与质量边界

- 密钥从环境变量或受控凭据存储读取，不进入源码、日志、trace、fixture 和提交历史。
- 模型输出、工具参数、文件内容和外部响应均作为不可信输入完成校验。
- 写入、执行和网络副作用经过策略判断，并在需要时进入审批流程。
- 文件工具规范化路径并确认目标位于允许的工作区内。
- 时间、步骤、token、费用、结果大小、并发数和进程执行具有明确预算。

## 开发命令

项目工具配置完成后使用统一命令：

```powershell
uv sync --dev
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
```

开发过程中运行受影响范围的检查，交付前运行与改动风险相匹配的完整检查。

## 变更管理

- 提交信息采用 Conventional Commits，例如 `feat: 支持工具注册`、`test: 增加路径逃逸用例`、`docs: 编写 Agent Loop 教程`。
- 每次提交聚焦一个完整意图，代码、测试和直接相关文档共同提交。
- `CHANGELOG.md` 按 Added、Changed、Fixed、Security 分类记录版本能力变化。
- 日常开发事实写入 `logs/`，长期设计结论写入 `docs/design/`，通用知识写入 `docs/tutorials/`。

## 工作流程

1. 读取当前任务直接相关的目录规则、代码、测试和文档。
2. 明确预期行为、边界和可验证完成条件。
3. 实现最小完整改动，保持模块职责和依赖方向。
4. 更新相关测试、评测、文档和验收证据。
5. 运行相关检查，修复当前改动造成的失败。
6. 检查敏感信息、临时产物、术语一致性和最终态表达。
7. 交付实际改动、验证结果、已知风险和需要用户决策的事项。

## 完成标准

- 实现行为符合目标和安全边界。
- 代码通过相关格式、静态检查和测试。
- Agent 行为变化具有对应评测结果。
- 公共接口、设计、示例和教程保持一致。
- 验收结论具有可复现证据。
- 仓库内容具有明确用途和许可条件。

## 规范来源

- [OpenAI model guidance: Using agents.md](https://developers.openai.com/api/docs/guides/latest-model): 多层指令的发现、合并和优先级。
- [OpenAI Developers: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): 精简根指令并按任务读取相关资料。
- [AGENTS.md](https://agents.md/): 编码智能体项目说明格式。
