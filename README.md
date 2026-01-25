# Rules

Clash/Mihomo 和 sing-box 规则集合

## 目录结构

```
emby/
├── src/
│   ├── mihomo/
│   │   └── emby.yaml       # Mihomo 源文件
│   └── singbox/
│       └── emby.json       # sing-box 源文件
├── emby.mrs                # Mihomo 输出
└── emby.srs                # sing-box 输出
```

## 当前规则

| 规则 | Mihomo | sing-box |
|------|--------|----------|
| Emby | [emby.mrs](https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.mrs) | [emby.srs](https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.srs) |

## 快速使用

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
        "url": "https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.srs"
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

## 格式差异

| 规则类型 | Mihomo MRS | sing-box SRS |
|----------|------------|--------------|
| DOMAIN | ✅ | ✅ |
| DOMAIN-SUFFIX | ✅ | ✅ |
| DOMAIN-KEYWORD | ❌ | ✅ |
| DOMAIN-REGEX | ❌ | ✅ |
| IP-CIDR | ✅ | ✅ |
| 混合规则 | ❌ | ✅ |

## 文档

- [Mihomo 使用指南](docs/mihomo.md) - 完整的 Mihomo 配置说明
- [sing-box 使用指南](docs/singbox.md) - 完整的 sing-box 配置说明

## 添加规则

1. 编辑对应的源文件
   - Mihomo: `*/src/mihomo/*.yaml`
   - sing-box: `*/src/singbox/*.json`
2. 提交并推送
3. GitHub Actions 自动编译

## 查看编译状态

https://github.com/xqd922/rules/actions
