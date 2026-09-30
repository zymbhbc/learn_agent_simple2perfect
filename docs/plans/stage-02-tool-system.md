# 阶段 2: Tool 工具系统学习安排

本计划用于理解 smolagents 工具描述与执行边界, 并完成三个限定测试工作区的只读文件工具。前置条件是阶段 1 的 `ToolCallingAgent` 示例和运行轨迹已通过验收, 可独立识别一次结构化工具调用中的名称、参数、结果与错误。

- 状态: `planned`
- 预计投入: 5-7 小时, 分 5 次学习会话
- 总路线图: [smolagents 学习与 Agent Harness 实践计划](smolagents-learning-roadmap.md)
- 输入: 阶段 1 的示例、教程和知识验收记录; smolagents 1.26.0 的 `tools.py`
- 产出: `examples/03-custom-tools.py`、`docs/tutorials/smolagents-tool-system.md`、`verification/code/stage-02-tools.md`、`verification/knowledge/stage-02-tools.md`, 以及三个工具的独立单元测试
- 约定: 所有命令的运行目录都是仓库根目录 `D:\programAI\learn_agent_simple2perfect`; 观察类步骤只描述操作, 实际现象与差异由你记录, 不预设结论

## 学习边界与关键问题

本阶段实现 `list_files`、`search_text` 和 `read_file` 三个只读工具, 并用固定测试工作区验证路径、参数、异常和输出大小边界。重点回答:

1. `name`、`description`、`inputs`、`output_type` 与实际 `forward()` 分别承担什么职责?
2. `@tool` 与 `Tool` 子类各自如何声明同一能力?
3. 参数校验、工具内部错误和输出限制应在哪一层处理, 模型将看到什么反馈?
4. 工具描述如何影响模型选择工具, 怎样通过相同任务轨迹验证这种影响?

## 会话 1: 工具契约 (60-80 分钟)

### 1.1 预检与源码定位 (约 15 分钟)

```powershell
uv run python -c "from smolagents import Tool, tool; print(Tool, tool)"
```

预期结果: 打印两个对象描述, 证明 1.26.0 的 `Tool` 与 `tool` 可从顶层导入。

本地源码定位 `.venv/Lib/site-packages/smolagents/tools.py`: `Tool` 类 (约 106 行起, 属性 docstring 列出 `name`、`description`、`inputs`、`output_type`、`output_schema`) 、`@tool` 装饰器 (约 1061 行) 、`tool_validation.py` 的 `MethodChecker`。只读 docstring 与关键分支, 不逐行展开。

### 1.2 契约观察 (约 25-35 分钟)

