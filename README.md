# IP Acquirer MCP

一个通过 MCP 协议获取本机详细内网IP信息和公网IP的工具。

## 功能

-   遍历所有网络接口，获取详细的 IP 配置 (IPv4/IPv6)。
-   区分 IP 地址类型（私有、公网、回环等）。
-   通过外部服务查询公网 IP 地址。
-   提供一个 MCP 工具 `get_ip_info` 以便其他程序调用。
-   提供一个命令行入口 `ip-acquirer` 直接启动服务。

## 安装

您可以从 PyPI 安装此工具：

```bash
pip install ip-acquirer-mcp
```

## 使用方法

### 作为命令行工具

安装后，您可以直接在终端中运行以下命令来启动 MCP 服务：

```bash
ip-acquirer
```

服务将通过标准输入/输出 (stdio) 进行通信。

### 作为库

您也可以在自己的 Python 代码中导入并使用 `get_ip_info` 工具，但这通常在 MCP 客户端的上下文中进行。

核心函数位于 `ip_acquirer_mcp/__init__.py` 中。

## 开发

1.  克隆仓库
2.  创建虚拟环境: `python -m venv .venv`
3.  激活虚拟环境
4.  安装依赖: `pip install -e .`
