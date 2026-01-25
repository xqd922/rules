# sing-box 规则使用指南

## 概述

本仓库提供 sing-box 的 SRS 二进制规则文件。

相比 Mihomo，sing-box 的 SRS 格式支持更多规则类型，包括 **DOMAIN-KEYWORD**。

## 目录结构

```
emby/
├── src/
│   └── singbox/
│       └── emby.json       # 源文件
└── emby.srs                # 编译输出
```

## 当前可用规则

| 规则 | 类型 | 链接 |
|------|------|------|
| Emby | domain | [emby.srs](https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.srs) |

---

## 配置示例

### 基础配置

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

### 完整配置示例

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "emby",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.srs",
        "download_detour": "proxy",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": "emby",
        "outbound": "Emby"
      },
      {
        "protocol": "dns",
        "outbound": "dns-out"
      },
      {
        "ip_is_private": true,
        "outbound": "direct"
      }
    ],
    "final": "proxy"
  },
  "outbounds": [
    {
      "tag": "proxy",
      "type": "selector",
      "outbounds": ["hk", "sg", "direct"]
    },
    {
      "tag": "Emby",
      "type": "selector",
      "outbounds": ["direct", "hk", "sg"]
    },
    {
      "tag": "direct",
      "type": "direct"
    }
  ]
}
```

### 本地文件配置

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "emby",
        "type": "local",
        "format": "binary",
        "path": "./rules/emby.srs"
      }
    ]
  }
}
```

---

## 源文件格式

源文件位于 `*/src/singbox/*.json`

### JSON 格式

```json
{
  "version": 2,
  "rules": [
    {
      "domain": [
        "example.com",
        "cdn.example.com"
      ]
    },
    {
      "domain_suffix": [
        "example.org",
        "cdn.example.net"
      ]
    },
    {
      "domain_keyword": [
        "emby",
        "plex"
      ]
    },
    {
      "ip_cidr": [
        "1.2.3.0/24",
        "10.0.0.0/8"
      ]
    }
  ]
}
```

### 支持的规则类型

| 字段 | 类型 | 说明 |
|------|------|------|
| `domain` | DOMAIN | 精确匹配域名 |
| `domain_suffix` | DOMAIN-SUFFIX | 后缀匹配 |
| `domain_keyword` | DOMAIN-KEYWORD | 关键词匹配 |
| `domain_regex` | DOMAIN-REGEX | 正则匹配 |
| `ip_cidr` | IP-CIDR | IPv4 段匹配 |
| `ip_cidr` (IPv6) | IP-CIDR6 | IPv6 段匹配 |

### 完整规则示例

```json
{
  "version": 2,
  "rules": [
    {
      "domain": [
        "cdn.lyrebirdemby.com",
        "emby.my"
      ]
    },
    {
      "domain_suffix": [
        "misty.cx",
        "emby.tnx.one"
      ]
    },
    {
      "domain_keyword": [
        "emby",
        "embyvip"
      ]
    }
  ]
}
```

---

## 规则类型详解

### domain - 精确匹配

```json
{
  "domain": ["example.com", "www.example.com"]
}
```

只匹配 `example.com` 和 `www.example.com`，不匹配 `sub.example.com`。

### domain_suffix - 后缀匹配

```json
{
  "domain_suffix": ["example.com"]
}
```

匹配 `example.com`、`www.example.com`、`a.b.c.example.com`。

### domain_keyword - 关键词匹配

```json
{
  "domain_keyword": ["emby", "plex"]
}
```

匹配包含 `emby` 或 `plex` 的任意域名，如 `myemby.com`、`emby-server.net`。

### domain_regex - 正则匹配

```json
{
  "domain_regex": ["^ad\\.", "^tracking\\."]
}
```

使用正则表达式匹配域名。

### ip_cidr - IP 匹配

```json
{
  "ip_cidr": [
    "1.2.3.4/32",
    "10.0.0.0/8",
    "192.168.0.0/16"
  ]
}
```

匹配 IP 地址段。

---

## 文件命名规则

sing-box 的 JSON 源文件**不需要**通过文件名区分类型，因为规则类型由 JSON 内容决定。

| 文件名 | 说明 |
|--------|------|
| `emby.json` | 可包含任意规则类型 |
| `emby-ip.json` | 可包含任意规则类型 |

**推荐命名**：为了清晰，建议按内容命名：

| 文件名 | 内容 |
|--------|------|
| `emby.json` | 域名规则 (domain, domain_suffix, domain_keyword) |
| `emby-ip.json` | IP 规则 (ip_cidr) |
| `emby-all.json` | 混合规则 |

---

## IP 规则

### 目录结构

```
emby/
├── src/
│   └── singbox/
│       ├── emby.json       # 域名规则 -> emby.srs
│       └── emby-ip.json    # IP 规则  -> emby-ip.srs
├── emby.srs
└── emby-ip.srs
```

### 源文件格式

文件名：`emby-ip.json`

