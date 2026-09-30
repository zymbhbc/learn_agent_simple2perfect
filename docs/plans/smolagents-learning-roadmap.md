# smolagents 学习与 Agent Harness 实践计划

## 计划信息

- 状态：`planned`
- 创建日期：2026-09-28
- 最近更新：2026-09-28
- 学习基线：smolagents v1.26.0 稳定文档
- 预计投入：51—69 小时
- 推荐节奏：每次 60—90 分钟，每周完成 3—5 次学习任务
- 最终产出：一个借鉴 smolagents 核心思想、由本项目独立实现的只读代码仓库 Agent Harness

## 学习目标

完成本计划后，应具备以下能力：

1. 解释 Agent、Model、Tool、Memory、Executor 和 Agent Loop 的职责与协作关系。
2. 使用 smolagents 创建 `ToolCallingAgent` 和 `CodeAgent`，并分析完整运行轨迹。
3. 阅读 smolagents 的关键源码，定位模型调用、工具执行、状态更新和停止条件。
4. 独立实现模型接口、工具注册、运行循环、事件记录、预算和错误处理。
5. 识别代码执行、文件访问、网络请求和凭据使用中的安全边界。
6. 使用确定性测试与固定评测集验证 Agent 行为。
7. 完成一个可运行、可观察、可测试的最小 Agent Harness。

## 学习范围

### 核心范围

- Agent 基础概念与 Think → Act → Observe 循环。
- smolagents 的 Model、Tool、MultiStepAgent、Memory 和 Python Executor。
- `ToolCallingAgent` 与 `CodeAgent` 的动作表达和执行差异。
- 工具 schema、输入校验、输出处理和错误反馈。
- 最大步骤、停止条件、planning、callback、日志和运行轨迹。
- fake model、单元测试、集成测试和 Agent 行为评测。
- 自研只读代码仓库 Agent Harness。

### 后续扩展

- Gradio UI 与 Hugging Face Spaces 发布。
- 视觉、音频和浏览器 Agent。
- MCP 工具接入。
- RAG 与长期记忆。
- 多种远程 sandbox 平台。
- 大规模多 Agent 编排。

这些扩展在最小 Harness 闭环完成后按实际需要进入独立计划。

## 学习阶段总览

| 阶段 | 主题 | 预计时间 | 核心产出 | 状态 |
| --- | --- | ---: | --- | --- |
| 0 | 环境与 Agent 基础 | 2—3h | 环境检查、概念自测 | `planned` |
| 1 | 第一个 smolagents Agent | 3—4h | ToolCallingAgent 最小示例 | `planned` |
| 2 | Tool 工具系统 | 5—7h | 三个只读工具 | `planned` |
| 3 | Model 与消息结构 | 5—7h | 模型调用观察器、fake model | `planned` |
| 4 | MultiStepAgent、Loop 与 Memory | 8—10h | 状态机、自研最小循环 | `planned` |
| 5 | CodeAgent 与安全执行 | 7—9h | 执行边界实验、威胁分析 | `planned` |
| 6 | Planning、Callback 与组合 | 5—7h | 运行事件、受控多 Agent 示例 | `planned` |
| 7 | 测试、评测与可观测性 | 6—8h | 固定评测集、对比报告 | `planned` |
| 8 | 自研最小 Agent Harness | 10—14h | 只读代码仓库助手 | `planned` |

## 执行方法

每个阶段采用相同的学习闭环：

1. 阅读对应官方教程，记录需要回答的问题。
2. 运行最小示例，观察输入、输出和运行轨迹。
3. 阅读关键源码，画出对象关系或调用链。
4. 关闭源码，使用自己的接口完成最小实现。
5. 编写自动化测试，并主动注入一个失败场景。
6. 在 `verification/knowledge/` 中用自己的语言完成知识验收。
7. 在 `verification/code/` 中记录运行命令、结果和证据路径。
8. 将可复用知识整理到 `docs/tutorials/`，将当天事实写入 `logs/`。

每个阶段通过全部验收条件后进入下一阶段。

## 阶段 0：环境与 Agent 基础

### 目标

建立运行 smolagents 示例所需的最小环境，理解 Agent 的基本组成和循环。

### 前置知识

- Python 函数、类、异常和类型标注。
- 基本命令行操作。
- LLM 的 prompt、message 和 response 概念。

### 学习任务

- [ ] 用自己的语言解释 LLM 与 Agent 的关系。
- [ ] 理解 Think、Act、Observe 三类步骤。
- [ ] 理解 Model、Tool、Memory、Executor 的基本职责。
- [ ] 安装并锁定 smolagents v1.26.0 学习环境。
- [ ] 确认密钥通过环境变量提供。
- [ ] 运行一个纯模型调用，观察请求和响应。

