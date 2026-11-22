# -*- coding: utf-8 -*-
"""
将 clash_proxies.yaml 中的代理节点合并到 clash18.yaml 的完整配置中，
保留 clash18.yaml 的端口、代理组、规则集、规则等所有其他设置，
输出 clash19.yaml。

运行前安装：
    py -3.12 -m pip install pyyaml

运行：
    py -3.12 merge_clash_yaml.py
"""

from pathlib import Path
import copy
import sys
import yaml



def load_yaml(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"找不到文件：{path.resolve()}")

    with path.open("r", encoding="utf-8-sig") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"{path.name} 内容不是有效的 YAML 字典配置")

    return data


def merge_clash_configs(base_path, proxy_path, output_path):
    # 读取完整配置和代理节点文件
    base_config = load_yaml(Path(base_path))
    proxy_config = load_yaml(Path(proxy_path))

    if "proxies" not in proxy_config:
        raise KeyError(f"{proxy_path} 中没有顶层 proxies 字段")

    new_proxies = proxy_config["proxies"]
    if not isinstance(new_proxies, list):
        raise TypeError("代理文件中的 proxies 必须是列表")

    # 检查每个节点结构及名称
    names = []
    for index, proxy in enumerate(new_proxies, start=1):
        if not isinstance(proxy, dict):
            raise TypeError(f"第 {index} 个代理节点不是字典")
        name = proxy.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"第 {index} 个代理节点缺少有效的 name")

        names.append(name)

    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        preview = "、".join(duplicates[:20])
        raise ValueError(
            f"发现 {len(duplicates)} 个重复代理名称，已停止写出：{preview}"
        )

    # 深拷贝完整配置，只替换 proxies，不改动其他配置项
    merged = copy.deepcopy(base_config)
    merged["proxies"] = copy.deepcopy(new_proxies)

    # 检查代理组引用是否能在节点名、代理组名或内置策略中找到
    proxy_names = set(names)
    groups = merged.get("proxy-groups", [])
    group_names = {
        group.get("name")
        for group in groups
        if isinstance(group, dict) and isinstance(group.get("name"), str)
    }
    builtins = {
        "DIRECT", "REJECT", "REJECT-DROP", "PASS",
        "COMPATIBLE", "GLOBAL", "待命"
    }

    missing = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        group_name = group.get("name", "<未命名代理组>")
        for key in ("proxies", "use"):
            values = group.get(key, [])
            if not isinstance(values, list):
                continue
            for item in values:
                if isinstance(item, str) and item not in (
                    proxy_names | group_names | builtins
                ):
                    missing.append((group_name, item))

    # 写入临时文件，成功后再替换目标文件，避免写到一半损坏
    output_path = Path(output_path)
    temp_path = output_path.with_suffix(output_path.suffix + ".tmp")

    with temp_path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(
            merged,
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=120,
        )

    # 再次读取临时文件，确认输出可正常解析
    check = load_yaml(temp_path)
    if check.get("proxies") != new_proxies:
        temp_path.unlink(missing_ok=True)
        raise RuntimeError("写出校验失败：输出文件中的代理节点与源文件不一致")

    temp_path.replace(output_path)

    print("=" * 60)
    print("Clash YAML 合并完成")
    print(f"完整配置：{Path(base_path).resolve()}")
    print(f"代理节点：{Path(proxy_path).resolve()}")
    print(f"输出文件：{output_path.resolve()}")
    print(f"代理节点数量：{len(new_proxies)}")
    print(f"代理组数量：{len(groups)}")
    print(f"规则数量：{len(merged.get('rules', []))}")
    print(f"规则集数量：{len(merged.get('rule-providers', {}))}")
    print(f"代理组缺失引用：{len(missing)}")

    if missing:
        print("\n以下引用在新节点和代理组中均未找到，请检查：")
        for group_name, item in missing[:50]:
            print(f"  代理组 [{group_name}] -> [{item}]")
        if len(missing) > 50:
            print(f"  ... 另有 {len(missing) - 50} 项未显示")
    else:
        print("代理组引用检查：通过")

    print("=" * 60)
    return output_path

def merge_proxies(template_file="clash18.yaml",
                  proxies_file="clash_proxies.yaml",
                  output_file="clash_proxies_full.yaml"):
    # 默认文件名：把本脚本与两个 YAML 文件放在同一目录即可
    BASE_CONFIG = Path(template_file)
    PROXY_CONFIG = Path(proxies_file)
    OUTPUT_CONFIG = Path(output_file)
    try:
        merge_clash_configs(BASE_CONFIG, PROXY_CONFIG, OUTPUT_CONFIG)
    except Exception as exc:
        print(f"\n处理失败：{type(exc).__name__}: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    merge_proxies()