```json
{
  "version": 2,
  "rules": [
    {
      "ip_cidr": [
        "1.2.3.4/32",
        "10.0.0.0/8",
        "192.168.0.0/16",
        "172.16.0.0/12"
      ]
    }
  ]
}
```

### 配置示例

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "emby",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.srs"
      },
      {
        "tag": "emby-ip",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/xqd922/rules/main/emby/emby-ip.srs"
      }
    ],
    "rules": [
      {
        "rule_set": ["emby", "emby-ip"],
        "outbound": "Emby"
      }
    ]
  }
}
```

### 混合规则（推荐）

sing-box 支持在**同一个文件**中混合域名和 IP 规则：

文件名：`emby.json`

```json
{
  "version": 2,
  "rules": [
    {
      "domain": ["cdn.emby.com"]
    },
    {
      "domain_suffix": ["emby.media"]
    },
    {
      "domain_keyword": ["emby"]
    },
    {
      "ip_cidr": [
        "1.2.3.0/24",
        "10.0.0.0/8"
      ]
    }
  ]
}
```

配置只需一个 rule_set：

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

### 与 Mihomo 的区别

| 特性 | Mihomo MRS | sing-box SRS |
|------|------------|--------------|
| 混合 domain + ip | ❌ 需分开文件 | ✅ 可放同一文件 |
| 文件名决定类型 | ✅ `-ip` 为 ipcidr | ❌ 由 JSON 内容决定 |

---

## 添加/修改规则

### 添加新域名

1. 编辑 `emby/src/singbox/emby.json`
2. 按 JSON 格式添加域名
3. 提交并推送到 GitHub
4. 等待 GitHub Actions 自动编译 (约 1 分钟)

### 创建新规则集

1. 创建目录结构：
   ```
   ai/
   └── src/
       └── singbox/
           └── ai.json
   ```

2. 编写规则文件 `ai/src/singbox/ai.json`：
   ```json
   {
     "version": 2,
     "rules": [
       {
         "domain_suffix": [
           "openai.com",
           "anthropic.com",
           "claude.ai"
         ]
       },
       {
         "domain_keyword": [
           "chatgpt",
           "openai"
         ]
       }
     ]
   }
   ```

3. 推送后自动生成 `ai/ai.srs`

---

## rule_set 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `tag` | 规则集标签 | `"emby"` |
| `type` | 来源类型 | `"remote"` / `"local"` |
| `format` | 文件格式 | `"binary"` / `"source"` |
| `url` | 远程地址 | `"https://..."` |
| `path` | 本地路径 | `"./rules/emby.srs"` |
| `download_detour` | 下载使用的出站 | `"proxy"` |
| `update_interval` | 更新间隔 | `"24h"` |

### format 类型

| format | 说明 | 文件扩展名 |
|--------|------|------------|
| `binary` | 二进制格式 | `.srs` |
| `source` | JSON 源格式 | `.json` |

---

## 版本说明

sing-box rule-set 有多个版本：

| 版本 | sing-box 版本 | 说明 |
|------|---------------|------|
| 1 | 1.8.0+ | 初始版本 |
| 2 | 1.10.0+ | 优化 domain_suffix 内存占用 |

本仓库使用 **version 2**。

---

## 常见问题

### Q: 推送后多久生效？

GitHub Actions 编译约 1 分钟。客户端按 `update_interval` 设置更新。

### Q: 如何查看编译是否成功？

访问 https://github.com/xqd922/rules/actions

### Q: 如何手动编译 SRS？

```bash
sing-box rule-set compile input.json -o output.srs
```

### Q: JSON 格式错误怎么办？

Actions 会编译失败，查看日志修正 JSON 语法后重新推送。

常见错误：
- 缺少逗号
- 多余的逗号 (最后一个元素后不要加逗号)
- 引号不匹配

### Q: 如何验证 JSON 格式？

推送前可以用在线工具验证：https://jsonlint.com/

或使用命令行：
```bash
python -m json.tool emby.json
```

### Q: SRS 和 JSON 有什么区别？

| 格式 | 优点 | 缺点 |
|------|------|------|
| SRS (binary) | 体积小、加载快 | 不可直接阅读 |
| JSON (source) | 可读、可编辑 | 体积大、加载慢 |

推荐使用 SRS 格式。

---

## 与 Mihomo 的对比

| 特性 | Mihomo MRS | sing-box SRS |
|------|------------|--------------|
| DOMAIN | ✅ | ✅ |
| DOMAIN-SUFFIX | ✅ | ✅ |
| DOMAIN-KEYWORD | ❌ | ✅ |
| DOMAIN-REGEX | ❌ | ✅ |
| IP-CIDR | ✅ | ✅ |
| 混合规则 | ❌ | ✅ |

---

## 参考链接

- [sing-box 官方文档](https://sing-box.sagernet.org/)
- [Rule Set 配置](https://sing-box.sagernet.org/configuration/rule-set/)
- [Route Rule 配置](https://sing-box.sagernet.org/configuration/route/rule/)
- [Source Format 说明](https://sing-box.sagernet.org/configuration/rule-set/source-format/)