### 项目产出

- `pyproject.toml`: Python 版本、smolagents 和开发工具配置。
- `docs/tutorials/agent-fundamentals.md`: Agent 基础概念教程。
- `verification/knowledge/stage-00-agent-fundamentals.md`: 概念自测记录。

### 验收标准

- 能画出用户输入到 Agent 最终输出的基本流程。
- 能解释工具为何需要 name、description、inputs 和 output type。
- 能区分模型生成内容与 Harness 执行动作。
- 环境安装命令可以重复执行。

## 阶段 1：第一个 smolagents Agent

具体会话与验收安排见 [阶段 1: 第一个 ToolCallingAgent 学习安排](stage-01-first-tool-calling-agent.md)。

### 目标

从使用者角度掌握 smolagents 的最小运行方式，建立结构化工具调用的直观认识。

### 学习任务

- [ ] 阅读官方 Guided Tour 的 Agent 构建部分。
- [ ] 创建一个带单个确定性工具的 `ToolCallingAgent`。
- [ ] 观察 system prompt、模型输出、工具调用和 final answer。
- [ ] 使用 `max_steps` 制造一次预算终止。
- [ ] 使用 `agent.replay()` 回放运行轨迹。
- [ ] 画出一次 ToolCallingAgent 运行的数据流。

### 项目产出

- `examples/01-first-tool-calling-agent.py`
- `docs/tutorials/first-smolagents-agent.md`
- `verification/knowledge/stage-01-agent-types.md`

### 验收标准

- 示例能够调用确定性工具并返回最终回答。
- 能解释结构化工具调用中的工具名称、参数和结果。
- 能在 replay 中指出 thought、action、observation 和 final answer。
- 能说明 `max_steps` 对运行终止的影响。

## 阶段 2：Tool 工具系统

具体会话与验收安排见 [阶段 2: Tool 工具系统学习安排](stage-02-tool-system.md)。

### 目标

理解工具如何向模型暴露能力，并掌握工具描述、schema、校验和错误反馈。

### 源码入口

- `src/smolagents/tools.py`
- `Tool`、`BaseTool`、`@tool` 与工具调用相关实现。

### 学习任务

- [ ] 使用 `@tool` 创建一个简单工具。
- [ ] 使用 `Tool` 子类创建同等能力的工具。
- [ ] 比较装饰器和类两种定义方式。
- [ ] 分析 name、description、inputs、output type 如何进入 prompt。
- [ ] 分别注入缺少参数、错误类型、工具内部异常和超大输出。
- [ ] 实现 `list_files`、`search_text`、`read_file` 三个只读工具。
- [ ] 为三个工具编写独立单元测试。

### 项目产出

- `examples/03-custom-tools.py`
- `docs/tutorials/smolagents-tool-system.md`
- `verification/code/stage-02-tools.md`
- `verification/knowledge/stage-02-tools.md`

### 验收标准

- 三个工具只能读取指定测试工作区。
- 非法参数产生清晰、可处理的错误。
- 能预测修改工具 description 对模型选择行为的影响。
- 能独立写出一个包含完整 schema 的工具。

## 阶段 3：Model 与消息结构

### 目标

理解 smolagents 如何统一不同模型提供商，并识别 Harness 与模型 API 之间的适配边界。

### 源码入口

- `src/smolagents/models.py`
- `Model`、API 模型基类、消息与工具调用相关类型。

### 学习任务

- [ ] 观察一次完整模型请求中的 messages、tools 和参数。
- [ ] 比较普通文本响应与工具调用响应。
- [ ] 分析 provider 响应转换为内部消息的过程。
- [ ] 记录 token usage、停止原因和错误信息。
- [ ] 创建一个能够返回固定响应的 fake model。
- [ ] 使用 fake model 驱动确定性的工具调用轨迹。
- [ ] 归纳内部模型接口需要保留的最小字段。

### 项目产出

- `examples/04-model-observer.py`
- `tests/unit/test_fake_model.py`
- `docs/tutorials/model-and-messages.md`
- `verification/knowledge/stage-03-model-adapter.md`

### 验收标准

- 能画出 provider API 与 Agent 内部消息之间的转换过程。
- fake model 能产生普通回答、工具调用和错误三种结果。
- 测试无需真实网络和真实模型即可重复运行。
- 能解释厂商响应对象为何需要在适配器边界完成转换。

## 阶段 4：MultiStepAgent、Agent Loop 与 Memory

### 目标

掌握 smolagents 最核心的多步运行循环，并独立实现一个最小 ToolCalling Agent Loop。

### 源码入口

