# Ollama基础入门

Ollama是一个专为在本地环境中运行和定制大型语言模型而设计的工具。它提供了一个简单而高效的接口，用于创建、运行和管理这些模型，同时还提供了一个丰富的预构建模型库，可以轻松集成到各种应用程序中。Ollama的目标是使大型语言模型的部署和交互变得简单，无论是对于开发者还是对于终端用户。

## 1. Ollama

### 1.1 什么是Ollama?

**Ollama**官网：https://ollama.com/，官方网站的介绍就一句话：**Get up and running with large language models.** （开始使用大语言模型）。Ollama是一个开源的 LLM（大型语言模型）服务工具，用于简化在本地运行大语言模型，降低使用大语言模型的门槛，使得大模型的开发者、研究人员和爱好者能够在本地环境快速实验、管理和部署最新大语言模型, 包括如Qwen2、Llama3、Phi3、Gemma2等开源的大型语言模型，Ollama是大语言模型便捷的管理和运维工具。Llama是 Meta 公司开源的备受欢迎的一个通用大语言模型，和其他大模型一样，Llama可以通过Ollama进行管理部署和推理等。

**Ollama**支持的大语言模型列表，可通过搜索模型名称查看：https://ollama.com/library

**Ollama**官方 GitHub 源代码仓库：[https://github.com/ollama/ollama/](https://github.com/ollama/ollama)

### 1.2 安装Ollama大语言模型工具

在官网首页，我们可以直接下载**Ollama**安装程序（支持 Windows/MacOS/Linux）：https://ollama.com/

**Ollama**的安装过程，与安装其他普通软件并没有什么两样，安装完成之后，有几个常用的系统**环境变量**参数建议进行设置：

1. **OLLAMA_MODELS**：模型文件存放目录，默认目录为当前用户目录（Windows 目录：`C:\Users%username%.ollama\models`，MacOS 目录：`~/.ollama/models`，Linux 目录：`/usr/share/ollama/.ollama/models`），如果是 Windows 系统**建议修改**（如：D:\OllamaModels），避免 C 盘空间吃紧。
2. **OLLAMA_HOST**：Ollama 服务监听的网络地址，默认为**127.0.0.1**，如果允许其他电脑访问 Ollama（如：局域网中的其他电脑），**建议设置**成**0.0.0.0**，从而允许其他网络访问。
3. **OLLAMA_PORT**：Ollama 服务监听的默认端口，默认为**11434**，如果端口有冲突，可以修改设置成其他端口（如：**8080**等）。
4. **OLLAMA_ORIGINS**：HTTP 客户端请求来源，半角逗号分隔列表，若本地使用无严格要求，可以设置成星号，代表不受限制。
5. **OLLAMA_KEEP_ALIVE**：大模型加载到内存中后的存活时间，默认为**5m**即 5 分钟（如：纯数字如 300 代表 300 秒，0 代表处理请求响应后立即卸载模型，任何负数则表示一直存活）；我们可设置成**24h**，即模型在内存中保持 24 小时，提高访问速度。
6. **OLLAMA_NUM_PARALLEL**：请求处理并发数量，默认为**1**，即单并发串行处理请求，可根据实际情况进行调整。
7. **OLLAMA_MAX_QUEUE**：请求队列长度，默认值为**512**，可以根据情况设置，超过队列长度请求被抛弃。
8. **OLLAMA_DEBUG**：输出 Debug 日志标识，应用研发阶段可以设置成**1**，即输出详细日志信息，便于排查问题。
9. **OLLAMA_MAX_LOADED_MODELS**：最多同时加载到内存中模型的数量，默认为**1**，即只能有 1 个模型在内存中。

#### 1.3 Ollama 管理本地已有大模型

- 展示本地大模型列表：`ollama list`

```bash
>ollama list
NAME            ID              SIZE    MODIFIED
gemma2:9b       c19987e1e6e2    5.4 GB  7 days ago
qwen2:7b        e0d4e1163c58    4.4 GB  10 days ago
```

- 删除单个本地大模型：`ollama rm 本地模型名称`

```bash
>ollama rm gemma2:9b
deleted 'gemma2:9b'

>ollama list
NAME            ID              SIZE    MODIFIED
qwen2:7b        e0d4e1163c58    4.4 GB  10 days ago
```

- 启动本地模型：`ollama run 本地模型名`, 启动成功之后，就可以通过终端对话界面进行对话

```bash
>ollama run qwen2:0.5b
>>>
```

- 查看本地运行中模型列表：`ollama ps`

```bash
>ollama ps
NAME            ID              SIZE    PROCESSOR       UNTIL
qwen2:0.5b      6f48b936a09f    693 MB  100% CPU        4 minutes from now
```

- 复制本地大模型：`ollama cp 本地存在的模型名 新复制模型名`

```bash
>ollama cp qwen2:0.5b Qwen2-0.5B
copied 'qwen2:0.5b' to 'Qwen2-0.5B'

>ollama list
NAME                    ID              SIZE    MODIFIED
Qwen2-0.5B:latest       6f48b936a09f    352 MB  4 seconds ago
qwen2:0.5b              6f48b936a09f    352 MB  29 minutes ago
qwen2:7b                e0d4e1163c58    4.4 GB  10 days ago
```

#### 1.4 Ollama下载大模型

##### 1.4.1 Ollama 从远程仓库下载大模型到本地

- 下载或者更新本地大模型：`ollama pull 本地/远程仓库模型名称`

本`pull`命令从 Ollama 远程仓库完整下载或增量更新模型文件，模型名称格式为：**模型名称:参数规格**；如`ollama pull qwen2:0.5b` 则代表从 Ollama 仓库下载qwen2大模型的0.5b参数规格大模型文件到本地磁盘。

如果参数规格标记为`latest`则代表为默认参数规格，下载时可以不用指定，如Qwen2的7b被标记为latest，则`ollama pull qwen2`和`ollama pull qwen2:7b`这 2 个命令的意义是一样的，都下载的为7b参数规格模型。为了保证后续维护方便、避免误操作等，建议不管是否为默认参数规格，我们下载命令中均明确参数规格。

```bash
>ollama pull qwen2:0.5b
pulling manifest
pulling manifest
pulling manifest
pulling manifest
pulling manifest
pulling 8de95da68dc4... 100% ▕████████████████████████▏ 352 MB
pulling 62fbfd9ed093... 100% ▕████████████████████████▏  182 B
pulling c156170b718e... 100% ▕████████████████████████▏  11 KB
pulling f02dd72bb242... 100% ▕████████████████████████▏   59 B
pulling 2184ab82477b... 100% ▕████████████████████████▏  488 B
verifying sha256 digest
writing manifest
removing any unused layers
success

>ollama list
NAME            ID              SIZE    MODIFIED
qwen2:0.5b      6f48b936a09f    352 MB  9 minutes ago
qwen2:7b        e0d4e1163c58    4.4 GB  10 days ago
```

若本地不存在该大模型，则下载完整模型文件到本地磁盘；若本地磁盘存在该大模型，则增量下载大模型更新文件到本地磁盘。

- 下载且运行本地大模型：`ollama run 本地/远程仓库模型名称`

```bash
>ollama run qwen2:0.5b
>>>
```

若本地不存在大模型，则下载完整模型文件到本地磁盘（类似于pull命令），然后启动大模型；若本地存在大模型，则直接启动（不进行更新）。启动成功后，默认为终端对客界面：

![](images/04.png)

1. 若需要输入多行文本，需要用**三引号**包裹，如：`"""这里是多行文本"""`
2. `/clear`清除对话上下文信息
3. `/bye`则退出对话窗口
4. `/set parameter num_ctx 4096`可设置窗口大小为 4096 个 Token，也可以通过请求设置，如：`curl <http://localhost:11434/api/generate> -d '{ "model": "qwen2:7b", "prompt": "Why is the sky blue?", "options": { "num_ctx": 4096 }}'`
5. `/show info`可以查看当前模型详情：

```bash
>>> /show info
  Model
        arch                    qwen2
        parameters              494.03M
        quantization            Q4_0
        context length          32768
        embedding length        896
 
  Parameters
        stop    "<|im_start|>"
        stop    "<|im_end|>"
 
  License
        Apache License
        Version 2.0, January 2004
```

##### 1.4.2 Ollama 导入 GGUF 模型文件到本地磁盘

若我们已经从 HF 或者 ModeScope 下载了 GGUF 文件（文件名为：**Meta-Llama-3-8B-Instruct.Q4_K_M.gguf**），在我们存放`Llama3-8B`的 GGUF 模型文件目录中，创建一个文件名为`Modelfile`的文件，该文件的内容如下：

```bash
FROM ./Meta-Llama-3-8B-Instruct.Q4_K_M.gguf
```

然后，打开终端，执行命令导入模型文件：`ollama create 模型名称 -f ./Modelfile`

```bash
>ollama create Llama-3-8B -f ./Modelfile
transferring model data
using existing layer sha256:647a2b64cbcdbe670432d0502ebb2592b36dd364d51a9ef7a1387b7a4365781f
creating new layer sha256:459d7c837b2bd7f895a15b0a5213846912693beedaf0257fbba2a508bc1c88d9
writing manifest
success
```

导入成功之后，我们就可以通过`list`命名，看到名为**Llama-3-8B**的本地模型了，后续可以和其他模型一样进行管理了。

##### 1.4.3 Ollama 导入 safetensors 模型文件到本地磁盘

官方操作文档：https://ollama.fan/getting-started/import/#importing-pytorch-safetensors

若我们已经从 HF 或者 ModeScope 下载了 safetensors 文件.

```bash
git lfs install
 
git clone https://www.modelscope.cn/rubraAI/Mistral-7B-Instruct-v0.3.git Mistral-7B
```

然后，我们转换模型（结果：`Mistral-7B-v0.3.bin`）：

```bash
python llm/llama.cpp/convert.py ./Mistral-7B --outtype f16 --outfile Mistral-7B-v0.3.bin
```

接下来，进行量化：

```bash
llm/llama.cpp/quantize Mistral-7B-v0.3.bin Mistral-7B-v0.3_Q4.bin q4_0
```

最后，通过 Ollama 导入到本地磁盘，创建`Modelfile`模型文件：

```bash
FROM Mistral-7B-v0.3_Q4.bin
```

执行导入命令，导入模型文件：`ollama create 模型名称 -f ./Modelfile`

```bash
>ollama create Mistral-7B-v0.3 -f ./Modelfile
transferring model data
using existing layer sha256:647a2b64cbcdbe670432d0502ebb2592b36dd364d51a9ef7a1387b7a4365781f
creating new layer sha256:459d7c837b2bd7f895a15b0a5213846912693beedaf0257fbba2a508bc1c88d9
writing manifest
success
```

导入成功之后，我们就可以通过`list`命名，看到名为**Mistral-7B-v0.3**的本地模型了，后续可以和其他模型一样进行管理了。



**参考**

1. [https://www.cnblogs.com/obullxl/p/18295202/NTopic2024071001](https://www.cnblogs.com/obullxl/p/18295202/NTopic2024071001)