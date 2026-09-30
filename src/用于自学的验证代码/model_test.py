"""通过 DeepSeek API 调用模型的最小验证脚本。

字段说明：
- model_id    服务侧模型名（deepseek-v4-pro）。
- api_base    API 端点（DeepSeek 官方 OpenAI 兼容地址）。
- api_key     Bearer 鉴权 token，当前直接写在源码里。
- max_tokens  单次响应允许生成的最大 token 数。
- messages    Chat Completions 协议消息体，每条 role 必填，content 可以是纯文本或多模态数组。
- response    模型返回的 ChatMessage，关键字段：role / content / tool_calls / raw / token_usage。

末尾用 ChatMessage repr 的注释块展示响应对象的嵌套结构，每个字段都附了注解。
"""

from smolagents import OpenAIServerModel

model = OpenAIServerModel(
    model_id="deepseek-v4-pro",
    api_base="https://api.deepseek.com",
    api_key="API_KEY_1234567890",  # 替换为实际的 Bearer token
    max_tokens=1000,
)

messages = [
    {
        "role": "user",
        "content": [{"type": "text", "text": "只回复 pong"}],
    }
]

response = model(messages=messages)
print(response)