- `src/smolagents/agents.py`
- `src/smolagents/memory.py`
- `MultiStepAgent`、`ToolCallingAgent`、`AgentMemory` 和各类 Memory Step。

### 学习任务

- [ ] 从 `run()` 入口追踪一次完整执行流程。
- [ ] 标注模型调用、动作解析、工具执行、观察回填和终止位置。
- [ ] 理解 `TaskStep`、`ActionStep`、`PlanningStep` 和 `FinalAnswerStep`。
- [ ] 分析 `max_steps`、final answer 和异常如何产生终态。
- [ ] 分析 `reset`、`replay` 和 memory message 构造。
- [ ] 画出 Agent Loop 状态机。
- [ ] 使用 fake model 独立实现一个最小循环。
- [ ] 测试正常结束、未知工具、工具失败和步骤耗尽。

### 项目产出

- `docs/design/agent-loop-state-machine.md`
- `docs/tutorials/smolagents-agent-loop.md`
- `src/agent_harness/core/` 中的最小运行类型与循环。
- `tests/unit/` 中的循环和状态测试。
- `verification/code/stage-04-agent-loop.md`
- `verification/knowledge/stage-04-agent-loop.md`

### 验收标准

- 能脱离源码画出完整状态机。
- 能解释每种 Memory Step 的产生位置和用途。
- 最小循环能够完成“模型 → 工具 → 观察 → 模型 → 最终回答”。
- 所有停止原因具有稳定类型和确定性测试。

## 阶段 5：CodeAgent 与安全执行

### 目标

理解代码动作的表达能力、执行器接口和隔离要求，建立自研 Harness 的执行安全边界。

### 源码入口

- `CodeAgent` 相关实现。
- `src/smolagents/local_python_executor.py`
- `PythonExecutor` 与不同 executor 类型。

### 学习任务

- [ ] 比较 Python 代码动作与 JSON 工具调用的轨迹。
- [ ] 创建一个仅执行纯计算任务的最小 `CodeAgent`。
- [ ] 分析工具如何绑定为代码执行环境中的函数。
- [ ] 理解 authorized imports、timeout 和输出长度限制。
- [ ] 观察变量状态如何在多步代码执行间保存。
- [ ] 使用纯计算任务测试本地执行器。
- [ ] 分析本地执行器、容器执行器和远程 sandbox 的信任边界。
- [ ] 完成路径访问、危险 import、超时和超大输出故障实验。
- [ ] 编写项目的代码执行威胁模型。

### 项目产出

- `examples/05-first-code-agent.py`
- `docs/design/code-execution-threat-model.md`
- `docs/tutorials/code-agent-and-executor.md`
- `tests/security/` 中的执行安全用例。
- `verification/code/stage-05-code-execution.md`

### 验收标准

- 能解释本地受控执行器与安全 sandbox 的能力边界。
- 能指出生成代码拥有的文件、网络、进程和 import 能力。
- 超时、危险 import 和超大输出均具有可复现结果。
- 能根据任务风险选择 ToolCallingAgent 或 CodeAgent。

## 阶段 6：Planning、Callback 与 Agent 组合

### 目标

理解计划步骤、运行回调、流式观察和受控的 Agent 组合方式。

### 学习任务

- [ ] 配置 `planning_interval` 并观察 PlanningStep。
- [ ] 使用 step callback 收集每一步事件。
- [ ] 记录步骤耗时、模型调用和工具调用结果。
- [ ] 测试 interrupt 和运行取消行为。
- [ ] 创建一个 manager agent 与一个只读搜索 agent。
- [ ] 观察 managed agent 的 name、description、输入和结果摘要。
- [ ] 比较单 Agent 与双 Agent 完成同一任务的步骤和上下文。

### 项目产出

- `examples/06-planning-and-callbacks.py`
- `examples/07-managed-agent.py`
- `docs/tutorials/planning-callbacks-and-managed-agents.md`
- `verification/knowledge/stage-06-agent-composition.md`

### 验收标准

- callback 能产生结构化步骤事件。
- 能解释 planning 对步骤数量和上下文的影响。
- managed agent 只获得完成其任务所需的工具和输入。
- 能根据对比结果说明 Agent 组合的实际收益与成本。

## 阶段 7：测试、评测与可观测性

### 目标

建立可重复的 Agent 行为验证体系，用数据比较实现和配置变化。

### 学习任务

- [ ] 使用 scripted fake model 构造固定运行轨迹。
- [ ] 为工具选择、参数、步骤、终态和错误编写断言。
- [ ] 建立 10—15 个只读仓库任务。
- [ ] 记录成功率、工具参数正确率、平均步骤和延迟。
- [ ] 在可用条件下记录 token 和费用。
- [ ] 比较 ToolCallingAgent 与 CodeAgent 的任务表现。
- [ ] 评估修改工具描述前后的结果。
- [ ] 输出一份可重复生成的评测报告。

