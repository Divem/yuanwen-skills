---
name: feishu-sync
description: 双向手动同步本地目录与飞书云文档。支持 init（首次全量推送建立映射）、push（本地变更→飞书）、pull（飞书变更→本地）、status（查看差异）。适用于任意本地目录和飞书文件夹的组合。
---

# feishu-sync — 本地目录 ↔ 飞书云文档双向同步

## 使用方式

```
/feishu-sync init --dir <本地目录> --folder <飞书URL或token>
/feishu-sync push [--dir <本地目录>]
/feishu-sync pull [--dir <本地目录>]
/feishu-sync status [--dir <本地目录>]
```

## 前置条件

- `lark-cli` 已安装并完成认证（`lark-cli doctor` 全部 pass）
- 需要 `drive:drive` scope（`lark-cli auth check --scope drive:drive`）
- 若缺少 scope，执行：`lark-cli auth login --scope drive:drive` 完成授权
- `pull`/`status` 检测飞书新增文件需要 `search:docs:read` scope：
  `lark-cli auth login --scope search:docs:read`

## 工作原理

同步引擎位于 `scripts/sync.py`，通过调用 lark-cli 命令实现：

| 操作 | 本地 | 飞书 |
|------|------|------|
| .md 文件 | 原始 Markdown | 飞书文档（`docs +create`/`+fetch`/`+update`）|
| 其他文件 | 原始文件 | 云盘文件（`drive +upload`/`+download`）|

映射关系存储在 `.feishu-sync.json`（自动生成在 `--dir` 的父目录），应加入 `.gitignore`。

## 子命令说明

### init — 首次初始化

扫描本地目录 → 在飞书创建对应文件夹结构 → 上传所有文件 → 生成映射文件。

```bash
python ~/.claude/skills/feishu-sync/scripts/sync.py init --dir docs --folder https://xxx.feishu.cn/drive/folder/TOKEN
```

- `--dir` 默认 `docs`
- `--folder` 支持完整 URL 或纯 token
- 飞书侧建议为空文件夹（避免命名冲突）
- 完成后自动生成 `.feishu-sync.json`

### push — 推送本地变更

检测本地文件哈希变化 → 增量创建/更新飞书文档。

```bash
python ~/.claude/skills/feishu-sync/scripts/sync.py push --dir docs
```

- 新文件 → 创建飞书文档/上传
- 修改的文件 → 更新飞书文档内容（overwrite 模式）
- 新目录 → 自动创建飞书文件夹
- 本地已删除的文件 → 列出提示，不自动删除飞书侧

### pull — 拉取飞书变更

批量查询飞书元数据修改时间 → 拉取变更文件到本地，同时检测飞书新增文件。

```bash
python ~/.claude/skills/feishu-sync/scripts/sync.py pull --dir docs
```

- 通过 `drive metas batch_query` 批量检测（每批 200 个）
- .md 文件 → `docs +fetch` 拉取 Markdown 内容
- 二进制文件 → `drive +download` 下载
- 飞书新增文件 → 通过 `docs +search` 检测，自动拉取到本地

### status — 查看同步状态

三向对比本地和飞书差异。

```bash
python ~/.claude/skills/feishu-sync/scripts/sync.py status --dir docs
```

输出标记：
- `→` 本地改了，待 push
- `←` 飞书改了，待 pull
- `⟷` 双边都改了，冲突需人工处理
- `+` 本地新增文件
- `-` 本地已删除文件
- `↓` 飞书新增文件（执行 pull 可拉取到本地）

## 冲突处理

当 status 显示 `⟷` 时，表示本地和飞书都修改了同一文件：
1. 先 `pull` 保留飞书版本
2. 手动合并内容
3. 再 `push` 推送合并结果

## 注意事项

- `drive +upload` 要求文件路径为**相对于当前工作目录的路径**，不可用绝对路径
- 文件大小限制 20MB
- `.md` 文件走飞书文档（支持富文本编辑），其他文件走云盘文件上传
- Markdown 往返可能有格式损失（飞书 flavored Markdown ≠ 标准 Markdown）
- 飞书 `drive/v1/files` API 的 `folder_token` 参数不生效，新文件检测通过 `docs +search` + 时间戳过滤实现
- 新文件检测依赖 `search:docs:read` scope，未授权时 pull/status 只能检测已有映射文件的变更
