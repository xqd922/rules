# 规则仓库使用指南

## 快速开始

### 添加新域名到 Emby 规则

1. 编辑文件 `emby/src/emby-domain.yaml`
2. 按格式添加域名
3. 提交并推送
4. 等待 GitHub Actions 自动编译（约 1 分钟）

## YAML 文件格式

```yaml
payload:
  # 精确匹配域名（DOMAIN）
  - example.com
  - cdn.example.com

  # 后缀匹配（DOMAIN-SUFFIX）- 使用 +. 前缀
  - +.example.org      # 匹配 example.org 及其所有子域名
  - +.cdn.example.net  # 匹配 cdn.example.net 及其所有子域名
```

### 规则类型说明

| 写法 | 等效规则 | 匹配示例 |
|------|----------|----------|
| `example.com` | `DOMAIN,example.com` | 仅匹配 `example.com` |
| `+.example.com` | `DOMAIN-SUFFIX,example.com` | 匹配 `example.com`、`www.example.com`、`a.b.example.com` |

## 实际示例

假设你要添加一个新的 Emby 服务 `newemby.com`：

**编辑前：**
```yaml
payload:
  - cdn.lyrebirdemby.com
  - +.misty.cx
```

**编辑后：**
```yaml
payload:
  - cdn.lyrebirdemby.com
  - +.misty.cx
  - +.newemby.com      # 新增
```

## 创建新的规则集

### 示例：创建 AI 规则集

1. 创建目录结构：
   ```
   ai/
   └── src/
       └── ai-domain.yaml
   ```

2. 编写 YAML 文件 `ai/src/ai-domain.yaml`：
   ```yaml
   payload:
     - +.openai.com
     - +.anthropic.com
     - +.claude.ai
   ```

3. 推送后，自动生成 `ai/ai-domain.mrs`

4. 在 Clash 配置中使用：
   ```yaml
   rule-providers:
     ai:
       type: http
       behavior: domain
       format: mrs
       url: 'https://raw.githubusercontent.com/xqd922/rules/main/ai/ai-domain.mrs'
       path: './rule_providers/ai.mrs'
       interval: 86400

   rules:
     - RULE-SET,ai,AI代理组
   ```

## 文件命名规则

| 文件名 | 自动识别类型 | 用途 |
|--------|--------------|------|
| `xxx-domain.yaml` | domain | 域名规则 |
| `xxx.yaml` | domain | 域名规则（默认） |
| `xxx-ip.yaml` | ipcidr | IP 规则 |

## IP 规则格式（如需要）

```yaml
payload:
  - 1.2.3.4/32        # 单个 IP
  - 10.0.0.0/8        # IP 段
  - 192.168.0.0/16    # IP 段
```

## 常见问题

### Q: 推送后多久生效？
A: GitHub Actions 编译约需 1 分钟，Clash 客户端按 `interval` 设置更新（默认 86400 秒 = 24 小时）。可手动刷新规则提供者立即生效。

### Q: 如何查看 Actions 是否成功？
A: 访问 https://github.com/xqd922/rules/actions 查看运行状态。

### Q: DOMAIN-KEYWORD 怎么写？
A: `.mrs` 格式不支持 DOMAIN-KEYWORD，需要在 Clash 配置中单独写内联规则。

### Q: 格式写错了怎么办？
A: Actions 会编译失败，查看日志修正后重新推送即可。
