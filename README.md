# Search MCP Server

![image](./images/logo.png)

一个基于MCP协议的搜索服务实现，提供网络搜索和本地搜索功能，Cursor和Claude Desktop能与之无缝集成。

使用Python开发，支持异步处理和高并发请求，搜索调用Brave Search API。

本实现参考TS版本的Brave Search，TS版本在Cursor里面无法集成使用，不知道是我环境有问题还是什么原因，由于自己用python实现了可用的这一版本。

更多MCP知识，见AI全书([ 一文看懂什么是MCP(大模型上下文)？用来干什么的？怎么用它？](https://aibook.ren/archives/mcp-course))

## 使用示例

![image](./images/demo.png)

## 功能特点

- **网络搜索**: 基于Brave Search API在线实时搜索
- **适用场景**: Claude Desktop或者Cursor集成使用，大大扩展工具的内容获取能力

## 工具列表

- **web_search**
  
  - 执行网络搜索，支持分页和过滤
  - 输入参数:
    - `query` (string): 搜索关键词
    - `count` (number, 可选): 每页结果数量(最大20)
    - `offset` (number, 可选): 分页偏移量(最大9)

- **local_search**
  
  - 搜索本地商家和服务
  - 输入参数:
    - `query` (string): 本地搜索关键词
    - `count` (number, 可选): 结果数量(最大20)
  - 无本地结果时自动切换到网络搜索

## 环境要求

- Python 3.9+
- uv 0.24.0+
- 异步支持库: `asyncio`, `httpx`
- MCP协议库: `mcp-server`
- 注意！需要科学上网！

**环境安装**

1. 安装uv
   
   ```bash
   # Linux环境
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Windows环境 
   pip install uv
   ```

2. 安装依赖模块
   
   ```bash
   pip install mcp
   pip install httpx
   pip install 
   ```

## 配置说明

### 下载源码

```bash
git clone https://github.com/fengin/search-server.git
```

### 获取API密钥

1. 注册[搜索API账号]([Brave Search API | Brave](https://brave.com/search/api/)) 
2. 选择合适的套餐(提供免费套餐，每月2000次查询)
3. 在开发者面板生成API密钥

### 环境变量配置

方式一：环境配置：

```bash
export SEARCH_API_KEY="your_api_key_here"
```

方式二：或者集成的工具（claude desktop或者cursor）里配置指定 

方式三：打开serve.py，在以下代码里修改为你的api key:

```python
# 检查API密钥
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
if not BRAVE_API_KEY:
    BRAVE_API_KEY = "你的api key"
```

### 与Claude Desktop集成

在`claude_desktop_config.json`中添加:

```json
{
  "mcpServers": {
    "search": {
      "command": "python",
      "args": [
        "-m",
        "search.server"
      ],
      "env": {
        "SEARCH_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

### 与Cursor集成

打开cursor的MCP Servers配置，入口：

文件—>首选项—>Cursor Settings—>Features—>MCP Server—>Add new MCP Server

配置项内容：

```bash
name: search
type: command
command: uv --directory D:\\code\\search-server run search
```

其中D:\code\search-server修改为你自己的代码目录位置

### 

## 速率限制

- 每秒请求数: 1
- 每月请求数: 15000

超出限制时会返回相应的错误信息。

## 开发说明

项目使用Python异步编程模型，主要依赖:

- `asyncio`: 异步IO支持
- `httpx`: 异步HTTP客户端
- `mcp`: MCP协议实现

代码结构:

```shell
search/
├── __init__.py
├── server.py      # 主服务实现
└── utils/         # 工具函数
```

## 许可证

本项目采用MIT许可证。您可以自由使用、修改和分发本软件，但需遵守MIT许可证的条款和条件。详细信息请参见项目中的LICENSE文件。

作者：凌封 （微信fengin）

网站：https://aibook.ren（AI全书）
