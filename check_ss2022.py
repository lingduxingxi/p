
import json
import base64
from pathlib import Path

config_path = Path(r"D:\客户端集合代理\SS1_configs_port10801.json")

with config_path.open("r", encoding="utf-8-sig") as f:
    config = json.load(f)

# 同时兼容单节点和 servers 列表格式
if isinstance(config, dict) and isinstance(config.get("servers"), list):
    servers = config["servers"]
elif isinstance(config, list):
    servers = config
else:
    servers = [config]

for index, node in enumerate(servers, 1):
    if not isinstance(node, dict):
        continue

    method = node.get("method", "")
    if not str(method).startswith("2022-blake3-"):
        continue

    password = str(node.get("password", ""))
    parts = password.split(":")

    print(f"\n节点 #{index}")
    print("服务器：", node.get("server", ""))
    print("端口：", node.get("server_port", ""))
    print("加密方式：", method)
    print("密码分段数：", len(parts))

    for part_index, part in enumerate(parts, 1):
        print(f"  第 {part_index} 段字符数：{len(part)}")

        try:
            decoded = base64.b64decode(part, validate=True)
            print(f"  第 {part_index} 段 Base64：有效")
            print(f"  解码长度：{len(decoded)} 字节")
        except Exception as exc:
            print(f"  第 {part_index} 段 Base64：无效")
            print(f"  错误：{exc}")

print("\n检查完成。")