1. `[Guided tour](https://huggingface.co/docs/smolagents/guided_tour)` 与 [Tools tutorial](https://huggingface.co/docs/smolagents/tutorials/tools) 中工具定义部分, 核对 `Args:` docstring 与 `inputs` 的关系。
2. 临时脚本或直接在会话 3 目标文件中, 用 `@tool` 定义阶段 1 的 `add_two_ints`, 打印 `name`、`description`、`inputs`、`output_type`, 记录 `inputs` 的实际结构 (KeyError 无 → 每个参数 dict 的键是什么) 。
3. 直接调用 `add_two_ints(a=2, b=4)` 确认装饰后仍可像普通函数调用。
4. 改动实验: 把 docstring 中 `Args:` 段删掉重新观察元数据; 把函数名改成动词缺失的形式, 记录模型可见文本的变化。只记录现象, 结论留给知识验收。

### 当次完成条件

- [ ] 能逐项说明 name、description、inputs、output_type 与函数实现的关系
- [ ] 记录了同一工具在改动 docstring 前后的元数据差异

## 会话 2: 类式工具与错误 (60-80 分钟)

### 2.1 双写对比 (约 25-35 分钟)

1. 用 `Tool` 子类重新声明 `add_two_ints`: 设置类属性 `name`、`description`、`inputs` (含每个参数 `type` 与 `description`) 、`output_type`, 实现 `forward()`。
2. 对照表五列: 声明来源 | `@tool` 写法 | `Tool` 子类写法 | 模型可见位置 | 备注 (校验差异, 如 `MethodChecker` 对方法体的检查) 。写入知识验收草稿。

### 2.2 错误注入 (约 25-35 分钟)

对两个版本的任一工具, 分别制造三类错误并记录 harness 的表现:

1. 缺少参数与错误类型: 先直接调用 `forward`/被装饰函数, 观察纯 Python 层异常; 再接入一个只挂该工具的 `ToolCallingAgent` 观察经 Agent Loop 后进入 observation 的文本形式。
2. 工具内部异常: 在 `forward` 中主动 `raise ValueError("boom")`。
3. 对照源码 `.venv/.../agents.py` 约 1300-1500 区段与 `utils.py` 的 `AgentToolExecutionError` (约 128 行) , 说明错误从 `forward` 到 observation 的包装链; `AgentParsingError` 分支注明是解析层错误。
4. 思考并在验收草稿标注: 哪些错误应转成给模型的文字提示 (可恢复) , 哪些应中止运行。

### 当次完成条件

- [ ] 契约对照表完成
- [ ] 三类错误各有纯函数层 + Agent 层两级观察记录

## 会话 3: 只读文件工具 (70-90 分钟)

### 3.1 设计规范 (先定规格再写码, 约 20 分钟)

三个工具共用一个受控根目录, 规格固定如下:

| 工具 | 参数 | 行为 | 输出上限 | 必测边界 |
| --- | --- | --- | --- | --- |
| `list_files` | `dir: str` (相对根目录, 可空) | 列出目录下一层文件名 | 最多 100 条 + `... (truncated)` 标记 | 越界目录、空目录 |
| `search_text` | `pattern: str`, `dir: str` | 逐文件按行子串匹配 | 最多 20 个 `file:line:content` + 计数 | 越界、无匹配、超上限 |
| `read_file` | `path: str` | 读取全文 (utf-8) | 最多 2000 字符 + 截断标记 | 越界、缺失、截断触发 |

### 3.2 路径边界公共逻辑 (约 25 分钟)

三个工具共用同一段"解析→校验→读取"逻辑, 在 `examples/03-custom-tools.py` 中实现, 骨架:

```python
"""Read-only workspace tools demo.

Run: ``uv run python examples/03-custom-tools.py`` (expects HF_TOKEN).
"""

from pathlib import Path

from smolagents import Tool

MAX_LIST_ENTRIES = 100
MAX_MATCHES = 20
MAX_CHARS = 2000


def resolve_in_root(root: Path, relative: str) -> Path:
    """Resolve ``relative`` and guarantee it stays inside ``root``.

    Raises ValueError with a recoverable message when the path escapes.
    """

    target = (root / relative).resolve() if relative else root.resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"path escapes workspace: {relative!r}")
    return target


class ReadFileTool(Tool):
    name = "read_file"
    description = ("Read one text file inside the allowed workspace. Long files "
                   "are truncated with an explicit marker.")

    inputs = {
        "path": {
            "type": "string",
            "description": "Workspace-relative file path.",
        }
    }
    output_type = "string"

    def __init__(self, root: Path) -> None:
        super().__init__()
        self.root = root.resolve()

    def forward(self, path: str) -> str:
        target = resolve_in_root(self.root, path)
        if not target.is_file():
            return f"not a file: {path}"
        text = target.read_text(encoding="utf-8")
        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS] + f"\n... (truncated at {MAX_CHARS} chars)"
        return text


# list_files / search_text 按同规格自行实现。注意:
# 1) resolve_in_root 抛出的 ValueError 是直接传播 (走 AgentToolExecutionError 路径) 还是改为返回错误字符串
#    (直接进入 observation), 两种策略各跑一次并记录模型端观感。
```

`list_files`、`search_text` 按同一规格自行实现, 关键决策点: 越界错误是抛异常 (走 `AgentToolExecutionError` 路径) 还是返回错误字符串 (直接进入 observation) — 各选其一并能在会话 5 说明取舍。

### 3.3 手工验证 (约 15 分钟)

`tests/fixtures/` 之外首选临时目录: 在系统临时路径创建工作区, 放入 3 个文件 (一个超过 2000 字符, 一个内容含 `TODO:` 关键词供会话 5 搜索任务使用) , 通过短脚本实例化工具并手动调用, 记录正常读取、截断、越界三种实际输出。

### 当次完成条件

- [ ] 三个工具实现完成且能独立调用出正确结果
- [ ] 越界、缺失、截断三种输出有实际摘录

## 会话 4: 独立测试 (70-90 分钟)

### 4.1 测试文件与引用方式 (约 15 分钟)

测试文件按 [tests 规则](../../tests/AGENTS.md) 命名: `tests/unit/test_stage02_tool_list_files.py`、`test_stage02_tool_search_text.py`、`test_stage02_tool_read_file.py`。示例文件不是包, 用 importlib 引用:

```python
import importlib.util
from pathlib import Path

EXAMPLE_PATH = Path(__file__).resolve().parents[2] / "examples" / "03-custom-tools.py"


def load_custom_tools():
    spec = importlib.util.spec_from_file_location("custom_tools", EXAMPLE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
```

测试工作区用 pytest 的 `tmp_path` 动态创建, 不依赖仓库内固定目录; 测试名遵循 `test_<behavior>_<condition>_<result>`。

### 4.2 用例矩阵 (约 30-40 分钟, 每工具独立建文件)

| 场景 | 输入 | 数据条件 | 期待结果 |
| --- | --- | --- | --- |
| 正常路径 | 合法相对路径 | 文件存在、内容可控 | 返回内容本体 |
| 输出截断 | 超长内容 | 超过上限 | 含截断标记且长度可控 |
| 路径逃逸-相对 | `../outside.txt` | 根目录外 | 稳定报错, 不返回外部内容 |
| 路径逃逸-绝对 | 绝对路径指向外部 | 同上 | 同上 |
| 路径逃逸-链接 | 根目录内符号链接指向外部 | 平台允许时 | 解析后被拒 |
| 参数缺失/类型错 | 缺 `path` / 传整数 | 待观察 | 纯函数层与封装层两种记录 |
| 目标缺失 | 不存在的路径 | 同上 | 可恢复的错误说明 |
| 内部异常 | `forward` 抛异常 | 同上 | 观察包装错误 |

```powershell
uv run pytest tests/unit -q
```

预期结果: 三个测试文件全部通过; 失败时先修实现或测试, 保留一次" failing→passing"的复现记录用于验收引用。

### 当次完成条件

- [ ] 矩阵中每行至少一个具名测试函数
- [ ] `uv run pytest tests/unit -q` 全绿并将实际输出存入 `.local/` 与验收记录

## 会话 5: 集成观察与验收 (60-80 分钟)

### 5.1 Agent 集成观察 (约 25-35 分钟)

1. 在示例中把三个工具都挂到阶段 1 的 `ToolCallingAgent`, 任务用固定措辞, 例如: "列出工作区有哪些文件, 找出其中有 todo 的文件并读取其中的任务项"。
2. 对比两个变体并各自保存轨迹: (a) 原版 description; (b) 把 `search_text` 的 description 改为含糊描述。回答: 工具选择与参数变化, description 的哪个位置被模型读见。
3. `replay(detailed=True)` 复述: 观察结果→ (`ActionStep.observations`) 如何被下一轮消息读取。
4. 模型不可用时, 使用固定响应模型构造两次调用脚本对工具和错误路线做最小集成观察。回退方案与阶段 1 风险区同一节一致。

### 5.2 验收与教程 (约 25-30 分钟)

1. `verification/code/stage-02-tools.md`: 验收对象、前置条件、测试命令、预期结果、实际结果、测试输出摘要、证据路径、`passed`/`failed`/`blocked` 结论与日期。
2. `verification/knowledge/stage-02-tools.md`: 四个关键问题独立分段作答 (不看源码) ; 双来源标注 (外部事实/AI 推断/自查) 。
3. `docs/tutorials/smolagents-tool-system.md`: 按 Tutorial 结构组织, 教程中的命令、代码与 `examples/03-custom-tools.py` 一致。
4. 更新路线图阶段总览 `docs/plans/smolagents-learning-roadmap.md` 中阶段 2 状态为 `completed` 并链接验收记录; 当日事实写入 `logs/`。

### 当次完成条件

- [ ] 两种 description 的轨迹对比可复述
- [ ] 三份文档相互引用一致
- [ ] 路线图状态已更新

## 记录与产物约定

| 内容 | 去向 | 要求 |
| --- | --- | --- |
| 完整测试输出、模型原始响应 | `.local/` | 不入 Git, 文件名注明场景与日期 |
| 测试与验收结论 | `verification/code/stage-02-tools.md` | 命令+预期+实际+结论, 结论用 `passed/failed/blocked` |
| 概念疑问与个人理解 | `notes/` | 保留原话, 标注 AI 推断 |
| 可复用知识 | `docs/tutorials/smolagents-tool-system.md` | 最终态表达, 与示例一致 |

## 依赖与风险

- 文件系统路径可能经过相对路径、绝对路径、`..` 或符号链接指向工作区外部; 实现以解析后的目标路径 (`Path.resolve()` + 归属判断) 为准。【AI 推断, 需自行核验】Windows 下创建符号链接通常需要管理员权限或开发者模式; 无条件时把链接逃逸用例标记 `pytest.skip(需特权)`, 改为代码走读确认 `resolve()` 语义, 并在验收记录注明覆盖方式。
- 搜索结果和文件内容可能过大; 每个工具设置结果上限, 并在截断信息中标明结果范围。
- 自然语言工具选择具有波动性; 工具的功能正确性由确定性单元测试验收, 模型选择行为用固定任务与轨迹记录观察。

## 完成条件

- 三个工具可读取指定测试工作区, 且对非法参数、路径越界和超大输出有稳定结果。
- 每个工具具有独立单元测试; 相关测试命令和结果写入代码验收记录。
- 能独立声明一个带完整 schema 的 `Tool`, 并解释 `@tool` 与类式工具的元数据来源。
- 教程、示例和知识验收记录明确描述工具描述、实际调用参数、执行结果与错误反馈的关系。

## 资料

- Hugging Face, [Tools tutorial](https://huggingface.co/docs/smolagents/tutorials/tools), 访问日期: 2026-09-29。
- Hugging Face, [Tools reference](https://huggingface.co/docs/smolagents/reference/tools), 访问日期: 2026-09-29。
- 本地已安装 smolagents 1.26.0 源码, 用于核对当前行为: `.venv/Lib/site-packages/smolagents/tools.py` (`Tool` 类约 106 行, `@tool` 约 1061 行) 、`tool_validation.py` (`MethodChecker`) 、`agents.py` (工具调用执行与错误包装约 1300-1500 区段) 、`utils.py` (`AgentToolExecutionError` 约 128 行) 。
- pytest: [Good Integration Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html), 测试布局参考, 访问日期: 2026-09-29。
