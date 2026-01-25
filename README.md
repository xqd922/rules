# Rules

Clash/Mihomo 和 sing-box 规则集合

## 目录结构

```
emby/
├── src/
│   ├── mihomo/
│   │   └── emby.yaml           # Mihomo 源文件
│   └── singbox/
│       └── emby.json           # sing-box 源文件
├── emby.mrs                    # Mihomo 输出
└── emby.srs                    # sing-box 输出
```

## 快速开始

- **Mihomo**：编辑 `*/src/mihomo/*.yaml` → 推送 → 自动编译为 `.mrs`
- **sing-box**：编辑 `*/src/singbox/*.json` → 推送 → 自动编译为 `.srs`

## 当前规则

| 规则 | Mihomo (MRS) | sing-box (SRS) |
|------|--------------|----------------|
| Emby | [emby.mrs](https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.mrs) | [emby.srs](https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.srs) |

## 格式差异

| 规则类型 | Mihomo MRS | sing-box SRS |
|----------|------------|--------------|
| DOMAIN | ✅ | ✅ |
| DOMAIN-SUFFIX | ✅ | ✅ |
| DOMAIN-KEYWORD | ❌ | ✅ |
| IP-CIDR | ✅ | ✅ |

## 配置示例

### Mihomo / Clash.Meta

```yaml
rule-providers:
  emby:
    type: http
    behavior: domain
    format: mrs
    url: 'https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.mrs'
    path: './rule_providers/emby.mrs'
    interval: 86400

rules:
  - RULE-SET,emby,Emby
```

### sing-box

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "emby",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.srs",
        "download_detour": "proxy"
      }
    ],
    "rules": [
      {
        "rule_set": "emby",
        "outbound": "Emby"
      }
    ]
  }
}
```

## 详细文档

- [使用指南](docs/usage.md)
