# 规则仓库使用指南

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

---

## Mihomo 规则

### 源文件格式 (YAML)

路径：`*/src/mihomo/*.yaml`

```yaml
payload:
  # 精确匹配域名（DOMAIN）
  - example.com

  # 后缀匹配（DOMAIN-SUFFIX）- 使用 +. 前缀
  - +.example.org
```

### 支持的规则类型

| 写法 | 类型 |
|------|------|
| `example.com` | DOMAIN |
| `+.example.com` | DOMAIN-SUFFIX |

### 配置示例

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

---

## sing-box 规则

### 源文件格式 (JSON)

路径：`*/src/singbox/*.json`

```json
{
  "version": 2,
  "rules": [
    {
      "domain": ["example.com"]
    },
    {
      "domain_suffix": ["example.org"]
    },
    {
      "domain_keyword": ["emby"]
    }
  ]
}
```

### 支持的规则类型

| 字段 | 类型 |
|------|------|
| `domain` | 精确匹配 |
| `domain_suffix` | 后缀匹配 |
| `domain_keyword` | 关键词匹配 |
| `ip_cidr` | IP 段匹配 |

### 配置示例

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

---

## 创建新规则集

例如创建 AI 规则集：

1. 创建目录结构：
   ```
   ai/
   └── src/
       ├── mihomo/
       │   └── ai.yaml
       └── singbox/
           └── ai.json
   ```

2. 推送后自动生成：
   - `ai/ai.mrs`
   - `ai/ai.srs`

---

## 文件命名规则

### Mihomo

| 文件名 | 类型 |
|--------|------|
| `xxx.yaml` | domain (默认) |
| `xxx-ip.yaml` | ipcidr |

### sing-box

所有 `.json` 文件直接编译，类型由 JSON 内容决定。

---

## 常见问题

### Q: 推送后多久生效？
A: GitHub Actions 编译约 1 分钟，客户端按 interval 更新。

### Q: 如何查看编译状态？
A: https://github.com/xqd922/rules/actions
