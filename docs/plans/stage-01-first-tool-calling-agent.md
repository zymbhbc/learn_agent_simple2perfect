# 阶段 1: 第一个 ToolCallingAgent 学习安排

本计划用于完成第一个 smolagents `ToolCallingAgent` 实验, 学习重点是观察结构化工具调用、运行轨迹和步骤上限。前置条件是已掌握阶段 0 的 Model、Tool、Memory 与 Agent Loop 概念, 并能在仓库根目录使用 Python 3.12 和已锁定的 smolagents 1.26.0 环境。

- 状态: `planned`
- 预计投入: 3-4 小时, 分 3 次学习会话
- 总路线图: [smolagents 学习与 Agent Harness 实践计划](smolagents-learning-roadmap.md)
- 输入: [阶段 0 学习记录](stage-00-agent-fundamentals.md)、仓库中的 `pyproject.toml` 与 `uv.lock`
- 产出: `examples/01-first-tool-calling-agent.py`、`docs/tutorials/first-smolagents-agent.md`、`verification/knowledge/stage-01-agent-types.md`
- 约定: 所有命令的运行目录都是仓库根目录 `D:\programAI\learn_agent_simple2perfect`; 未注明预期结果的命令在执行后自行记录实际输出

## 学习边界与关键问题

本阶段使用一个确定性的纯计算工具, 观察 `ToolCallingAgent` 如何将工具描述交给 Model、解析工具调用、执行工具、保存观察并生成最终回答。重点回答:

1. 工具的名称、描述和参数如何影响 Model 给出的调用?
2. 一次工具调用中的具体参数、工具返回值和下一轮消息如何对应?
3. `replay()` 中的动作、观察与最终回答分别来自哪里?
4. 达到 `max_steps` 后, 运行轨迹和最终输出呈现什么状态?

## 会话 1: 阅读与构建 (60-80 分钟)

### 1.1 环境预检 (约 5 分钟)

依序执行并核对预期结果, 任何一项不符合先停下修复:

```powershell
uv run python -c "import smolagents, sys; print(smolagents.__version__, sys.version)"
```

预期结果: 输出 `1.26.0` 和 Python `3.12.x`。

```powershell
uv run python -c "import os; print(bool(os.environ.get('HF_TOKEN')))"
```

预期结果: 输出 `True`。为 `False` 时先执行 `$env:HF_TOKEN = Read-Host -Prompt "HF_TOKEN" -MaskInput`, 并确认理解这是会话级密钥。

```powershell
uv run python -c "from smolagents import ToolCallingAgent, InferenceClientModel, tool, LogLevel; print(LogLevel.DEBUG)"
```

预期结果: 输出 `LogLevel.DEBUG` 之类的一行, 证明示例所需的公开接口在 1.26.0 中都存在。

```powershell
uv run python -c "import inspect; from smolagents import ToolCallingAgent; print(inspect.signature(ToolCallingAgent.__init__))"
```

预期结果: 打印 `(tools, model, prompt_templates=None, planning_interval=None, stream_outputs=False, max_tool_threads=None, **kwargs)`。该检查只确认当前安装版本的公开构造接口；`description` 和 `max_steps` 的实际行为通过 1.3 示例验证。

### 1.2 阅读与协议观察 (约 20-30 分钟)

