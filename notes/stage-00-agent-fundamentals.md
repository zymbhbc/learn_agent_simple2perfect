# 阶段 0 笔记: 环境与 Agent 基础

- 日期: 2026-09-28
- 关联计划: `docs/plans/smolagents-learning-roadmap.md` 阶段 0
- 预计投入: 2—3h
- 状态: 进行中

## 标注约定

- 【我的理解】 用自己当前的语言写, 即使不准确也保留原样, 之后用横线补充修正, 不直接删除。
- 【疑问】 学习过程中产生的开放问题, 解决后回填结论并注明来源。
- 【外部事实】 来自文档或实验结果的客观陈述, 必须附来源链接和访问日期。
- 【AI 推断】 AI 给出的解释或观点, 需要自行核验后才作为结论。
- 【观察】 运行命令后的实际输出摘录或现象描述。

---

## 一、概念理解

### 1. LLM 与 Agent 的关系

【我的理解】

- 现在的LLM本质上是指各种API的模型调用，主要接口类型包含OpenAI类型和Anthropic类型，具体调用方式可以是通过Ollama或者vLLM框架部署的本地模型，也可以是使用url+api-key方式的网络调用
- Agent通俗来说是LLM外面套的一层壳，Agent的出现实际上是一个演化的过程
  - 在大模型刚出来的时候，人通过对话来指导大模型来完成对应的任务，这个对话或者是指令，为了构建对话更快，重复性的知识通过抽象形成了Prompt工程，这构成了Agent的第一大部分。同时Prompt也是大模型补充先验知识不足重要的手段
  - 大模型可以生成调用函数的脚本或者是运行函数的参数，这是Agent中能使用工具的根本原则
  - 大模型的上下文窗口有限，通过不断叠加上下文对话然后输入到模型的方式会导致模型的上下文溢出，而且会话历史保存在缓存中，当运行结束会话历史就消失了，因此需要持久化存储和上下文管理让宝贵的token用在有用的信息上
- 因此可以说Agent就是以上拓展大模型能力的工程化集合，本质上就是通过工程化的手段修改输入到大模型中的指令
- 然而单纯的Agent还不足以达到生产级别的Agent，为了约束React Agent在实际生产中的表现和安全边界，Agent Harness通过沙箱、审查和自我评估来约束Agent

【AI 补充与校正】

- LLM 是经过训练的参数化模型。OpenAI-compatible API、Anthropic Messages API 是服务接口，Ollama、vLLM 是模型运行与服务组件；它们属于模型的访问和部署层。
- Agent 的关键特征是模型输出能够影响后续控制流，例如选择工具、生成参数、决定是否继续循环或调整计划。Prompt 是 Agent 的组成部分，工具、状态、循环、解析、权限和执行环境同样属于 Agent 系统。
- Prompt 中提供的是当前请求可用的上下文、指令和示例，属于 in-context information。模型训练形成的参数知识与运行时上下文是两个层次。
- 会话历史的保存位置由具体 API 与 Harness 决定。它可以由客户端重传、服务端 session 保存或写入持久化存储；“缓存”和“持久化会话”是不同机制。
- Agent Harness 是承载 Agent 运行的工程基础设施，负责模型与工具循环、session、执行环境、权限、预算、事件和观测。它与 Agent 关系紧密，但职责层次不同。


【疑问】

- 广义上的Agent到底是什么？Agent Harness现在是不是可以指代Agent？一个确定好的工作流也可以是Agent吗？

【疑问解答】

- 广义 Agent：一个由模型参与决策、能够感知当前状态并通过动作推进目标的系统。Hugging Face 给出的操作性定义是“LLM 输出控制工作流的程序”，并将 agency 视为连续程度。
- Agent 与 Harness：Agent 表达目标、指令、模型、工具和行为策略；Harness 负责把这些行为可靠地运行起来。日常交流中两者有时会合称 Agent，进行架构设计时应分别建模。
- 确定工作流：控制路径由代码预先确定时，可称为 workflow 或 agentic workflow。模型根据中间结果自主决定步骤和循环时，更符合 agent 的定义。一个工作流可以包含 Agent 节点，Agent 也可以调用确定工作流。

【外部事实】(附来源与访问日期)

