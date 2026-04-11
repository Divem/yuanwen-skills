# feishu-doc-copier

飞书文档批量复制工具 - 双模式支持（lark-cli + 纯 Python API）

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 方式一：使用 lark-cli（推荐）
npm install -g @larksuite/cli
lark-cli auth login

# 方式二：使用 API（无需 lark-cli）
cp .env.example .env
# 编辑 .env 填入 App ID 和 Secret

# 复制文档
python scripts/copy_docs.py <source_token> <target_token>
```

## 详细文档

见 [README.md](README.md)

## 特性

- ✅ 双模式支持（CLI + API）
- ✅ 自动检测可用模式
- ✅ 保持文档格式完整
- ✅ 批量复制支持

## 许可证

MIT
