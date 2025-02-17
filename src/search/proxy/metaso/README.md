# Metaso Python SDK

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**作者**：凌封（微信：fengin）  
**网站**：[AI全书](https://aibook.ren)

一个用于访问秘塔搜索服务的 Python SDK，支持高速流式输出、全网搜索和学术搜索，提供简洁、深入、研究三种模式。

## 功能特点

- 支持异步操作和流式输出
- 支持全网搜索和学术搜索
- 提供三种搜索模式：
  - 简洁模式：回答简短精炼
  - 深入模式：回答详细全面
  - 研究模式：回答深度分析
- 支持多账号配置
- 完善的错误处理机制
- 跨平台支持（Windows/macOS/Linux）

## 安装

### 依赖要求

- Python 3.7+
- Playwright
- aiohttp
- asyncio

### 安装步骤

1. 安装 Python 包：
```bash
pip install -r requirements.txt
```

2. 安装 Playwright 浏览器：
```bash
playwright install
```

## 获取凭证

需要从秘塔搜索获取 `uid` 和 `sid`：

1. 访问 [秘塔AI搜索](https://metaso.cn/) 并登录账号（**建议登录账号，否则可能遭遇奇怪的限制**）
2. 打开浏览器开发者工具（F12）
3. 切换到 Application > Cookies 标签页
4. 找到 `uid` 和 `sid` 的值
5. 分别记录这两个值用于初始化客户端

![获取uid-sid](https://raw.githubusercontent.com/LLM-Red-Team/metaso-free-api/main/doc/example-0.png)

## 使用示例

### 基本使用

```python
import asyncio
from metaso import MetasoClient

async def main():
    # 初始化客户端
    async with MetasoClient("your_uid", "your_sid") as client:
        # 使用默认模型(detail)进行对话
        result = await client.get_completion("介绍一下杭州西湖的主要景点")
        
        # 获取主要内容
        print(result["content"])
        
        # 处理参考文献
        for ref in result["references"]:
            print(f"[{ref['id']}] {ref['title']}")
            
        # 使用完整的markdown格式
        print(result["markdown"])

asyncio.run(main())
```

### 流式输出

```python
import asyncio
from metaso import MetasoClient

async def main():
    async with MetasoClient("your_uid", "your_sid") as client:
        # 使用流式输出
        async for chunk in client.get_completion_stream("详细介绍杭州西湖十景"):
            print(chunk, end="", flush=True)

asyncio.run(main())
```

### 使用不同模型

```python
import asyncio
from metaso import MetasoClient

async def main():
    async with MetasoClient("your_uid", "your_sid") as client:
        # 使用研究模式
        result = await client.get_completion(
            "分析人工智能对未来教育的影响", 
            model="research"
        )
        print(result["content"])

asyncio.run(main())
```

## 返回数据结构

非流式调用返回一个包含以下字段的字典：

```python
{
    "content": str,      # 主要内容文本
    "references": [      # 参考文献列表
        {
            "id": str,           # 引用ID
            "title": str,        # 标题
            "link": str,         # 链接
            "snippet": str,      # 摘要
            "source": str,       # 来源
            "date": str          # 日期
        }
    ],
    "markdown": str,     # 完整的markdown格式文本
    "meta": {           # 元数据信息
        "model": str,           # 使用的模型
        "conversation_id": str,  # 会话ID
        "query": str,           # 查询内容
        "timestamp": int        # 时间戳
    }
}
```

## 支持的模型

### 全网搜索模型
- `concise`: 简洁模式
- `detail`: 深入模式（默认）
- `research`: 研究模式

### 学术搜索模型
- `concise-scholar`: 学术-简洁模式
- `detail-scholar`: 学术-深入模式
- `research-scholar`: 学术-研究模式

## 注意事项

1. **浏览器数据目录**
   - 默认使用 `tmp/browser` 目录
   - 可以通过构造函数参数 `browser_data_dir` 自定义

2. **错误处理**
   - 使用 try/except 捕获 MetasoException
   - 查看具体的错误码和消息

3. **性能优化**
   - 建议复用 MetasoClient 实例
   - 使用异步操作提高并发性能

4. **安全建议**
   - 妥善保管凭证信息
   - 建议使用环境变量管理敏感信息

## 免责声明

**逆向API是不稳定的，建议前往秘塔AI官方 https://metaso.cn/ 使用，避免封禁的风险。**

**本项目仅用于个人学习研究，请勿用于商业用途。使用本项目时请遵守相关服务条款和法律法规。** 