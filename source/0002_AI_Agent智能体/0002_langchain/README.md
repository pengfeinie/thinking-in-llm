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

### 1.2. 案例代码

```python
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

### 1.3. 部署LangChain程序

[ LangServe](https://python.langchain.com/docs/langserve/)

```bash
pip install "langserve[all]"
```

```python
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI
import uvicorn
from pydantic import BaseModel

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

prompt = PromptTemplate.from_template(template="你是一个{name}, 帮我起一个具有{country}特色的{sex}名字.")
messages = prompt.format(name="算命大师", country="法国", sex="女孩")

output_parser = StrOutputParser()

chain = chat | output_parser

app = FastAPI(title="我的Langchain服务", version="v10")


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# 定义请求体模型
class NameRequest(BaseModel):
    name: str
    country: str
    sex: str

app = FastAPI(title="我的Langchain服务", version="v10")

@app.post("/generate_name/")
async def generate_name(request: NameRequest):
    try:
        # 使用提取的参数调用模型
        prompt = PromptTemplate.from_template(template="你是一个{name}, 帮我起一个具有{country}特色的{sex}名字.")
        messages = prompt.format(name=request.name, country=request.country, sex=request.sex)
        response = chain.invoke(messages)
        return {"generated_name": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 添加 LangChain 路由
add_routes(app, chat | StrOutputParser(), path="/chain")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```



[【LangChain教程】2025年吃透LangChain+LangGraph快速入门与底层原理教程](https://www.bilibili.com/video/BV1duKsevEwK?spm_id_from=333.788.videopod.episodes&vd_source=68a8583f88fde22ce39c9c2212b4cac4)
