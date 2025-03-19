# 基于 LangChain 调用 LLM

## 1. 测试

### 1.1. 设置环境变量

在 Linux上：打开终端, 编辑你的 shell 配置文件（例如 `~/.bashrc`）, 在文件末尾添加以下行：保存文件并退出编辑器。

```
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="<your-langsmith-api-key>"
export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
# The example uses OpenAI, but it's not necessary if your code uses another LLM provider
export OPENAI_API_KEY="<your-openai-api-key>"
```

 运行以下命令使更改生效：

```
source ~/.bashrc
```

创建一个LangChain项目:

```bash
langchain app new thinking-in-langchain
```

使用poetry添加第三方包(例如langchain-openai等)

```
pip index versions pipx
pip install pipx==1.7.1
pipx ensurepath

pip index versions poetry
pipx install poetry==2.1.1
```

添加依赖：

```bash
poetry add langchain==0.3.20
poetry add langchain-community==0.3.19
poetry add langchain-openai==0.3.8
poetry add langsmith==0.3.15
```

运行项目

```bash
poetry run langchain serve --port 8090 
```

## 2. 测试

### 2.1. LangChain服务部署与链路监控

### 2.1. LangChain消息管理与聊天历史存储

#### 2.1.1 session_id 存储在内存

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
import os

# 启用LangChain追踪
os.environ["LANGSMITH_TRACING"] = "true"
# 设置LangChain API密钥
os.environ["LANGCHAIN_API_KEY"] = "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"
# 这里输入在langsmith中创建的项目的名字
os.environ["LANGCHAIN_PROJECT"] = "default"
# 设置LangChain API端点地址
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# 从环境变量中获取 API 密钥
openai_api_key = os.getenv("OPENAI_API_KEY")

# 初始化 ChatOpenAI 实例
chat = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=openai_api_key,
    openai_api_base="https://api.deepseek.com",
    streaming=False
)

# 定义 ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant who is good at {ability}. Response in 200 words or fewer."
        ),
        MessagesPlaceholder(variable_name="history"),  # 历史消息占位符
        ("human", "{input}")  # 用户输入
    ]
)

# 将 prompt 和 chat 组合成一个 runnable
runnable = prompt | chat

# 用于存储会话历史的字典
store = {}

# 获取会话历史的函数
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 创建 RunnableWithMessageHistory
with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",  # 用户输入的键
    history_messages_key="history"  # 历史消息的键
)

# 第一次调用
response = with_message_history.invoke(
    {"ability": "math", "input": "余弦是什么意思?"},  # 输入
    config={"configurable": {"session_id": "abc123"}}  # 会话 ID
)
print(response.content)

# 第二次调用
response = with_message_history.invoke(
    {"ability": "math", "input": "什么?"},  # 输入
    config={"configurable": {"session_id": "abc123"}}  # 会话 ID
)
print(response.content)

# 第三次调用
response = with_message_history.invoke(
    {"ability": "math", "input": "什么?"},  # 输入
    config={"configurable": {"session_id": "abc456"}}  # 会话 ID
)
print(response.content)
```

#### 2.1.2 user_id & conversation_id 存储在内存

```Python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
import os
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.output_parsers import StrOutputParser

# 启用LangChain追踪
os.environ["LANGSMITH_TRACING"] = "true"
# 设置LangChain API密钥
os.environ["LANGCHAIN_API_KEY"] = "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"
# 这里输入在langsmith中创建的项目的名字
os.environ["LANGCHAIN_PROJECT"] = "default"
# 设置LangChain API端点地址
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# 从环境变量中获取 API 密钥
openai_api_key = os.getenv("OPENAI_API_KEY")

# 初始化 ChatOpenAI 实例
chat = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=openai_api_key,
    openai_api_base="https://api.deepseek.com",
    streaming=False
)

# 定义 ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant who is good at {ability}. Response in 200 words or fewer."
        ),
        MessagesPlaceholder(variable_name="history"),  # 历史消息占位符
        ("human", "{input}")  # 用户输入
    ]
)