- 阅读 [Guided tour](https://huggingface.co/docs/smolagents/guided_tour) 中 "select a model"、"build your agent" 与工具调用演示部分; 访问日期记入资料区。
- 阅读 [Agent 中工具如何使用](../../notes/Agent中工具如何使用.md#六工具-schema-与轮次衔接) 中的运行时观察，理解工具目录、ToolCall、ToolResult、Memory 和下一轮 Context 的稳定关系。
- 在 1.3 的实际运行中核对两个问题: Model 收到的工具定义位于什么输入位置? ToolCall 和 ToolResult 如何进入下一轮上下文? 只记录可观察输入输出，不要求阅读 Agent Loop 实现源码。

### 1.3 构建示例 (约 30-40 分钟)

创建 `examples/01-first-tool-calling-agent.py`, 采用如下骨架 (保持最小, 之后有需要再扩展):

```python
"""Minimal ToolCallingAgent with one deterministic arithmetic tool.

Prerequisite: ``HF_TOKEN`` set in the environment.
Run: ``uv run python examples/01-first-tool-calling-agent.py``
Expected: a final answer of ``6`` (or equivalent text) after one tool call.
"""

import os

from smolagents import InferenceClientModel, ToolCallingAgent, tool


@tool
def add_two_ints(a: int, b: int) -> int:
    """Add two integers and return the sum.

    Args:
        a: First integer.
        b: Second integer.
    """

    return a + b


def main() -> None:
    print("=== tool metadata ===")
    print("name:", add_two_ints.name)
    print("description:", add_two_ints.description)
    print("inputs:", add_two_ints.inputs)
    print("output_type:", add_two_ints.output_type)

    model = InferenceClientModel(
        model_id="Qwen/Qwen3-Next-80B-A3B-Thinking",
        token=os.environ["HF_TOKEN"],
        max_tokens=256,
    )
    # ToolCallingAgent.__init__ takes **kwargs and forwards them to
    # MultiStepAgent.__init__, which accepts description and max_steps.
    agent = ToolCallingAgent(
        tools=[add_two_ints],
        model=model,
        max_steps=5,
        description="Demo agent that can only add two integers.",
    )

    print("=== run ===")
    result = agent.run("Use the add_two_ints tool to compute 2 + 4.")
    print("final answer:", result)

    print("=== replay ===")
    agent.replay(detailed=True)


if __name__ == "__main__":
    main()
```

执行: `uv run python examples/01-first-tool-calling-agent.py`。前置条件: 1.1 全部通过且网络可达模型服务。预期结果: 打印工具元数据、至少一次工具调用与包含 6 的最终回答, replay 输出可读轨迹。

完成当次会话后建一条自测清单并记录: 能口头回答 "工具名称、描述、参数和返回类型被模型读见的完整传递路径"。

### 当次完成条件

- [ ] 1.1 预检三条命令全部符合预期
- [x] 示例运行成功, 出现真实工具调用与最终回答
- [x] 已将工具元数据摘录到知识验收草稿

## 会话 2: 运行轨迹与预算 (60-80 分钟)

### 2.1 正常轨迹记录 (约 30-40 分钟)

1. 重跑示例, 或把任务换成 `add_two_ints` 需处理的不同数字, 记录完整输出。
2. `uv run python examples/01-first-tool-calling-agent.py > .local/stage-01-normal.log 2>&1`, 将完整轨迹存入被 Git 忽略的 `.local/`。
3. 在 `verification/knowledge/stage-01-agent-types.md` 建一个表格: 轮次 | Model 输入中的工具目录 | Model 动作 | 工具与参数 | ToolResult | 下一轮变化。逐轮填完后说明工具目录的传递位置，以及 ToolCall 和 ToolResult 在下一轮的对应关系。

### 2.2 步骤上限实验 (约 20-30 分钟)

1. 复制会话 1 示例为 `.local/` 下临时脚本或直接在示例内增加开关, 构造无法在步数内完成的任务: `agent = ToolCallingAgent(..., max_steps=2)` 并让任务要求把三个数字连续相加三次 (超过两步)。
2. 运行并对比 2.1 的日志: 状态如何变为 `max_steps_error`, 收尾是否又调了一次模型, 最终输出与正常路径有什么差异。
3. 对照实际运行日志与 `agent.replay(detailed=True)` 输出，说明 replay 如何呈现任务、动作、观察和最终回答。
4. 若模型输出异常 (超长、格式不符) , 先用 `verbosity_level=LogLevel.DEBUG` 复跑一次并记录现象, 再决定是否改换参数。

### 当次完成条件

- [ ] 两条轨迹 (正常 + 步数上限) 都已保存并可复述
- [ ] 知识验收文件中标出每轮 Model 调用、工具动作、观察和最终回答
- [ ] 能解释 `max_steps=2` 触发后的收尾流程

## 会话 3: 复述与验收 (60-80 分钟)

### 3.1 数据流图 (约 20 分钟)

在 `verification/knowledge/stage-01-agent-types.md` 中绘制 Mermaid `flowchart TD`: 用户任务 → system prompt 组装 → Model 决策 → 工具调用 → 观察 → 循环或 final answer。节点术语与阶段 0 画图区一致。

### 3.2 知识自测 (约 20-30 分钟)

不看源码与文档, 独立回答四类问题, 每题写一段话: 1) 工具 schema 从定义到被模型读见的传递路径; 2) 一次 tool call 的 arguments 与 Python 实参的对应过程; 3) replay 中四类信息的出处; 4) max_steps 用尽时发生了什么。参考 [knowledge 验收规则](../../verification/AGENTS.md) , 必要时通过阶段 0 的【外部事实】补充证据。

