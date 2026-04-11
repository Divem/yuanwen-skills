# Pencil CLI 命令参考

> 版本：0.2.4 | 包：`@pencil.dev/cli`
> AI 驱动的设计文件操作工具，使用 `.pen` 格式，基于 Anthropic Claude 模型生成/修改设计。

---

## 认证命令

| 命令 | 说明 |
|------|------|
| `pencil login` | 交互式登录（邮箱 + 密码或 OTP） |
| `pencil status` | 查看认证状态 |
| `pencil version` | 显示 CLI 版本号 |
| `pencil interactive` | 启动交互式 Shell |

---

## 核心用法

### 1. 从零创建设计文件

通过 `--prompt` 描述需求，`--out` 指定输出路径，AI 从空白生成 `.pen` 设计文件：

```bash
pencil --out <output.pen> --prompt "Create a login page"
```

### 2. 基于现有文件修改

通过 `--in` 传入已有设计文件，结合 `--prompt` 描述修改需求：

```bash
pencil --in <input.pen> --out <output.pen> --prompt "Add a button"
```

---

## 全部参数

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `--in` | `-i` | 输入 `.pen` 文件路径 | - |
| `--out` | `-o` | 输出 `.pen` 文件路径（**必填**） | - |
| `--prompt` | `-p` | AI 代理的提示词（**必填**） | - |
| `--model` | `-m` | 使用的模型 ID | Claude Opus |
| `--custom` | `-c` | 使用自定义 Claude 模型配置 | 关闭 |
| `--list-models` | - | 列出所有可用模型 | - |
| `--tasks` | `-t` | 批量操作的 JSON 任务文件路径 | - |
| `--workspace` | `-w` | 工作区文件夹路径 | - |
| `--export` | `-e` | 导出最终结果的图片路径 | - |
| `--export-scale` | - | 导出缩放倍数 | 1 |
| `--export-type` | - | 导出格式：`png` / `jpeg` / `webp` / `pdf` | `png` |
| `--preview-output` | - | 预览 PNG 保存路径 | `~/.pencil/latest-preview.png` |
| `--enable-preview` | - | 每次设计变更后保存预览 | 关闭 |
| `--verbose-mcp` | - | 输出完整 MCP 工具错误详情 | 关闭 |

---

## 批量操作

通过 `--tasks` 传入 JSON 文件，可一次性执行多个设计任务：

```bash
pencil --tasks tasks.json --out output.pen
```

`tasks.json` 格式示例：

```json
[
  { "prompt": "Create a header with logo" },
  { "prompt": "Add a hero section" },
  { "prompt": "Add a footer with links" }
]
```

---

## 导出

设计完成后可直接导出为图片或 PDF：

```bash
# 导出 2x 高清 PNG
pencil --in design.pen --export output.png --export-scale 2

# 导出 PDF
pencil --in design.pen --export output.pdf --export-type pdf
```

---

## 模型选择

```bash
# 查看可用模型列表
pencil --list-models

# 指定模型
pencil --out result.pen --prompt "Design a card" --model <model-id>
```

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `PENCIL_CLI_KEY` | Pencil API 密钥 |
| `ANTHROPIC_API_KEY` | Anthropic Claude API 密钥 |
| `PENCIL_API_BASE` | 自定义 API 基础 URL |
| `DEBUG` | 开启调试模式 |

---

## 配置目录

Pencil 的本地数据存储在 `~/.pencil/`：

| 文件/目录 | 说明 |
|-----------|------|
| `session-cli.json` | CLI 登录凭证 |
| `session-desktop.json` | Desktop 应用凭证 |
| `apps/` | 应用数据 |
| `resources/` | 资源文件 |
| `latest-preview.png` | 最新预览图 |
