## CodeLlama 是什么

Code Llama 是 Meta 开源的基于 Llama 2 的用于辅助代码生成的大模型，其中包含基础模型 (Code Llama)、Python 专业化模型 (Code Llama - Python) 和指令跟随模型 (Code Llama - Instruct)，每个模型都有 7B、13B 和 34B 参数的版本。

**Foundation models (Code Llama) **

- 简介：这些模型构成了代码生成的基石。
- 模型参数规模：它们分为三个大小：7B、13B和34B参数。
- 训练特点：
  - 7B和13B模型使用了infilling objective策略进行训练，使它们能够在集成开发环境中自动完成文件中段落的代码。
  - 34B模型并未使用此策略。
- 数据和初始化：所有模型均从Llama 2模型权重开始初始化，并在一个主要包含代码的数据集上使用500B tokens进行训练。此外，这些模型都已针对长上下文经过优化。

**Python specializations (Code Llama) **

- 简介：这些模型专为Python代码生成而设计。
- 模型参数规模：它们同样分为7B、13B和34B参数三个版本。
- 研究目的：这些模型的目标是探讨针对特定编程语言的模型与通用代码生成模型之间的性能差异。
- 数据和初始化：这些模型从Llama 2模型权重开始初始化，并在Code Llama数据集上使用500B tokens进行训练。随后，它们在一个以Python为主的数据集上针对100B tokens进行了进一步的训练。
- 特色：所有Code Llama - Python模型都在没有使用填充策略的情况下进行训练，并已优化以处理长上下文。

**Instruct-following (Code Llama) **

- 简介：这些模型在Code Llama的基础上微调，旨在更精确地遵循人类指示。
- 微调数据：这些模型接受了约5B tokens的额外微调。

## 下载模型

第一步: 先在 [Meta AI](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) 网站填写个人信息并同意协议，提交之后会收到一封名为 `Get started with Code Llama` 的邮件，里面有个 `https://download2.llamameta.net/*?Policy=...`开头的链接。

第一步: 克隆代码到本地。

```bash
  # 克隆代码
  git clone https://github.com/facebookresearch/codellama.git
  # 进入代码目录
  cd codellama
  # 执行下载命令
  bash download.sh
```

- 按提示把邮件里的链接粘贴到终端，然后再按提示输入需要下载的模型，等待模型下载完成。

## 创建虚拟环境

```python
# 创建虚拟环境，基于 python3.10 版
conda create -n codellama python==3.10 -y
# 激活虚拟环境
conda activate codellama
# 安装 pytorch 等必要的库
# 参考 https://pytorch.org/get-started/locally/
# 比如我的 cuda 版本是 11.8 安装方法如下
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# 安装 code llama 依赖
pip install -e .
```

## 测试code llama代码填充

具体可以查看 `example_completion.py` 代码，输入了两段代码片段，然后 code llama 会自动补全代码。

```python
# 进入 codellama 目录
cd codellama
# 激活虚拟环境
conda activate codellama
# 假设下载的模型是 CodeLlama-7b
CUDA_VISIBLE_DEVICES=1 torchrun --nproc_per_node 1 example_completion.py \
    --ckpt_dir CodeLlama-7b/ \
    --tokenizer_path CodeLlama-7b/tokenizer.model \
    --max_seq_len 128 --max_batch_size 4
```

出现这样的结果就说明 code llama 已经可以正常使用了。

## 在 VS Code 中使用 code llama

code llama 在 vscode 中使用，需要使用 vscode 的 continue 插件（[官网](https://continue.dev/)），以及通过 [这个项目](https://github.com/xNul/code-llama-for-vscode/tree/main) 启动 api 服务。

**安装 continue 插件**

在 vscode 的插件搜索 continue，然后安装即可。

**continue 配置 code llama**

参考官方文档 [continue 官方文档](https://continue.dev/docs/customization), 修改配置文件 `~/.continue/config.py`

**方案 1 开启 api 服务，这里使用模型 CodeLlama-7b-Instruct**

按照这里的说明 [code-llama-for-vscode](https://github.com/xNul/code-llama-for-vscode/tree/main)，下载 https://github.com/xNul/code-llama-for-vscode/blob/main/llamacpp_mock_api.py 到 codellama 目录下，然后执行下面命令即可启动 api 服务。如果要更改端口号，可以在 `llamacpp_mock_api.py` 文件中修改`port: int = 8000,`，默认是 8000 端口。

```python
CUDA_VISIBLE_DEVICES=1 torchrun --nproc_per_node 1 llamacpp_mock_api.py \
    --ckpt_dir CodeLlama-7b-Instruct/ \
    --tokenizer_path CodeLlama-7b-Instruct/tokenizer.model \
    --max_seq_len 512 --max_batch_size 4
```



## 参考链接

1. https://www.bingal.com/posts/code-llama-usage/