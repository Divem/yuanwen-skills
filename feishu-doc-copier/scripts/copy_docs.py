#!/usr/bin/env python3
"""
飞书文档复制工具 - 双模式版本
支持 lark-cli 模式和纯 API 模式，自动检测和切换
"""

import subprocess
import json
import os
import sys
from typing import List, Tuple, Optional, Dict
from pathlib import Path
import time

# 尝试导入可选依赖
try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from dotenv import load_dotenv

    HAS_DOTENV = True
    # 加载 .env 文件
    load_dotenv()
except ImportError:
    HAS_DOTENV = False


class FeishuDocCopier:
    """飞书文档复制器 - 支持 CLI 和 API 两种模式"""

    def __init__(self, app_id: Optional[str] = None, app_secret: Optional[str] = None):
        """
        初始化复制器

        Args:
            app_id: 飞书应用 ID（API 模式需要）
            app_secret: 飞书应用密钥（API 模式需要）
        """
        self.app_id = app_id or os.getenv("FEISHU_APP_ID")
        self.app_secret = app_secret or os.getenv("FEISHU_APP_SECRET")
        self.access_token = None
        self.token_expires_at = 0

        # 检测可用模式
        self.has_cli = self._check_cli()
        self.has_api = self._check_api()

        if not self.has_cli and not self.has_api:
            raise RuntimeError(
                "无法使用任何复制模式。请安装 lark-cli 或配置飞书应用凭证:\n"
                "  方式1: npm install -g @larksuite/cli\n"
                "  方式2: 设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET"
            )

    def _check_cli(self) -> bool:
        """检查是否安装了 lark-cli"""
        try:
            result = subprocess.run(
                ["lark-cli", "--version"], capture_output=True, timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _check_api(self) -> bool:
        """检查是否可以使用 API 模式"""
        if not HAS_REQUESTS:
            return False
        return bool(self.app_id and self.app_secret)

    def _get_access_token(self) -> str:
        """获取飞书访问令牌（API 模式）"""
        # 检查缓存的 token 是否有效
        if self.access_token and time.time() < self.token_expires_at - 300:
            return self.access_token

        if not HAS_REQUESTS:
            raise RuntimeError("未安装 requests 库，无法使用 API 模式")

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        resp = requests.post(
            url, json={"app_id": self.app_id, "app_secret": self.app_secret}
        )

        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取 token 失败: {data.get('msg')}")

        self.access_token = data["tenant_access_token"]
        # token 有效期 2 小时，我们缓存 1.5 小时
        self.token_expires_at = time.time() + data.get("expire", 7200)
        return self.access_token

    def _api_fetch_doc(self, doc_token: str) -> str:
        """使用 API 获取文档内容"""
        token = self._get_access_token()
        headers = {"Authorization": f"Bearer {token}"}

        # 获取文档 blocks
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks"
        resp = requests.get(url, headers=headers)
        data = resp.json()

        if data.get("code") != 0:
            raise RuntimeError(f"获取文档失败: {data.get('msg')}")

        # 这里简化处理，实际应该解析 blocks 转换为 markdown
        # 飞书的 API 返回的是结构化数据，需要转换
        # 暂时返回提示让用户使用 CLI 模式获取更好格式
        return self._blocks_to_markdown(data.get("data", {}).get("items", []))

    def _blocks_to_markdown(self, blocks: List[Dict]) -> str:
        """将飞书 blocks 转换为 Markdown（简化版）"""
        lines = []
        for block in blocks:
            block_type = block.get("block_type")

            if block_type == 1:  # page
                # 获取标题
                if "page" in block and "elements" in block["page"]:
                    for elem in block["page"]["elements"]:
                        if "text_run" in elem:
                            lines.append(f"# {elem['text_run']['content']}")
                            lines.append("")

            elif block_type == 2:  # text
                if "text" in block and "elements" in block["text"]:
                    texts = []
                    for elem in block["text"]["elements"]:
                        if "text_run" in elem:
                            texts.append(elem["text_run"]["content"])
                    if texts:
                        lines.append("".join(texts))
                        lines.append("")

            elif block_type == 3:  # heading1
                text = self._extract_text_from_block(block, "heading1")
                if text:
                    lines.append(f"# {text}")
                    lines.append("")

            elif block_type == 4:  # heading2
                text = self._extract_text_from_block(block, "heading2")
                if text:
                    lines.append(f"## {text}")
                    lines.append("")

            elif block_type == 5:  # heading3
                text = self._extract_text_from_block(block, "heading3")
                if text:
                    lines.append(f"### {text}")
                    lines.append("")

            elif block_type == 12:  # bullet
                text = self._extract_text_from_block(block, "bullet")
                if text:
                    lines.append(f"- {text}")

            elif block_type == 13:  # ordered
                text = self._extract_text_from_block(block, "ordered")
                if text:
                    lines.append(f"1. {text}")

            elif block_type == 14:  # code
                text = self._extract_text_from_block(block, "code")
                if text:
                    lines.append("```")
                    lines.append(text)
                    lines.append("```")
                    lines.append("")

            elif block_type == 18:  # divider
                lines.append("---")
                lines.append("")

        return "\n".join(lines)

    def _extract_text_from_block(self, block: Dict, key: str) -> str:
        """从 block 中提取文本"""
        if key not in block:
            return ""

        elements = block[key].get("elements", [])
        texts = []
        for elem in elements:
            if "text_run" in elem:
                texts.append(elem["text_run"]["content"])

        return "".join(texts)

    def _api_create_doc(self, title: str, folder_token: Optional[str] = None) -> str:
        """使用 API 创建文档"""
        token = self._get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        url = "https://open.feishu.cn/open-apis/docx/v1/documents"
        data = {"title": title}
        if folder_token:
            data["folder_token"] = folder_token

        resp = requests.post(url, headers=headers, json=data)
        result = resp.json()

        if result.get("code") != 0:
            raise RuntimeError(f"创建文档失败: {result.get('msg')}")

        return result["data"]["document"]["document_id"]

    def _api_update_doc(self, doc_token: str, content: str) -> bool:
        """使用 API 更新文档内容（通过 blocks 批量创建）"""
        token = self._get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # 注意：飞书 API 不支持直接写入 markdown
        # 需要将 markdown 转换为 blocks 然后批量创建
        # 这是一个简化实现，仅支持基本文本

        # 获取文档的 page block id
        url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks"
        resp = requests.get(url, headers=headers)
        data = resp.json()

        if data.get("code") != 0:
            return False

        items = data.get("data", {}).get("items", [])
        if not items:
            return False

        page_block_id = items[0].get("block_id")

        # 解析 markdown 并创建 blocks（简化版）
        lines = content.split("\n")
        children = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            child = None

            if line.startswith("### "):
                child = {
                    "block_type": 5,
                    "heading3": {"elements": [{"text_run": {"content": line[4:]}}]},
                }
            elif line.startswith("## "):
                child = {
                    "block_type": 4,
                    "heading2": {"elements": [{"text_run": {"content": line[3:]}}]},
                }
            elif line.startswith("# "):
                child = {
                    "block_type": 3,
                    "heading1": {"elements": [{"text_run": {"content": line[2:]}}]},
                }
            elif line.startswith("- "):
                child = {
                    "block_type": 12,
                    "bullet": {"elements": [{"text_run": {"content": line[2:]}}]},
                }
            elif line.startswith("1. "):
                child = {
                    "block_type": 13,
                    "ordered": {"elements": [{"text_run": {"content": line[3:]}}]},
                }
            else:
                child = {
                    "block_type": 2,
                    "text": {"elements": [{"text_run": {"content": line}}]},
                }

            if child:
                children.append(child)

        # 批量创建 blocks（每次最多 500 个）
        batch_size = 100
        for i in range(0, len(children), batch_size):
            batch = children[i : i + batch_size]
            url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{page_block_id}/children"
            resp = requests.post(url, headers=headers, json={"children": batch})

            if resp.json().get("code") != 0:
                return False

        return True

    def _cli_fetch_doc(self, doc_token: str) -> str:
        """使用 lark-cli 获取文档内容"""
        result = subprocess.run(
            ["lark-cli", "docs", "+fetch", "--doc", doc_token, "--format", "json"],
            capture_output=True,
            text=True,
        )

        try:
            data = json.loads(result.stdout)
            if data.get("ok") and data.get("data"):
                return data["data"].get("markdown", "")
        except:
            pass

        return ""

    def _cli_update_doc(self, doc_token: str, content: str) -> bool:
        """使用 lark-cli 更新文档"""
        result = subprocess.run(
            [
                "lark-cli",
                "docs",
                "+update",
                "--doc",
                doc_token,
                "--mode",
                "overwrite",
                "--markdown",
                content,
            ],
            capture_output=True,
            text=True,
        )

        try:
            data = json.loads(result.stdout)
            return data.get("ok", False)
        except:
            return False

    def fetch_doc(self, doc_token: str) -> str:
        """
        获取文档内容，自动选择可用模式

        优先级：lark-cli > API
        """
        if self.has_cli:
            return self._cli_fetch_doc(doc_token)
        elif self.has_api:
            return self._api_fetch_doc(doc_token)
        else:
            raise RuntimeError("没有可用的复制模式")

    def update_doc(self, doc_token: str, content: str) -> bool:
        """
        更新文档内容，自动选择可用模式

        优先级：lark-cli > API
        """
        if self.has_cli:
            return self._cli_update_doc(doc_token, content)
        elif self.has_api:
            return self._api_update_doc(doc_token, content)
        else:
            raise RuntimeError("没有可用的复制模式")

    def copy_document(self, source_token: str, target_token: str) -> Tuple[bool, str]:
        """
        复制单个文档

        Returns:
            (成功标志, 消息)
        """
        try:
            content = self.fetch_doc(source_token)
            if not content:
                return False, "获取源文档失败或内容为空"

            if self.update_doc(target_token, content):
                return True, f"复制成功 ({len(content)} 字符)"
            else:
                return False, "更新目标文档失败"

        except Exception as e:
            return False, f"复制出错: {str(e)}"

    def batch_copy(
        self, doc_mappings: List[Tuple[str, str, str]], verbose: bool = True
    ) -> Dict:
        """
        批量复制文档

        Args:
            doc_mappings: [(source_token, target_token, name), ...]
            verbose: 是否打印详细信息

        Returns:
            {
                "total": int,
                "success": int,
                "failed": int,
                "results": [...]
            }
        """
        total = len(doc_mappings)
        success = 0
        failed = 0
        results = []

        # 显示当前模式
        mode = "lark-cli" if self.has_cli else "API"

        if verbose:
            print("=" * 70)
            print(f"飞书文档批量复制 (使用 {mode} 模式)")
            print("=" * 70)
            print()

        for i, (source, target, name) in enumerate(doc_mappings, 1):
            if verbose:
                print(f"[{i}/{total}] {name}")

            ok, msg = self.copy_document(source, target)

            if ok:
                success += 1
                status = "✅"
            else:
                failed += 1
                status = "❌"

            results.append(
                {
                    "name": name,
                    "source": source,
                    "target": target,
                    "success": ok,
                    "message": msg,
                }
            )

            if verbose:
                print(f"  {status} {msg}")

        if verbose:
            print()
            print("=" * 70)
            print(f"完成！成功: {success}/{total}, 失败: {failed}/{total}")
            print("=" * 70)

        return {
            "total": total,
            "success": success,
            "failed": failed,
            "results": results,
        }


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="飞书文档批量复制工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 复制单个文档
  python copy_docs.py <source_token> <target_token>
  
  # 批量复制（从配置文件）
  python copy_docs.py --config config.json
  
  # 使用 API 模式（指定凭证）
  python copy_docs.py --app-id xxx --app-secret xxx <source> <target>
        """,
    )

    parser.add_argument("source", nargs="?", help="源文档 token")
    parser.add_argument("target", nargs="?", help="目标文档 token")
    parser.add_argument("--config", "-c", help="配置文件路径")
    parser.add_argument("--app-id", help="飞书应用 ID")
    parser.add_argument("--app-secret", help="飞书应用密钥")

    args = parser.parse_args()

    # 初始化复制器
    try:
        copier = FeishuDocCopier(app_id=args.app_id, app_secret=args.app_secret)
    except RuntimeError as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)

    # 批量模式
    if args.config:
        with open(args.config) as f:
            config = json.load(f)

        doc_mappings = [
            (doc["source"], doc["target"], doc["name"])
            for doc in config.get("documents", [])
        ]

        copier.batch_copy(doc_mappings)

    # 单文档模式
    elif args.source and args.target:
        ok, msg = copier.copy_document(args.source, args.target)
        print(f"{'✅' if ok else '❌'} {msg}")
        sys.exit(0 if ok else 1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
