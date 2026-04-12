# cli-anything-open-autoglm 命令行参考手册

> **版本**: 0.1.0
> **许可**: MIT License
> **Python 要求**: >= 3.10

## 目录

- [概述](#概述)
- [安装](#安装)
- [全局选项](#全局选项)
- [命令速查表](#命令速查表)
- [设备管理 (`device`)](#设备管理-device)
  - [device list](#device-list)
  - [device connect](#device-connect)
  - [device disconnect](#device-disconnect)
  - [device tcpip](#device-tcpip)
- [任务执行 (`task`)](#任务执行-task)
  - [task run](#task-run)
  - [task history](#task-history)
  - [task clear-history](#task-clear-history)
- [脚本管理 (`script`)](#脚本管理-script)
  - [script list](#script-list)
  - [script info](#script-info)
  - [script export](#script-export)
  - [script delete](#script-delete)
- [配置管理 (`config`)](#配置管理-config)
  - [config show](#config-show)
  - [config set](#config-set)
  - [config del](#config-del)
  - [config apps](#config-apps)
  - [config test-model](#config-test-model)
- [交互模式 (`repl`)](#交互模式-repl)
  - [启动选项](#启动选项)
  - [REPL 内部命令](#repl-内部命令)
  - [REPL 使用示例](#repl-使用示例)
- [快速执行 (`exec`)](#快速执行-exec)
- [JSON 输出模式](#json-输出模式)
- [配置系统](#配置系统)
  - [配置优先级](#配置优先级)
  - [环境变量](#环境变量)
  - [配置存储](#配置存储)
- [退出码](#退出码)
- [常见错误与排查](#常见错误与排查)

---

## 概述

`cli-anything-open-autoglm` 是 [Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM) 的命令行工具，用于通过自然语言指令控制 Android 手机执行自动化操作。它基于 AutoGLM 视觉语言模型，能够理解屏幕内容并通过 ADB 执行 UI 操作。

主要功能：

- **设备管理** — 通过 ADB 管理已连接的 Android 设备（USB / WiFi）
- **任务执行** — 用自然语言描述任务，AI 自动操控手机完成
- **脚本录制** — 录制操作过程为可重放脚本（JSON / Python）
- **配置管理** — 灵活管理模型 API、设备、语言等参数
- **交互模式** — REPL 持续交互，无需反复输入命令前缀

---

## 安装

```bash
# 1. 克隆 Open-AutoGLM 项目
git clone https://github.com/zai-org/Open-AutoGLM.git
cd Open-AutoGLM

# 2. 安装 phone_agent 核心包
pip install -e .

# 3. 安装 CLI 工具
cd agent-harness
pip install -e .

# 4. 验证安装
cli-anything-open-autoglm --version
```

**系统要求**：

| 依赖 | 说明 |
|------|------|
| Python >= 3.10 | 运行环境 |
| ADB (Android Debug Bridge) | 设备通信，需加入 PATH |
| Android 7.0+ 设备 | 目标设备系统版本 |
| ADB Keyboard APK | 文本输入辅助（安装在设备上） |

**Python 依赖**：

| 包 | 版本 | 用途 |
|----|------|------|
| `click>=8.0` | CLI 框架 |
| `requests>=2.28` | HTTP 请求（模型 API 测试） |
| `phone_agent` | Open-AutoGLM 核心包（需单独安装） |

---

## 全局选项

以下选项可在任意命令中使用，需放在子命令之前：

```
cli-anything-open-autoglm [全局选项] <命令> [子命令] [参数] [选项]
```

| 选项 | 说明 |
|------|------|
| `--json` | 以 JSON 格式输出结果，适用于程序/Agent 解析 |
| `--version` | 显示版本号并退出 |

```bash
# 示例：全局启用 JSON 输出
cli-anything-open-autoglm --json device list

# 查看版本
cli-anything-open-autoglm --version
```

---

## 命令速查表

```
cli-anything-open-autoglm
├── device                          # 设备管理
│   ├── list                        # 列出已连接设备
│   ├── connect <host:port>         # 连接远程设备
│   ├── disconnect <address|all>    # 断开设备
│   └── tcpip [--port 5555]         # 开启 TCP/IP 调试
├── task                            # 任务管理
│   ├── run "任务描述" [OPTIONS]     # 执行自动化任务
│   ├── history [--limit N]         # 查看执行历史
│   └── clear-history               # 清空执行历史
├── script                          # 脚本管理
│   ├── list [--dir DIR] [--keyword KW]  # 列出已录制脚本
│   ├── info <path>                 # 查看脚本详情
│   ├── export <path> --format FMT  # 导出脚本
│   └── delete <path>               # 删除脚本
├── config                          # 配置管理
│   ├── show                        # 显示当前配置
│   ├── set <key> <value>           # 设置配置项
│   ├── del <key>                   # 删除配置项（恢复默认）
│   ├── apps                        # 列出支持的应用
│   └── test-model [--base-url URL] [--model NAME]  # 测试模型连通性
├── repl [OPTIONS]                  # 启动交互模式
└── exec "任务描述" [OPTIONS]        # 快捷执行（等同于 task run）
```

---

## 设备管理 (`device`)

通过 ADB（Android Debug Bridge）管理 Android 设备的连接与通信。

### `device list`

列出所有通过 ADB 连接的设备。

**语法**：

```bash
cli-anything-open-autoglm device list [--json]
```

**输出字段（JSON 模式）**：

```json
{
  "count": 1,
  "devices": [
    {
      "device_id": "emulator-5554",
      "connection_type": "usb",
      "model": "Pixel 6",
      "status": "connected"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `count` | int | 已连接设备数量 |
| `devices[].device_id` | string | ADB 设备标识符 |
| `devices[].connection_type` | string | 连接类型：`usb` 或 `wifi` |
| `devices[].model` | string/null | 设备型号（可检测时） |
| `devices[].status` | string | 设备状态 |

**示例**：

```bash
# 列出设备
cli-anything-open-autoglm device list

# JSON 格式输出（供程序解析）
cli-anything-open-autoglm device list --json
```

---

### `device connect`

通过 WiFi 连接远程 Android 设备。设备需先通过 USB 开启 TCP/IP 调试（参见 `device tcpip`）。

**语法**：

```bash
cli-anything-open-autoglm device connect <address> [--json]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `address` | 是 | 设备地址，格式为 `host:port`（如 `192.168.1.100:5555`） |

**输出字段（JSON 模式）**：

```json
{
  "address": "192.168.1.100:5555",
  "connected": true,
  "message": "connected to 192.168.1.100:5555"
}
```

**示例**：

```bash
# 连接局域网设备
cli-anything-open-autoglm device connect 192.168.1.100:5555

# 连接模拟器
cli-anything-open-autoglm device connect 127.0.0.1:5555
```

---

### `device disconnect`

断开远程设备连接。

**语法**：

```bash
cli-anything-open-autoglm device disconnect <address> [--json]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `address` | 是 | 设备地址（`host:port`）或 `all`（断开所有远程连接） |

**输出字段（JSON 模式）**：

```json
{
  "address": "all",
  "disconnected": true,
  "message": "all devices disconnected"
}
```

**示例**：

```bash
# 断开指定设备
cli-anything-open-autoglm device disconnect 192.168.1.100:5555

# 断开所有远程设备
cli-anything-open-autoglm device disconnect all
```

---

### `device tcpip`

在通过 USB 连接的设备上开启 TCP/IP 调试模式，使设备可以通过 WiFi 接受 ADB 连接。

**语法**：

```bash
cli-anything-open-autoglm device tcpip [--port PORT] [--json]
```

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--port` | `5555` | TCP/IP 监听端口 |

**输出字段（JSON 模式）**：

```json
{
  "tcpip_enabled": true,
  "port": 5555,
  "device_ip": "192.168.1.100",
  "message": "TCP/IP mode enabled on port 5555"
}
```

| 字段 | 说明 |
|------|------|
| `tcpip_enabled` | 是否成功开启 |
| `port` | 使用的端口 |
| `device_ip` | 设备 IP 地址（可检测时） |

**典型工作流**：

```bash
# 1. USB 连接设备后，开启 TCP/IP 模式
cli-anything-open-autoglm device tcpip --port 5555

# 2. 拔掉 USB 线，通过 WiFi 连接
cli-anything-open-autoglm device connect 192.168.1.100:5555

# 3. 验证连接
cli-anything-open-autoglm device list
```

---

## 任务执行 (`task`)

核心功能：用自然语言描述任务，AI 代理自动操控手机完成。

### `task run`

执行一个自动化任务。AI 代理会分析屏幕截图、理解任务意图、逐步执行 UI 操作。

**语法**：

```bash
cli-anything-open-autoglm task run <task_text> [OPTIONS] [--json]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `task_text` | 是 | 自然语言任务描述（如 "打开微信查看未读消息"） |

| 选项 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--device-id` | `-d` | 自动检测 | 指定 ADB 设备 ID |
| `--max-steps` | | `100` | 单个任务最大执行步数 |
| `--lang` | | `cn` | 语言：`cn`（中文）/ `en`（英文） |
| `--record` | | `false` | 录制操作为可重放脚本 |
| `--script-dir` | | `scripts` | 脚本输出目录 |
| `--quiet` | `-q` | `false` | 静默模式，抑制详细输出 |
| `--base-url` | | 配置值 | 覆盖模型 API 地址 |
| `--model` | | 配置值 | 覆盖模型名称 |
| `--api-key` | | 配置值 | 覆盖 API 密钥 |

**输出字段（JSON 模式）**：

```json
{
  "task": "打开微信查看未读消息",
  "reason": "completed",
  "step_count": 12,
  "message": "Task completed successfully",
  "duration_seconds": 45.3,
  "recorded": true,
  "script_summary": {
    "script_path": "scripts/open_wechat_20260408_120000.json",
    "total_steps": 12
  }
}
```

| 字段 | 说明 |
|------|------|
| `task` | 任务描述文本 |
| `reason` | 结束原因：`completed` / `max_steps_reached` / `stopped` / `error` |
| `step_count` | 实际执行步数 |
| `message` | 结果消息 |
| `duration_seconds` | 执行耗时（秒） |
| `recorded` | 是否录制了脚本 |
| `script_summary` | 脚本摘要（仅 `--record` 时存在） |

**任务执行流程**：

1. 截取手机屏幕截图
2. 将截图和任务描述发送给 AutoGLM 模型
3. 模型返回操作指令（点击、滑动、输入等）
4. 通过 ADB 执行操作
5. 重复步骤 1-4，直到任务完成或达到最大步数

**示例**：

```bash
# 基本任务执行
cli-anything-open-autoglm task run "打开微信查看未读消息"

# 指定设备
cli-anything-open-autoglm task run "打开设置" -d emulator-5554

# 限制最大步数
cli-anything-open-autoglm task run "搜索附近的餐厅" --max-steps 30

# 使用英文界面
cli-anything-open-autoglm task run "Open Chrome and search for weather" --lang en

# 录制脚本
cli-anything-open-autoglm task run "打开淘宝搜索手机壳" --record

# 录制脚本到指定目录
cli-anything-open-autoglm task run "打开抖音" --record --script-dir ./my_scripts

# 静默模式
cli-anything-open-autoglm task run "打开日历" --quiet

# 临时覆盖模型配置
cli-anything-open-autoglm task run "发消息" \
  --base-url https://open.bigmodel.cn/api/paas/v4 \
  --model autoglm-phone \
  --api-key "your-api-key"

# JSON 输出
cli-anything-open-autoglm task run "打开微信" --json
```

**终止任务**：按 `Ctrl+C` 可随时中断任务执行，结果中 `reason` 将为 `stopped`。

---

### `task history`

查看最近的任务执行历史记录。

**语法**：

```bash
cli-anything-open-autoglm task history [--limit N] [--json]
```

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--limit` | `20` | 返回的历史条目数量 |

**输出字段（JSON 模式）**：

```json
{
  "count": 3,
  "entries": [
    {
      "task": "打开微信查看未读消息",
      "reason": "completed",
      "step_count": 12,
      "model": "autoglm-phone",
      "device_id": "emulator-5554",
      "timestamp": "2026-04-08T12:00:00"
    }
  ]
}
```

| 字段 | 说明 |
|------|------|
| `task` | 任务描述 |
| `reason` | 结束原因 |
| `step_count` | 执行步数 |
| `model` | 使用的模型名称 |
| `device_id` | 设备 ID |
| `timestamp` | 执行时间（ISO 8601 格式） |

**注意**：历史记录自动保存，最多保留最近 100 条。

**示例**：

```bash
# 查看最近 10 条
cli-anything-open-autoglm task history --limit 10

# 查看全部历史
cli-anything-open-autoglm task history --limit 100
```

---

### `task clear-history`

清空所有任务执行历史。

**语法**：

```bash
cli-anything-open-autoglm task clear-history [--json]
```

**输出字段（JSON 模式）**：

```json
{
  "cleared": true
}
```

**示例**：

```bash
cli-anything-open-autoglm task clear-history
```

---

## 脚本管理 (`script`)

管理通过 `--record` 选项录制的自动化脚本。

### `script list`

列出已录制的脚本。

**语法**：

```bash
cli-anything-open-autoglm script list [--dir DIR] [--keyword KEYWORD] [--json]
```

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--dir` | `scripts` | 脚本目录路径 |
| `--keyword` | | 按任务名称关键词过滤 |

**输出字段（JSON 模式）**：

```json
{
  "count": 2,
  "scripts": [
    {
      "id": "open_wechat_20260408_120000",
      "name": "打开微信查看未读消息",
      "file": "scripts/open_wechat_20260408_120000.json",
      "replay_file": "scripts/open_wechat_20260408_120000_replay.py",
      "total_steps": 12,
      "success_rate": 1.0,
      "model_name": "autoglm-phone",
      "device_id": "emulator-5554",
      "created_at": "2026-04-08T12:00:00"
    }
  ]
}
```

| 字段 | 说明 |
|------|------|
| `id` | 脚本 ID（文件名去后缀） |
| `name` | 任务名称 |
| `file` | 脚本 JSON 文件路径 |
| `replay_file` | Python 回放脚本路径（存在时） |
| `total_steps` | 总操作步数 |
| `success_rate` | 成功率（0.0 - 1.0） |
| `model_name` | 录制时使用的模型 |
| `device_id` | 录制时的设备 ID |
| `created_at` | 创建时间 |

**示例**：

```bash
# 列出所有脚本
cli-anything-open-autoglm script list

# 从指定目录列出
cli-anything-open-autoglm script list --dir ./my_scripts

# 按关键词过滤
cli-anything-open-autoglm script list --keyword "微信"
```

---

### `script info`

查看脚本的详细信息，包括每一步的操作记录。

**语法**：

```bash
cli-anything-open-autoglm script info <script_path> [--json]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `script_path` | 是 | 脚本 JSON 文件路径 |

**输出字段（JSON 模式）**：

```json
{
  "metadata": {
    "task_name": "打开微信查看未读消息",
    "total_steps": 12,
    "model_name": "autoglm-phone",
    "device_id": "emulator-5554",
    "created_at": "2026-04-08T12:00:00"
  },
  "statistics": {
    "total_steps": 12,
    "success_steps": 11,
    "failed_steps": 1,
    "success_rate": 91.7
  },
  "steps": [
    {
      "step": 1,
      "action": "click",
      "success": true,
      "thinking": "点击微信图标..."
    }
  ]
}
```

**示例**：

```bash
cli-anything-open-autoglm script info scripts/open_wechat_20260408_120000.json
```

---

### `script export`

导出脚本为指定格式。

**语法**：

```bash
cli-anything-open-autoglm script export <script_path> --format FMT [--json]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `script_path` | 是 | 脚本 JSON 文件路径 |

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--format` | `json` | 导出格式：`json`（原始录制数据）/ `python`（Python 回放脚本） |

**示例**：

```bash
# 导出原始 JSON 数据
cli-anything-open-autoglm script export scripts/open_wechat.json --format json

# 导出 Python 回放脚本
cli-anything-open-autoglm script export scripts/open_wechat.json --format python
```

**注意**：非 JSON 模式下，内容将直接输出到标准输出。

---

### `script delete`

删除脚本及其关联的 Python 回放文件。

**语法**：

```bash
cli-anything-open-autoglm script delete <script_path> [--json]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `script_path` | 是 | 脚本 JSON 文件路径 |

**输出字段（JSON 模式）**：

```json
{
  "deleted": [
    "scripts/open_wechat.json",
    "scripts/open_wechat_replay.py"
  ]
}
```

**注意**：删除操作会同时移除 `*_replay.py` 文件（如果存在）。此操作不可逆。

**示例**：

```bash
cli-anything-open-autoglm script delete scripts/open_wechat.json
```

---

## 配置管理 (`config`)

管理 CLI 工具的运行配置。配置可持久化存储，跨会话生效。

### `config show`

显示当前生效的完整配置，包含模型配置、代理配置、环境变量和状态文件路径。

**语法**：

```bash
cli-anything-open-autoglm config show [--json]
```

**输出字段（JSON 模式）**：

```json
{
  "model": {
    "base_url": "http://localhost:8000/v1",
    "model": "autoglm-phone-9b",
    "api_key": "EMPTY"
  },
  "agent": {
    "device_id": "emulator-5554",
    "max_steps": 100,
    "lang": "cn"
  },
  "environment": {
    "supabase_url": "(not set)",
    "screenshot_auto_upload": "true",
    "step_tracking_enabled": "true"
  },
  "state_file": "/Users/<user>/.cli-anything/open-autoglm/config.json"
}
```

| 字段组 | 说明 |
|--------|------|
| `model` | 模型 API 配置（已解析最终值） |
| `agent` | 代理运行配置 |
| `environment` | 相关环境变量状态 |
| `state_file` | 配置文件存储路径 |

---

### `config set`

设置配置项的值。值会持久化到 `~/.cli-anything/open-autoglm/config.json`。

**语法**：

```bash
cli-anything-open-autoglm config set <key> <value> [--json]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `key` | 是 | 配置键名（见下方有效键列表） |
| `value` | 是 | 配置值 |

**有效配置键**：

| 键 | 类型 | 说明 |
|----|------|------|
| `base_url` | string | 模型 API 基础 URL |
| `model` | string | 模型名称 |
| `api_key` | string | API 认证密钥 |
| `device_id` | string | 默认 ADB 设备 ID |
| `max_steps` | int | 默认最大执行步数 |
| `lang` | string | 默认语言（`cn` / `en`） |
| `record_script` | bool | 是否默认录制脚本（`true`/`false`/`1`/`0`/`yes`/`no`/`on`/`off`） |
| `script_output_dir` | string | 脚本输出目录 |

**输出字段（JSON 模式）**：

```json
{
  "key": "base_url",
  "value": "https://open.bigmodel.cn/api/paas/v4"
}
```

**示例**：

```bash
# 设置模型 API
cli-anything-open-autoglm config set base_url https://open.bigmodel.cn/api/paas/v4
cli-anything-open-autoglm config set model autoglm-phone
cli-anything-open-autoglm config set api_key "your-api-key"

# 设置设备
cli-anything-open-autoglm config set device_id emulator-5554

# 设置默认最大步数
cli-anything-open-autoglm config set max_steps 50

# 设置默认语言
cli-anything-open-autoglm config set lang en

# 开启默认脚本录制
cli-anything-open-autoglm config set record_script true
```

---

### `config del`

删除配置项，使其恢复为环境变量或默认值。

**语法**：

```bash
cli-anything-open-autoglm config del <key> [--json]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `key` | 是 | 要删除的配置键名 |

**输出字段（JSON 模式）**：

```json
{
  "key": "api_key",
  "deleted": true
}
```

**示例**：

```bash
# 删除 API 密钥配置（恢复为环境变量或默认值）
cli-anything-open-autoglm config del api_key
```

---

### `config apps`

列出所有支持的 Android 应用程序。

**语法**：

```bash
cli-anything-open-autoglm config apps [--json]
```

**输出字段（JSON 模式）**：

```json
{
  "count": 50,
  "apps": {
    "微信": "com.tencent.mm",
    "淘宝": "com.taobao.taobao",
    "抖音": "com.ss.android.ugc.aweme",
    "支付宝": "com.eg.android.AlipayGphone",
    "Chrome": "com.android.chrome"
  }
}
```

---

### `config test-model`

测试模型 API 的连通性，验证配置是否正确。

**语法**：

```bash
cli-anything-open-autoglm config test-model [--base-url URL] [--model NAME] [--json]
```

| 选项 | 说明 |
|------|------|
| `--base-url` | 临时覆盖 API 地址（不持久化） |
| `--model` | 临时覆盖模型名称（不持久化） |

**输出字段（JSON 模式 — 成功时）**：

```json
{
  "reachable": true,
  "base_url": "https://open.bigmodel.cn/api/paas/v4",
  "models_available": ["autoglm-phone", "glm-4v-plus", ...],
  "configured_model": "autoglm-phone",
  "configured_model_found": true
}
```

**输出字段（JSON 模式 — 失败时）**：

```json
{
  "reachable": false,
  "base_url": "https://open.bigmodel.cn/api/paas/v4",
  "status_code": 401,
  "error": "Unauthorized"
}
```

| 字段 | 说明 |
|------|------|
| `reachable` | API 是否可达 |
| `models_available` | 可用模型 ID 列表 |
| `configured_model_found` | 配置的模型是否在可用列表中 |
| `status_code` | HTTP 状态码（失败时） |
| `error` | 错误信息（失败时） |

**常见错误信息**：

| 错误 | 原因 |
|------|------|
| `Connection refused - model service not running` | API 服务未启动 |
| `Unauthorized` (401) | API 密钥无效 |
| `Not Found` (404) | API 地址错误 |

**示例**：

```bash
# 使用已保存的配置测试
cli-anything-open-autoglm config test-model

# 临时测试其他 API 地址
cli-anything-open-autoglm config test-model --base-url http://localhost:8000/v1 --model autoglm-phone-9b
```

---

## 交互模式 (`repl`)

启动一个交互式 REPL（Read-Eval-Print Loop）会话，可连续执行任务而无需重复输入命令前缀。

### 启动选项

**语法**：

```bash
cli-anything-open-autoglm repl [OPTIONS]
```

| 选项 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--device-id` | `-d` | 自动检测 | 默认设备 ID |
| `--max-steps` | | `100` | 默认最大执行步数 |
| `--lang` | | `cn` | 默认语言：`cn` / `en` |
| `--record` | | `false` | 启用脚本录制 |

**启动示例**：

```bash
# 默认启动
cli-anything-open-autoglm repl

# 指定设备和录制
cli-anything-open-autoglm repl --device-id emulator-5554 --record

# 英文模式
cli-anything-open-autoglm repl --lang en
```

### REPL 内部命令

启动后会看到提示符 `autoglm>`，可以输入任务文本或斜杠命令。

| 命令 | 说明 |
|------|------|
| `<任务文本>` | 直接执行一个任务 |
| `/help` | 显示帮助信息 |
| `/reset` | 重置代理上下文（清空对话历史，但不影响配置） |
| `/config` | 显示当前配置 |
| `/config <key> <val>` | 设置配置值（同 `config set`） |
| `/devices` | 列出已连接设备 |
| `/apps` | 列出支持的应用 |
| `/history` | 查看任务执行历史 |
| `/model` | 测试当前模型连通性 |
| `/model <url> <name>` | 重新配置模型并测试连通性 |
| `/record on\|off` | 开启/关闭脚本录制 |
| `/record` | 查看当前录制状态 |
| `/quit` | 退出 REPL |
| `/exit` | 退出 REPL（同 `/quit`） |

**REPL 特性**：

- 代理实例在每次任务执行后自动重置
- 配置修改即时生效，无需重启 REPL
- `Ctrl+C` 可中断当前任务
- `Ctrl+D` 退出 REPL
- 输入空行会被忽略

### REPL 使用示例

```
$ cli-anything-open-autoglm repl --device-id emulator-5554
Open-AutoGLM Interactive REPL
Type a task to execute, or /help for commands.

autoglm> 打开微信查看未读消息
[任务执行中...]
Task completed successfully. Steps: 12, Duration: 45.3s

autoglm> /history
# 显示最近任务记录

autoglm> /record on
Script recording enabled.

autoglm> 打开淘宝搜索手机壳
[任务执行中，操作被录制...]

autoglm> /config max_steps 200
key: max_steps
value: 200

autoglm> /reset
Agent context reset.

autoglm> /quit
Goodbye!
```

---

## 快速执行 (`exec`)

`exec` 是 `task run` 的快捷方式，语法和参数完全相同。

**语法**：

```bash
cli-anything-open-autoglm exec <task_text> [OPTIONS]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `task_text` | 是 | 自然语言任务描述（未提供时显示用法提示） |

| 选项 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--device-id` | `-d` | 自动检测 | 指定 ADB 设备 ID |
| `--max-steps` | | `100` | 最大执行步数 |
| `--base-url` | | 配置值 | 覆盖模型 API 地址 |
| `--model` | | 配置值 | 覆盖模型名称 |
| `--api-key` | | 配置值 | 覆盖 API 密钥 |
| `--quiet` | `-q` | `false` | 静默模式 |
| `--record` | | `false` | 录制脚本 |
| `--lang` | | `cn` | 语言 |

**与 `task run` 的区别**：

- `exec` 是顶级命令，路径更短
- `task run` 支持额外的 `--script-dir` 选项
- 输出完全相同

**示例**：

```bash
# 快捷执行
cli-anything-open-autoglm exec "打开微信"

# 等同于
cli-anything-open-autoglm task run "打开微信"
```

---

## JSON 输出模式

所有命令均支持 `--json` 标志，将输出格式化为结构化 JSON，便于程序和 Agent 消费。

**使用方式**：

```bash
# 全局模式（影响所有子命令）
cli-anything-open-autoglm --json device list
cli-anything-open-autoglm --json task run "打开微信"

# 各命令均可独立使用
cli-anything-open-autoglm device list --json
cli-anything-open-autoglm config show --json
```

**JSON 输出特点**：

- 使用 `ensure_ascii=False`，正确显示中文和 Unicode 字符
- 缩进 2 空格，格式化输出
- 错误信息统一格式：`{"error": "错误描述"}`
- 成功信息格式：`{"success": true, "message": "描述"}`
- 表格数据自动转为对象数组

---

## 配置系统

### 配置优先级

配置值的解析遵循以下优先级（从高到低）：

```
CLI 命令行参数 > 持久化配置文件 > 环境变量 > 内置默认值
```

例如，设置模型名称时：

1. `--model autoglm-phone`（命令行参数）— 最高优先级
2. `config.json` 中的 `model` 字段
3. `PHONE_AGENT_MODEL` 环境变量
4. `autoglm-phone-9b`（内置默认值）

### 环境变量

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `PHONE_AGENT_BASE_URL` | `http://localhost:8000/v1` | 模型 API 基础 URL |
| `PHONE_AGENT_MODEL` | `autoglm-phone-9b` | 模型名称 |
| `PHONE_AGENT_API_KEY` | `EMPTY` | API 认证密钥 |
| `PHONE_AGENT_MAX_STEPS` | `100` | 默认最大执行步数 |
| `PHONE_AGENT_DEVICE_ID` | （自动检测） | 默认 ADB 设备 ID |
| `PHONE_AGENT_LANG` | `cn` | 默认语言 |
| `SUPABASE_URL` | （未设置） | Supabase URL（截图上传） |
| `SCREENSHOT_AUTO_UPLOAD` | `true` | 截图自动上传 |
| `STEP_TRACKING_ENABLED` | `true` | 步骤追踪启用 |

### 配置存储

配置文件路径：

```
~/.cli-anything/open-autoglm/config.json
```

历史记录文件路径：

```
~/.cli-anything/open-autoglm/history.json
```

**目录结构**：

```
~/.cli-anything/
└── open-autoglm/
    ├── config.json    # 持久化配置
    └── history.json   # 任务执行历史（最多 100 条）
```

**配置文件示例**：

```json
{
  "base_url": "https://open.bigmodel.cn/api/paas/v4",
  "model": "autoglm-phone",
  "api_key": "your-api-key-here",
  "device_id": "emulator-5554",
  "max_steps": 100,
  "lang": "cn",
  "record_script": false,
  "script_output_dir": "scripts"
}
```

---

## 退出码

| 退出码 | 说明 |
|--------|------|
| `0` | 命令成功执行 |
| `1` | 一般错误（参数缺失、命令未找到等） |
| `2` | `phone_agent` 包未安装 |

---

## 常见错误与排查

### `phone_agent package not found`

**原因**：未安装 `phone_agent` 核心包。

**解决**：

```bash
cd /path/to/Open-AutoGLM
pip install -e .
```

### `ADB not found`

**原因**：ADB 未安装或未加入 PATH。

**解决**：

```bash
# macOS
brew install android-platform-tools

# 或手动下载 Android SDK Platform-Tools
# 确保 adb 在 PATH 中
which adb
```

### `Connection refused - model service not running`

**原因**：模型 API 服务未启动或地址错误。

**解决**：

```bash
# 1. 检查配置
cli-anything-open-autoglm config show

# 2. 测试连通性
cli-anything-open-autoglm config test-model --json

# 3. 确认服务正在运行
curl http://localhost:8000/v1/models
```

### `Invalid config key: xxx`

**原因**：使用了不支持的配置键名。

**解决**：有效键名为：`base_url`, `model`, `api_key`, `device_id`, `max_steps`, `lang`, `record_script`, `script_output_dir`。

### `Script not found: xxx`

**原因**：指定的脚本文件不存在。

**解决**：

```bash
# 查看可用脚本
cli-anything-open-autoglm script list
```

### 任务执行中按 Ctrl+C 无响应

**原因**：某些 ADB 操作可能阻塞信号。

**解决**：再次按 `Ctrl+C`，或等待当前步骤完成后会自动检测中断。
