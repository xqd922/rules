# Rules

Clash/Mihomo 规则集合

## 使用方法

编辑 `*/src/*.yaml` 文件，推送后 GitHub Actions 会自动编译为 `.mrs` 格式。

## 目录结构

```
rules/
├── emby/
│   ├── emby-domain.mrs      # 自动生成
│   └── src/
│       └── emby-domain.yaml # 编辑这个
```

## Emby 规则

| 文件 | 类型 | 说明 |
|------|------|------|
| `emby/emby-domain.mrs` | domain | Emby 域名规则 |

### 配置示例

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

## 添加新规则

1. 创建目录：`新规则/src/`
2. 添加 YAML 文件（文件名含 `-ip` 会被识别为 ipcidr 类型）
3. 推送，自动编译