- Hugging Face 将 AI Agent 定义为“LLM 输出控制工作流的程序”，并使用 LLM 对控制流的影响程度描述 agency。[What are agents?](https://huggingface.co/docs/smolagents/conceptual_guides/intro_agents)，访问日期：2026-09-28。
- Anthropic 区分 workflow 与 agent：workflow 通过预定义代码路径编排 LLM 和工具，agent 由 LLM 动态决定过程和工具使用。[Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)，访问日期：2026-09-28。
- OpenAI Agents API 将 Harness 描述为运行模型与工具循环并维护 Agent session 的组件，执行环境负责命令、代码和文件操作。[Agents API Architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture)，访问日期：2026-09-28。

### 2. Think、Act、Observe 三类步骤

【我的理解】

- Think、Act、Observe这三个实际上是React的三步，思考、行动、观察
- 其实这不是React框架独创的，这是强化学习提出的思想，也符合我们人探索世界时候的逻辑
- 先想清楚应该怎么做，然后行动，观察当前动作的环境反馈确定执行下一步，还是修改这一步的动作重新执行
- 这里我详细介绍一下React的执行过程
  - think：首先模型会推理用户的问题和当前Agent中提供的工具和系统提示词，如果需要执行工具，会在tool_call参数中生成调用模型的Json schema
  - act：Agent会根据json schema解析函数名本地调用函数或者是直接调用MCP工具
  - observe：实际上和think是一起的，工具运行的结果会放入到历史中，大模型下次思考的时候会自动观察

【AI 补充与校正】

- ReAct 来自 Reasoning 与 Acting 的组合。它借鉴了智能体与环境交互的通用形式，但 ReAct 本身是 2022 年提出的 LLM prompting/agent 方法，并非强化学习算法。
- Thought/Reasoning 阶段根据任务、历史观察和可用工具形成下一步决策。具体产品可以隐藏内部推理，只输出结构化动作或简短说明。
- Tool schema 描述工具名称、参数字段与类型；一次 tool call 携带的是符合该 schema 的具体参数对象。schema 与本次调用参数需要分开理解。
- Act 阶段由 Harness 解析模型给出的动作，并通过本地函数、MCP client 或其他适配器执行。
- Observe 是独立的状态更新阶段。Harness 将工具结果或错误记录到 memory/context，下一次模型调用据此继续决策。


【疑问】

- 当前的Agent Loop是否还是React？相比于之前的naive react多了什么？

【疑问解答】

- smolagents 当前的 `MultiStepAgent` 明确以 ReAct 为基础：将 memory 转为 messages，调用 Model，解析并执行 action，将结果写入 `ActionStep`，再进入下一轮。
- 现代 Agent Loop 通常仍保留 Reason/Act/Observe 核心循环，并加入结构化 tool calling、最大步骤、时间与 token 预算、错误分类与重试、planning、callback、流式事件、人工审批、权限策略、持久化恢复、轨迹观测和最终答案校验。
- “naive ReAct”适合描述只具备模型、工具和简单 while loop 的实现；生产 Harness 的差异主要来自循环外围的确定性控制与安全机制。

【外部事实】(附来源与访问日期)

- ReAct 论文提出交错生成 reasoning traces 与 task-specific actions，使推理能够更新计划、处理异常，并通过动作从外部环境获取信息。[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)，访问日期：2026-09-28。
- smolagents 的 `MultiStepAgent` 将 ReAct 具体化为 memory → messages → Model → action → execution → `ActionStep`，并支持 planning 与 step callbacks。[How do multi-step agents work?](https://huggingface.co/docs/smolagents/conceptual_guides/react)，访问日期：2026-09-28。
- `MultiStepAgent` 暴露 `max_steps`、`step_callbacks`、`planning_interval`、`final_answer_checks` 和 `return_full_result` 等控制项。[Agents reference](https://huggingface.co/docs/smolagents/reference/agents)，访问日期：2026-09-28。

### 3. Model、Tool、Memory、Executor 的职责

【我的理解】

- model负责封装url、API和OpenAI接口，方便切换模型
- Tool是大模型可以调用的工具，可以是本地的脚本、Bash工具、文件读写工具、MCP工具，实际上就是一个Json，包含函数名、函数介绍、参数和参数介绍
- Memory现在执行三级记忆
  - 短期对话记忆：记录会话中的每轮对话
  - 长期对话记忆：持久化存储会话内容到磁盘当中
  - 抽象记忆：当会话压缩或者归档的时候，提取用户偏好和之前会话的摘要
- Executor是工具的执行器，工具的参数会在这里被真正运行，运行的环境可以是沙箱也可以本机操作系统分配给进程的运行环境

【AI 补充与校正】

- Model 适配器除了封装 URL 和凭据，还统一 messages、tool definitions、生成参数、模型响应、usage、停止原因和 provider error。稳定的内部模型接口能够隔离不同提供商的变化。
- Tool 是“可执行能力 + 面向模型的元数据”。JSON 或 JSON Schema 只负责描述名称、用途、输入和输出；真正的工具还包含实现、依赖、错误语义与副作用边界。
- “短期、长期、抽象”是可采用的记忆分层方案，并非所有 Agent 框架的固定结构。smolagents 的 `AgentMemory` 主要保存当前 Agent 的 system prompt 和 task/action/planning steps，支持 reset、读取和 replay；跨进程持久化与用户画像需要额外实现。
- 在 smolagents 中，`PythonExecutor` 专门执行 `CodeAgent` 生成的 Python 动作。`ToolCallingAgent` 的普通工具调用由 Agent Loop 找到工具并执行。自研 Harness 可以在更高层将所有副作用统一抽象为 executor/runtime。

【疑问】

- 有什么补充吗？或者不对的地方？

【疑问解答】

- 你的四组件划分已经覆盖主干，可以再加入 Loop/Runner、Context、Policy、Storage 和 Telemetry。
- Memory 表示 Agent 可利用的状态；Context 表示某一次模型调用实际装入窗口的信息。持久化内容需要经过选择后才进入 Context。
- Executor 需要与 Tool Registry 区分：Registry 负责发现、描述和定位工具，Executor 负责在权限与资源约束下运行具体动作。
- Harness 的最小调用链可以表达为：Runner 读取状态 → Context 组装 messages → Model 生成 action → Policy 判断权限 → Executor 执行动作 → Memory/Storage 记录 observation → Runner 判断继续或结束。

【外部事实】(附来源与访问日期)

- smolagents 的 `Model` 基类统一消息处理、工具集成和模型配置，具体实现通过 `generate()` 接入模型推理。[Models reference](https://huggingface.co/docs/smolagents/reference/models)，访问日期：2026-09-28。
- smolagents 的 `Tool` 同时包含 `name`、`description`、`inputs`、`output_type`、可选 `output_schema` 和实际执行的 `forward()`。[Tools reference](https://huggingface.co/docs/smolagents/reference/tools)，访问日期：2026-09-28。
- smolagents 的 `AgentMemory` 保存 system prompt 与 task/action/planning steps，并支持完整或精简读取、reset 和 replay。[Agents reference](https://huggingface.co/docs/smolagents/reference/agents)，访问日期：2026-09-28。
- smolagents 明确说明本地 Python executor 不是安全 sandbox，不可信代码应使用隔离执行器。[Python code executors](https://huggingface.co/docs/smolagents/reference/python_executors)，访问日期：2026-09-28。


## 二、环境搭建记录

目标: 安装并锁定 smolagents v1.26.0, 密钥通过环境变量提供。

### 推荐环境

- 操作系统：Windows 11 + PowerShell 7。
- Python：3.12，由 uv 管理。
- 包管理：当前机器已安装 uv 0.12.17。
- smolagents：锁定 v1.26.0，保证学习期间源码与文档基线稳定。
- 首个模型接入：`InferenceClientModel` + Hugging Face Inference Providers。
- 开发工具：pytest、pytest-asyncio、Ruff、mypy。

### 搭建步骤

#### 1. 检查 uv

运行目录：仓库根目录 `D:\programAI\learn_agent_simple2perfect`。

```powershell
uv --version
```

预期结果：输出 `uv 0.12.17` 或更高兼容版本。当前机器检查结果为 `uv 0.12.17`。

缺少 uv 时使用 Windows Package Manager 安装：

```powershell
winget install --id=astral-sh.uv -e
```

#### 2. 安装 Python 3.12

```powershell
uv python install 3.12
uv python list
```

预期结果：列表中存在 uv 管理的 Python 3.12。

#### 3. 初始化项目元数据

```powershell
uv init --lib --name agent-harness --python 3.12 --no-readme --vcs none .
```

预期结果：生成 `pyproject.toml` 和 `.python-version`，并保留当前 README、Git 仓库与既有目录。

#### 4. 添加学习依赖

```powershell
uv add "smolagents==1.26.0"
uv add --dev pytest pytest-asyncio ruff mypy
uv sync
```

预期结果：生成 `.venv/` 和 `uv.lock`，项目依赖安装完成。

#### 5. 验证版本

```powershell
uv run python -c "from importlib.metadata import version; print(version('smolagents'))"
uv run python --version
```

预期结果：分别输出 `1.26.0` 和 Python 3.12.x。

#### 6. 设置模型密钥

当前 PowerShell 会话中安全输入 Hugging Face token：

```powershell
$env:HF_TOKEN = Read-Host -Prompt "HF_TOKEN" -MaskInput
```

预期结果：token 只保存在当前进程环境中，关闭终端后失效。代码使用 `os.environ["HF_TOKEN"]` 读取。

`.gitignore` 至少包含：

```gitignore
.venv/
.local/
.env
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
```

#### 7. 运行纯模型调用

创建临时学习脚本时使用以下核心代码，明确指定模型 ID 以保证实验可复现：

```python
import os

from smolagents import InferenceClientModel


model = InferenceClientModel(
    model_id="Qwen/Qwen3-Next-80B-A3B-Thinking",
    token=os.environ["HF_TOKEN"],
    max_tokens=256,
)

messages = [
    {
        "role": "user",
        "content": [{"type": "text", "text": "只回复 pong"}],
    }
]

response = model(messages)
print(response.content)
```

执行命令：

```powershell
uv run python <脚本路径>
```

预期结果：模型返回包含 `pong` 的响应。将模型 ID、provider、响应字段、usage 和延迟记录到“纯模型调用观察”。

【外部事实】

- uv 支持 Windows，并使用 `uv init`、`uv add`、`uv sync` 和 lockfile 管理项目环境。[uv documentation](https://docs.astral.sh/uv/)，访问日期：2026-09-28。
- smolagents 当前稳定文档版本为 v1.26.0；main 文档对应源码开发版本。[smolagents documentation](https://huggingface.co/docs/smolagents/index)，访问日期：2026-09-28。
- `InferenceClientModel` 封装 Hugging Face `InferenceClient`，支持 Hub 上的 Inference Providers、专用 endpoint 和自定义 base URL。[Models reference](https://huggingface.co/docs/smolagents/reference/models)，访问日期：2026-09-28。

- [ ] `pyproject.toml` 完成 Python 版本、smolagents 和开发工具配置
- [ ] 安装命令可重复执行
- [ ] 确认密钥只从环境变量读取, 未出现在源码和日志中

### 操作记录

(每条命令注明运行目录、前置条件和预期结果)

```powershell
# 在实际执行上述步骤时，将命令和关键输出复制到这里。
```

【观察】

-

### 纯模型调用观察

- [ ] 运行一个纯模型调用 (不使用 Agent、不使用工具)

【观察】 摘录请求与响应的关键内容: 发送了什么消息结构、返回了什么字段、token 用量、延迟。记录原始输入输出时可放入被 Git 忽略的 `.local/`。

- 发送内容:
- 返回内容:
- 值得注意的点:


## 三、画图区: 用户输入到 Agent 最终输出的基本流程

(验收要求之一。用文字或 ASCII 图, 术语与站内文档保持一致: Think / Act / Observe / Model / Tool / Memory / Executor)

```

```

---

## 四、今日疑问汇总

1. 广义 Agent 的定义、Agent 与 Harness 的边界：已形成阶段 0 结论，后续在阶段 4 使用自研 Agent Loop 验证。
2. 现代 Agent Loop 与 ReAct 的关系：已形成阶段 0 结论，后续在阶段 4 阅读 `MultiStepAgent` 源码验证。
3. Model、Tool、Memory、Executor 的边界：已补充框架事实，后续分别在阶段 2、3、4、5 通过代码验证。

## 五、资料

- smolagents 官方文档 (学习基线 v1.26.0): https://huggingface.co/docs/smolagents/index
- smolagents Guided Tour: https://huggingface.co/docs/smolagents/guided_tour
- smolagents Agent 概念: https://huggingface.co/docs/smolagents/conceptual_guides/intro_agents
- smolagents Multi-step Agent: https://huggingface.co/docs/smolagents/conceptual_guides/react
- ReAct 论文: https://arxiv.org/abs/2210.03629
- Anthropic Agent 工程实践: https://www.anthropic.com/engineering/building-effective-agents
- OpenAI Agents API Architecture: https://developers.openai.com/api/docs/guides/agents-api/architecture
- uv 官方文档: https://docs.astral.sh/uv/
- 访问日期: 2026-09-28
