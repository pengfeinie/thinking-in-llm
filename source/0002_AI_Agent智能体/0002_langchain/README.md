# 基于 LangChain 调用 LLM

## 1. 环境准备

参考 **AI Agent智能体开发实战之环境准备**

## 2. 测试

### 2.1. 设置环境变量

在 Linux上：

a. 打开终端。

b. 编辑你的 shell 配置文件（例如 `~/.bashrc`）。

c. 在文件末尾添加以下行：

```
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="<your-langsmith-api-key>"
export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
# The example uses OpenAI, but it's not necessary if your code uses another LLM provider
export OPENAI_API_KEY="<your-openai-api-key>"
```

d. 保存文件并退出编辑器。

e. 运行以下命令使更改生效：

```
source ~/.bashrc
```

### 2.1. 案例代码

```
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import os

# 从环境变量中获取 API 密钥
openai_api_key = os.getenv("OPENAI_API_KEY")
# 启用LangChain追踪
os.environ["LANGSMITH_TRACING"] = "true"
# 设置LangChain API密钥
os.environ["LANGCHAIN_API_KEY"] = "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"
# 这里输入在langsmith中创建的项目的名字
os.environ["LANGCHAIN_PROJECT"] = "default"
# 设置LangChain API端点地址
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# 初始化 ChatOpenAI 实例
chat = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=openai_api_key,
    openai_api_base="https://api.deepseek.com",
    streaming=False
)

# 构建消息列表
messages = [
    SystemMessage(content="你是一个起名大师，你的名字叫徐大师"),
    HumanMessage(content="你好徐大师, 你感觉如何？"),
    AIMessage(content="你好，我状态非常好."),
    HumanMessage(content="你叫什么名字"),
]

# 调用模型并获取响应
response = chat.invoke(messages)

# 打印响应内容
print(response.content)
```



[【LangChain教程】2025年吃透LangChain+LangGraph快速入门与底层原理教程](https://www.bilibili.com/video/BV1duKsevEwK?spm_id_from=333.788.videopod.episodes&vd_source=68a8583f88fde22ce39c9c2212b4cac4)