### 项目产出

- `evals/cases/` 中的固定任务集。
- `evals/fixtures/` 中的小型测试仓库。
- `evals/evaluators/` 中的确定性评分器。
- `verification/code/stage-07-evaluation.md`
- `docs/tutorials/agent-testing-and-evaluation.md`

### 验收标准

- 评测集能够无交互重复运行。
- 每个失败可定位到模型、工具、循环或上下文步骤。
- 对比报告包含样本数、配置、结果和可复现命令。
- 能使用评测结果判断一项修改是否值得保留。

## 阶段 8：自研最小 Agent Harness

### 目标

将学习所得组合成一个独立实现的只读代码仓库助手，并与 smolagents 实现进行对照。

### 功能范围

- 一个模型提供商适配器和一个 fake provider。
- `list_files`、`search_text`、`read_file` 三个只读工具。
- 显式 Agent Loop 和稳定运行状态。
- 步数、时间、token 和结果大小预算。
- JSONL 运行事件。
- CLI 入口。
- 单元测试、集成测试、安全测试和固定评测集。

### 学习任务

- [ ] 定义内部 Message、ToolCall、ToolResult、RunEvent 和 StopReason。
- [ ] 实现 ModelProvider 与 ToolRegistry。
- [ ] 实现 Agent Loop 与运行预算。
- [ ] 实现工作区路径边界和工具结果限制。
- [ ] 将运行事件写入 JSONL。
- [ ] 实现 CLI 并显示最终回答与运行摘要。
- [ ] 运行固定评测集。
- [ ] 与 smolagents 版本比较接口、轨迹、测试和扩展成本。
- [ ] 完成第一份架构决策记录。

### 项目产出

- `src/agent_harness/` 中的最小实现。
- `tests/` 中的完整测试集。
- `evals/` 中的固定回归集。
- `docs/design/architecture.md`
- `docs/design/adr/0001-minimal-harness-boundary.md`
- `verification/code/stage-08-minimal-harness.md`
- `verification/knowledge/stage-08-capstone-review.md`

### 验收标准

- CLI 能回答“某个功能在哪里实现”并给出文件与行号证据。
- 所有文件访问限定在指定工作区。
- 无限工具调用在预算边界可靠终止。
- 运行轨迹能够重放并定位失败步骤。
- 固定评测集生成成功率、步骤、延迟和安全结果。
- 能说明自研实现从 smolagents 借鉴的设计及本项目形成的独立边界。

## 阶段验收模板

每个阶段完成后，在对应 `verification/` 文件中填写：

```markdown
# 阶段 N 验收：主题

- 状态：passed | failed | blocked
- 确认日期：YYYY-MM-DD
- 学习目标：
- 实际产出：
- 运行命令：
- 测试与评测结果：
- 故障实验：
- 调用链或状态图：
- 核心机制解释：
- 与 smolagents 的对照：
- 当前结论：
- 下一阶段前置问题：
```

## 学习调整规则

- 某阶段验收未通过时，将失败项拆成一次 60—90 分钟的补充任务。
- Python 基础成为阻塞项时，在当前阶段插入对应专题练习。
- 模型费用或访问条件受限时，使用 fake model 完成机制学习和测试。
- 源码 API 与本计划不一致时，以锁定版本源码为准，并在计划中记录版本。
- 每完成两个阶段进行一次回顾，调整后续任务的深度和投入时间。

## 参考资料

- Hugging Face, [smolagents documentation](https://huggingface.co/docs/smolagents/index), 访问日期：2026-09-28。
- Hugging Face, [Agents - Guided tour](https://huggingface.co/docs/smolagents/guided_tour), 访问日期：2026-09-28。
- Hugging Face, [Agents reference](https://huggingface.co/docs/smolagents/reference/agents), 访问日期：2026-09-28。
- Hugging Face, [Tools reference](https://huggingface.co/docs/smolagents/reference/tools), 访问日期：2026-09-28。
- Hugging Face, [Manage your agent's memory](https://huggingface.co/docs/smolagents/tutorials/memory), 访问日期：2026-09-28。
- Hugging Face, [Secure code execution](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution), 访问日期：2026-09-28。
- Hugging Face, [Python code executors](https://huggingface.co/docs/smolagents/en/reference/python_executors), 访问日期：2026-09-28。
- Hugging Face, [smolagents source repository](https://github.com/huggingface/smolagents), 访问日期：2026-09-28。
- Hugging Face, [AI Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction), 访问日期：2026-09-28。
