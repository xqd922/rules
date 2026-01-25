# Mihomo 规则使用指南

## 概述

本仓库提供 Mihomo (Clash.Meta) 的 MRS 二进制规则文件。

## 目录结构

```
emby/
├── src/
│   └── mihomo/
│       └── emby.yaml       # 源文件
└── emby.mrs                # 编译输出
```

## 当前可用规则

| 规则 | 类型 | 链接 |
|------|------|------|
| Emby | domain | [emby.mrs](https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.mrs) |

---

## 配置示例

### 基础配置

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
  - RULE-SET,emby,Emby代理组
```

### 完整配置示例

```yaml
# 规则提供者
rule-providers:
  emby:
    type: http
    behavior: domain
    format: mrs
    url: 'https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.mrs'
    path: './rule_providers/emby.mrs'
    interval: 86400

# 代理组
proxy-groups:
  - name: Emby
    type: select
    proxies:
      - DIRECT
      - 香港节点
      - 新加坡节点

# 规则
rules:
  # Emby 规则集
  - RULE-SET,emby,Emby

  # DOMAIN-KEYWORD 需要手动添加 (MRS 不支持)
  - DOMAIN-KEYWORD,emby,Emby
  - DOMAIN-KEYWORD,embyvip,Emby
  - DOMAIN-KEYWORD,pilipiliultra,Emby

  # 其他规则
  - MATCH,DIRECT
```

---

## 源文件格式

源文件位于 `*/src/mihomo/*.yaml`

### YAML 格式

```yaml
payload:
  # DOMAIN - 精确匹配
  - example.com
  - cdn.example.com

  # DOMAIN-SUFFIX - 后缀匹配 (使用 +. 前缀)
  - +.example.org
  - +.cdn.example.net
```

### 规则类型

| 写法 | 类型 | 说明 |
|------|------|------|
| `example.com` | DOMAIN | 精确匹配 `example.com` |
| `+.example.com` | DOMAIN-SUFFIX | 匹配 `example.com` 及所有子域名 |

### 不支持的规则类型

MRS 格式**不支持**以下规则类型，需要在配置文件中手动添加：

| 类型 | 说明 | 配置写法 |
|------|------|----------|
| DOMAIN-KEYWORD | 关键词匹配 | `- DOMAIN-KEYWORD,emby,代理组` |
| DOMAIN-REGEX | 正则匹配 | `- DOMAIN-REGEX,^ad\..+,REJECT` |

---

## 文件命名规则

| 文件名 | 编译类型 | behavior |
|--------|----------|----------|
| `emby.yaml` | domain | `behavior: domain` |
| `emby-ip.yaml` | ipcidr | `behavior: ipcidr` |

**判断逻辑**：文件名包含 `-ip` 则编译为 `ipcidr`，否则为 `domain`。

---

## IP 规则

### 目录结构

```
emby/
├── src/
│   └── mihomo/
│       ├── emby.yaml       # 域名规则 -> emby.mrs
│       └── emby-ip.yaml    # IP 规则  -> emby-ip.mrs
├── emby.mrs
└── emby-ip.mrs
```

### 源文件格式

文件名：`emby-ip.yaml`

```yaml
payload:
  - 1.2.3.4/32        # 单个 IP
  - 10.0.0.0/8        # IP 段
  - 192.168.0.0/16    # IP 段
  - 172.16.0.0/12     # IP 段
```

### 配置示例

```yaml
rule-providers:
  emby-domain:
    type: http
    behavior: domain
    format: mrs
    url: 'https://raw.githubusercontent.com/xqd922/rules/main/emby/emby.mrs'
    path: './rule_providers/emby.mrs'
    interval: 86400

  emby-ip:
    type: http
    behavior: ipcidr
    format: mrs
    url: 'https://raw.githubusercontent.com/xqd922/rules/main/emby/emby-ip.mrs'
    path: './rule_providers/emby-ip.mrs'
    interval: 86400

rules:
  - RULE-SET,emby-domain,Emby
  - RULE-SET,emby-ip,Emby
```

### 注意事项

- **behavior 必须匹配**：domain 规则用 `behavior: domain`，IP 规则用 `behavior: ipcidr`
- **不能混合**：一个 MRS 文件只能包含一种类型
- **分开配置**：需要两个 rule-providers 分别引用

---

## 添加/修改规则

### 添加新域名

1. 编辑 `emby/src/mihomo/emby.yaml`
2. 按格式添加域名
3. 提交并推送到 GitHub
4. 等待 GitHub Actions 自动编译 (约 1 分钟)

### 创建新规则集

1. 创建目录结构：
   ```
   ai/
   └── src/
       └── mihomo/
           └── ai.yaml
   ```

2. 编写规则文件 `ai/src/mihomo/ai.yaml`：
   ```yaml
   payload:
     - +.openai.com
     - +.anthropic.com
     - +.claude.ai
   ```

3. 推送后自动生成 `ai/ai.mrs`

---

## 规则参数说明

### rule-providers 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `type` | 规则来源类型 | `http` / `file` |
| `behavior` | 规则行为 | `domain` / `ipcidr` / `classical` |
| `format` | 文件格式 | `mrs` / `yaml` / `text` |
| `url` | 远程地址 | `https://...` |
| `path` | 本地缓存路径 | `./rule_providers/xxx.mrs` |
| `interval` | 更新间隔 (秒) | `86400` (24小时) |

### behavior 类型

| behavior | 说明 | MRS 支持 |
|----------|------|----------|
| `domain` | 域名规则 | ✅ |
| `ipcidr` | IP 规则 | ✅ |
| `classical` | 混合规则 | ❌ |

---

## 常见问题

### Q: 推送后多久生效？

GitHub Actions 编译约 1 分钟。客户端按 `interval` 设置更新 (默认 24 小时)。

手动刷新：在客户端中手动更新规则提供者即可立即生效。

### Q: 如何查看编译是否成功？

访问 https://github.com/xqd922/rules/actions

### Q: DOMAIN-KEYWORD 怎么用？

MRS 格式不支持 DOMAIN-KEYWORD，需要在配置文件中手动添加：

```yaml
rules:
  - DOMAIN-KEYWORD,emby,Emby
  - RULE-SET,emby,Emby  # 放在 KEYWORD 后面
```

### Q: 如何同时使用 domain 和 ipcidr 规则？

需要分开两个文件：

```yaml
rule-providers:
  emby-domain:
    behavior: domain
    format: mrs
    url: '.../emby.mrs'
  emby-ip:
    behavior: ipcidr
    format: mrs
    url: '.../emby-ip.mrs'

rules:
  - RULE-SET,emby-domain,Emby
  - RULE-SET,emby-ip,Emby
```

### Q: 格式写错了怎么办？

Actions 会编译失败，查看日志修正后重新推送即可。

---

## 参考链接

- [Mihomo 官方文档](https://wiki.metacubex.one/)
- [rule-providers 配置](https://wiki.metacubex.one/config/rule-providers/)
- [规则类型说明](https://wiki.metacubex.one/config/rules/)
