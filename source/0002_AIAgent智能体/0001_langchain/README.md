# AI Agent入门到精通





## 1. 环境安装

```python
安装Python3.10.2版本: 
https://mirrors.huaweicloud.com/python/3.10.2/
pip install --upgrade pip --user

安装jupyterlab
官网：https://jupyter.org/install
命令安装: pip install jupyterlab==4.3.5 -i https://pypi.mirrors.ustc.edu.cn --user
启动：jupyter-lab
```

## 2. 使用openai测试Deepseek

```python
安装openai
pip install openai==1.65.2 --user
```

```python
# Please install OpenAI SDK first: `pip install openai==1.65.2 --user`

from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
```

## 3. 使用langchain测试Deepseek

```python
pip install langchain==0.3.19
pip install langchain_community==0.3.18
pip install langchain-openai==0.3.7
```

### 3.1 例子1

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# 1. 创建 ChatOpenAI 实例
chat = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key="sk-bf9cb507120c42d49366e6aabd1f4157",
    openai_api_base="https://api.deepseek.com",
    streaming=False
)

# 2. 创建消息列表
messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="介绍一下你自己"),
]

# 3. 调用模型并获取响应
response = chat(messages)

# 4. 打印响应内容
print(response.content)
```

![](images/2025-03-03_180314.png)

### 3.1 例子2

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# 初始化 ChatOpenAI 实例
chat = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key="sk-bf9cb507120c42d49366e6aabd1f4157",
    openai_api_base="https://api.deepseek.com",
    streaming=False
)

# 构建消息列表
messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="介绍一下你自己"),
]

# 调用模型并获取响应
response = chat.invoke(messages)

# 打印响应内容
print(response.content)
```

### 3.1 例子3

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# 初始化 ChatOpenAI 实例
chat = ChatOpenAI(
    model="deepseek-r1:1.5b",
    openai_api_key="sk-bf9cb507120c42d49366e6aabd1f4157",
    openai_api_base="http://localhost:11434/v1",
    streaming=False
)

# 构建消息列表
messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="介绍一下你自己"),
]

# 调用模型并获取响应
response = chat.invoke(messages)

# 打印响应内容
print(response.content)
```

