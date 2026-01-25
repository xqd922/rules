# Rules

Clash/Mihomo 和 sing-box 规则集合

## 快速开始

编辑 `*/src/*.yaml` → 推送 → 自动编译为 `.mrs` (Mihomo) 和 `.srs` (sing-box)

**[详细使用文档](docs/usage.md)**

## 当前规则

| 规则 | Mihomo (MRS) | sing-box (SRS) |
|------|--------------|----------------|
| Emby | [emby-domain.mrs](https://raw.githubusercontent.com/xqd922/rules/main/emby/emby-domain.mrs) | [emby-domain.srs](https://raw.githubusercontent.com/xqd922/rules/main/emby/emby-domain.srs) |

## 配置示例

### Mihomo / Clash.Meta

```yaml
rule-providers:
  emby:
    type: http
    behavior: domain
    format: mrs
    url: 'https://raw.githubusercontent.com/xqd922/rules/main/emby/emby-domain.mrs'
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
        "url": "https://raw.githubusercontent.com/xqd922/rules/main/emby/emby-domain.srs",
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
