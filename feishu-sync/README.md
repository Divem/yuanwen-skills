# feishu-sync

本地目录与飞书云文档的双向手动同步工具。

支持四种操作：`init`（首次全量推送建立映射）、`push`（本地→飞书）、`pull`（飞书→本地）、`status`（查看差异）。

## 功能特性

- **双向同步**：本地文件 ↔ 飞书文档/云盘文件
- **增量更新**：基于文件哈希检测变更，仅同步有差异的文件
- **Markdown 优化**：`.md` 文件转为飞书文档（支持富文本编辑），其他文件走云盘上传
- **差异对比**：`status` 命令展示本地与飞书的双向差异
- **新文件检测**：`pull`/`status` 可检测飞书侧新增的文档
- **冲突提示**：检测双向修改，引导人工合并

## 前置条件

1. 安装并认证 [lark-cli](https://github.com/nicepkg/lark-cli)
2. 确保以下 scope 已授权：
   - `drive:drive`：文件读写
   - `search:docs:read`：检测飞书新增文档（`pull`/`status` 需要）

```bash
lark-cli auth login --scope drive:drive
lark-cli auth login --scope search:docs:read
```

## 使用方式

```bash
/feishu-sync init --dir <本地目录> --folder <飞书URL或token>
/feishu-sync push [--dir <本地目录>]
/feishu-sync pull [--dir <本地目录>]
/feishu-sync status [--dir <本地目录>]
```

也可以直接调用脚本：

```bash
python ~/.claude/skills/feishu-sync/scripts/sync.py <子命令> [选项]
```

## 常用流程

1. **首次同步**：`init` 扫描本地目录，在飞书创建对应结构并上传所有文件
2. **日常推送**：本地修改后执行 `push`，增量更新到飞书
3. **日常拉取**：飞书修改后执行 `pull`，拉取到本地（含飞书新增文件）
4. **查看差异**：`status` 查看当前同步状态

## 注意事项

- 映射关系存储在 `.feishu-sync.json`，建议加入 `.gitignore`
- 飞书侧建议使用空文件夹初始化，避免命名冲突
- Markdown 往返可能有格式损失
- 文件大小限制 20MB
- 飞书 drive/v1/files API 的 `folder_token` 参数不生效，新文件检测通过 `docs +search` + 时间戳过滤实现

---

[English Version](README.en.md)