output_parser = StrOutputParser()

# 将 prompt 和 chat 组合成一个 runnable
runnable = prompt | chat | output_parser

# 用于存储会话历史的字典
store = {}

# 获取会话历史的函数
def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
    if (user_id, conversation_id) not in store:
        store[(user_id, conversation_id)] = ChatMessageHistory()
    return store[(user_id, conversation_id)]

# 创建 RunnableWithMessageHistory
with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="用户的唯一标识符。",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="对话的唯一标识符。",
            default="",
            is_shared=True,
        ),
    ],
)

response = with_message_history.invoke(
    {"ability": "math", "input": "余弦是什么意思？"},
    config={"configurable": {"user_id": "123", "conversation_id": "1"}},
)
print(response)

# 记住
response = with_message_history.invoke(
    {"ability": "math", "input": "什么?"},
    config={"configurable": {"user_id": "123", "conversation_id": "1"}},
)
print(response)

response = with_message_history.invoke(
    {"ability": "math", "input": "什么?"},
    config={"configurable": {"user_id": "123", "conversation_id": "2"}},
)
print(response)
```

#### 2.1.3 user_id & conversation_id 存储在Redis

```bash
## pip index versions redis 
## pip install redis==5.2.1
```

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

from langchain_community.chat_message_histories import ChatMessageHistory,RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
import os
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.output_parsers import StrOutputParser

# 启用LangChain追踪
os.environ["LANGSMITH_TRACING"] = "true"
# 设置LangChain API密钥
os.environ["LANGCHAIN_API_KEY"] = "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"
# 这里输入在langsmith中创建的项目的名字
os.environ["LANGCHAIN_PROJECT"] = "default"
# 设置LangChain API端点地址
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# 从环境变量中获取 API 密钥
openai_api_key = os.getenv("OPENAI_API_KEY")

# 初始化 ChatOpenAI 实例
chat = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=openai_api_key,
    openai_api_base="https://api.deepseek.com",
    streaming=False
)

# 定义 ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant who is good at {ability}. Response in 200 words or fewer."
        ),
        MessagesPlaceholder(variable_name="history"),  # 历史消息占位符
        ("human", "{input}")  # 用户输入
    ]
)

output_parser = StrOutputParser()

# 将 prompt 和 chat 组合成一个 runnable
runnable = prompt | chat | output_parser

REDIS_URL = "redis://localhost:6379/0"

# 获取会话历史的函数
def get_message_history(user_id: str, conversation_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(user_id+conversation_id, url=REDIS_URL)

with_message_history = RunnableWithMessageHistory(
    runnable,
    get_message_history,
    input_messages_key="input",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="用户的唯一标识符。",
            default="",
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="对话的唯一标识符。",
            default="",
            is_shared=True,
        ),
    ],
)

response = with_message_history.invoke(
    {"ability": "math", "input": "余弦是什么意思？"},
    config={"configurable": {"user_id": "123", "conversation_id": "1"}},
)
print(response)

# 记住
response = with_message_history.invoke(
    {"ability": "math", "input": "什么?"},
    config={"configurable": {"user_id": "123", "conversation_id": "1"}},
)
print(response)

response = with_message_history.invoke(
    {"ability": "math", "input": "什么?"},
    config={"configurable": {"user_id": "123", "conversation_id": "2"}},
)
print(response)
```





**参考：**

1. [【LangChain教程】2025年吃透LangChain+LangGraph快速入门与底层原理教程](https://www.bilibili.com/video/BV1duKsevEwK?spm_id_from=333.788.videopod.episodes&vd_source=68a8583f88fde22ce39c9c2212b4cac4)
2. [LangChain服务部署与链路监控_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1uNQAYZE4C/?spm_id_from=333.1391.0.0&p=5&vd_source=68a8583f88fde22ce39c9c2212b4cac4)
3. [ LangServe](https://python.langchain.com/docs/langserve/)
