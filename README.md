# thinking-in-llm

在thinking-in-llm 目录中执行 `make html`，就会在 build/html 目录生成 html 相关文件。可以在浏览器中打开 index.html。

```bash
make html
```

当然，直接访问 html 文件不是很方便，所以我们借助 `sphinx-autobuild` 工具启动 HTTP 服务。

```bash
sphinx-autobuild source build/html
```
