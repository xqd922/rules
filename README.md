# Rules

Clash/Mihomo 规则集合

## Emby

| 文件 | 类型 | 说明 |
|------|------|------|
| `emby/emby-domain.mrs` | domain | Emby 域名规则 |
| `emby/emby-ip.mrs` | ipcidr | Emby IP 规则 |

### 使用方法

```yaml
rule-providers:
  emby:
    type: http
    behavior: domain
    format: mrs
    url: 'https://raw.githubusercontent.com/xqd922/rules/main/emby/emby-domain.mrs'
    path: './rule_providers/emby.mrs'
    interval: 86400
  emby-ip:
    type: http
    behavior: ipcidr
    format: mrs
    url: 'https://raw.githubusercontent.com/xqd922/rules/main/emby/emby-ip.mrs'
    path: './rule_providers/emby_ip.mrs'
    interval: 86400

rules:
  - RULE-SET,emby,Emby
  - RULE-SET,emby-ip,Emby,no-resolve
```