### 3.3 教程与收尾 (约 20-30 分钟)

1. 将本阶段可复用的操作与判断整理为 `docs/tutorials/first-smolagents-agent.md`, 按 Tutorial 结构 (目标/前置/步骤/验证/故障/掌握检查) 组织, 命令与本示例保持一致。
2. 完善知识验收文件, 补运行命令、结果摘要、证据路径与结论 (`passed`/`failed`/`blocked` + 日期) 。
3. 将 `smolagents-learning-roadmap.md` 阶段总览中阶段 1 状态改为 `completed`, 链接验收记录。

### 当次完成条件

- [ ] 数据流图完成且与轨迹一致
- [ ] 四个问题全部独立作答, 疑问进入 notes
- [ ] 教程与两份验收记录落盘并交叉对应

## 记录与产物约定

| 内容 | 去向 | 要求 |
| --- | --- | --- |
| 完整运行轨迹、模型原始响应 | `.local/` | 不入 Git, 文件名注明场景与日期 |
| 运行命令、版本、结果摘要 | `verification/knowledge/stage-01-agent-types.md` | 命令 + 预期 + 实际 + 结论 |
| 概念疑问与个人理解 | `notes/stage-00-agent-fundamentals.md` 或新文件 | 保留原话, 标注 AI 推断 |
| 可复用知识 | `docs/tutorials/first-smolagents-agent.md` | 最终态表达, 相对路径链接 |

## 依赖与风险

- 模型的工具调用能力、可用额度和响应稳定性影响在线运行。模型接入受限时, 先用固定响应模型记录工具调用机制, 再补充真实模型观察。
- 无真实模型时使用已验证的 scripted `Model`: 在 `generate()` 中按队列返回预制 `ChatMessage`，第一轮调用 `add_two_ints`，第二轮调用 `final_answer`。该实验可同时记录每轮 `messages` 与 `tools_to_call_from`，用于验证工具目录和轮次衔接，不依赖网络与随机模型输出。

## 完成条件

- `examples/01-first-tool-calling-agent.py` 能调用确定性工具并返回最终回答。
- 验收记录包含正常轨迹、步骤上限轨迹、Mermaid 数据流图和运行命令。
- 能独立说明工具 schema、调用参数、工具结果和 Memory 中观察记录的关系。
- `docs/tutorials/first-smolagents-agent.md` 的命令与当前示例保持一致。

## 资料

- smolagents Guided tour: https://huggingface.co/docs/smolagents/guided_tour , 访问日期 2026-09-29。
- smolagents Agents reference: https://huggingface.co/docs/smolagents/reference/agents , 访问日期 2026-09-29。
- [Agent 中工具如何使用](../../notes/Agent中工具如何使用.md): 工具 schema、ToolCall、ToolResult 与下一轮上下文的运行时观察，记录日期 2026-09-29。
