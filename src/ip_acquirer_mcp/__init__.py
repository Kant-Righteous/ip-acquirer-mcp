# server.py
from mcp.server.fastmcp import FastMCP
import psutil
import requests
import socket
import ipaddress
from typing import Literal

# Create an MCP server
mcp = FastMCP("Demo")


def get_ip_type(ip: str) -> Literal["loopback", "link-local", "private", "public"]:
    """
    判断IP地址类型
    
    Args:
        ip: IP地址字符串
    
    Returns:
        "loopback": 回环地址
        "link-local": 链路本地地址
        "private": 内网地址
        "public": 公网地址
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        
        # 处理特殊情况
        if ip_obj.is_loopback:
            return "loopback"
        
        # IPv4特殊判断
        if isinstance(ip_obj, ipaddress.IPv4Address):
            # 链路本地地址 (169.254.0.0/16)
            if ip.startswith("169.254."):
                return "link-local"
            
        # IPv6特殊判断
        elif isinstance(ip_obj, ipaddress.IPv6Address):
            # IPv6链路本地地址 (fe80::/10)
            if ip_obj.is_link_local:
                return "link-local"
            # IPv6唯一本地地址 (fc00::/7)
            if ip_obj.is_private:
                return "private"
                
        # 内网地址判断
        if ip_obj.is_private:
            return "private"
            
        return "public"
        
    except ValueError:
        return "public"  # 无法解析的IP默认为public

@mcp.tool()
def get_ip_info() -> dict:
    """
    获取本机所有网卡的详细内网IP信息和公网IP
    
    Returns:
        dict: {
            "interfaces": [
                {
                    "name": str,  # 网卡名称
                    "mac": str,   # MAC地址
                    "ips": [
                        {
                            "address": str,  # IP地址
                            "family": str,   # IPv4或IPv6
                            "type": str     # loopback/link-local/private/public
                        }
                    ]
                }
            ],
            "public_ip": str  # 通过外部服务获取的公网IP
        }
    """
    interfaces = []
    for name, addrs in psutil.net_if_addrs().items():
        iface = {"name": name, "mac": None, "ips": []}
        for addr in addrs:
            if addr.family == socket.AF_INET:  # IPv4
                ip_type = get_ip_type(addr.address)
                iface["ips"].append({
                    "address": addr.address,
                    "family": "IPv4",
                    "type": ip_type
                })
            elif addr.family == socket.AF_INET6:  # IPv6
                ip_type = get_ip_type(addr.address)
                iface["ips"].append({
                    "address": addr.address,
                    "family": "IPv6",
                    "type": ip_type
                })
            elif addr.family == psutil.AF_LINK:  # MAC地址
                iface["mac"] = addr.address
        
        # 只添加有IP的接口
        if iface["ips"]:
            interfaces.append(iface)
            
    # 获取公网IP
    try:
        resp = requests.get("https://api.ipify.org?format=json", timeout=3)
        public_ip = resp.json().get("ip", "")
    except Exception:
        public_ip = None

    result = {
        "interfaces": interfaces,
        "public_ip": public_ip
    }

    return result


def main() -> None:
    mcp.run(transport="stdio")
