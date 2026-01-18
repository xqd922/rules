# Rules

Clash/Mihomo 规则集合

## 快速开始

编辑 `*/src/*.yaml` → 推送 → 自动编译为 `.mrs`

**[详细使用文档](docs/usage.md)**

## 当前规则

| 规则 | 文件 | URL |
|------|------|-----|
| Emby | `emby/emby-domain.mrs` | [链接](https://raw.githubusercontent.com/xqd922/rules/main/emby/emby-domain.mrs) |

## 配置示例

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
