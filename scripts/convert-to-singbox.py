#!/usr/bin/env python3
"""
将 Mihomo YAML 规则转换为 sing-box JSON 格式

Mihomo 格式:
  payload:
    - example.com        # DOMAIN
    - +.example.org      # DOMAIN-SUFFIX

sing-box 格式:
  {
    "version": 2,
    "rules": [
      { "domain": ["example.com"] },
      { "domain_suffix": ["example.org"] }
    ]
  }
"""

import json
import sys
import yaml
from pathlib import Path


def convert_mihomo_to_singbox(yaml_content: dict, rule_type: str = "domain") -> dict:
    """将 Mihomo YAML 规则转换为 sing-box JSON 格式"""

    payload = yaml_content.get("payload", [])

    if rule_type == "domain":
        domains = []
        domain_suffixes = []

        for item in payload:
            if item is None:
                continue
            item = str(item).strip()
            if not item or item.startswith("#"):
                continue

            if item.startswith("+."):
                # DOMAIN-SUFFIX: +.example.com -> example.com
                domain_suffixes.append(item[2:])
            else:
                # DOMAIN: example.com
                domains.append(item)

        rules = []
        if domains:
            rules.append({"domain": domains})
        if domain_suffixes:
            rules.append({"domain_suffix": domain_suffixes})

        return {"version": 2, "rules": rules}

    elif rule_type == "ipcidr":
        ip_cidrs = []

        for item in payload:
            if item is None:
                continue
            item = str(item).strip()
            if not item or item.startswith("#"):
                continue
            ip_cidrs.append(item)

        rules = []
        if ip_cidrs:
            rules.append({"ip_cidr": ip_cidrs})

        return {"version": 2, "rules": rules}

    else:
        raise ValueError(f"Unsupported rule type: {rule_type}")


def main():
    if len(sys.argv) < 3:
        print("Usage: convert-to-singbox.py <input.yaml> <output.json> [domain|ipcidr]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    rule_type = sys.argv[3] if len(sys.argv) > 3 else "domain"

    # 根据文件名自动判断类型
    if rule_type == "auto":
        filename = input_file.stem.lower()
        if "ip" in filename or "cidr" in filename:
            rule_type = "ipcidr"
        else:
            rule_type = "domain"

    with open(input_file, "r", encoding="utf-8") as f:
        yaml_content = yaml.safe_load(f)

    singbox_json = convert_mihomo_to_singbox(yaml_content, rule_type)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(singbox_json, f, ensure_ascii=False, indent=2)

    print(f"Converted {input_file} -> {output_file} (type: {rule_type})")


if __name__ == "__main__":
    main()
