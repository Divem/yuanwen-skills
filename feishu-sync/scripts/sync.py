#!/usr/bin/env python3
"""
feishu-sync: 本地目录 ↔ 飞书云文档 双向手动同步引擎

用法:
    python sync.py init --dir docs --folder <url|token>
    python sync.py push [--dir docs]
    python sync.py pull [--dir docs]
    python sync.py status [--dir docs]
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone


# --- 工具函数 ---

def sha256_file(filepath):
    """计算文件 sha256 哈希"""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_str(text):
    """计算字符串 sha256 哈希"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_folder_token(input_str):
    """从飞书 URL 或纯 token 中提取 folder token"""
    m = re.search(r'/drive/folder/([a-zA-Z0-9]+)', input_str)
    if m:
        return m.group(1)
    if re.match(r'^[a-zA-Z0-9]{10,}$', input_str):
        return input_str
    raise ValueError(f"无法从输入中提取 folder token: {input_str}")


def run_lark(args, capture=True, check=False):
    """执行 lark-cli 命令"""
    cmd = ["lark-cli"] + args
    if capture:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        if check and proc.returncode != 0:
            raise RuntimeError(f"lark-cli failed: {cmd}\n{output}")
        return output
    else:
        subprocess.run(cmd)


def run_lark_json(args):
    """执行 lark-cli 命令并解析 JSON 返回"""
    output = run_lark(args, capture=True)
    # lark-cli 可能混合了非 JSON 行（如 "Uploading: xxx"），找 JSON 块
    # 策略：找第一个 { 到最后一个 } 之间的内容
    start = output.find("{")
    end = output.rfind("}")
    if start != -1 and end != -1 and end > start:
        json_str = output[start:end + 1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    # fallback: 逐行尝试
    best = None
    for line in output.split("\n"):
        line = line.strip()
        if line.startswith("{"):
            try:
                obj = json.loads(line)
                if obj.get("ok"):
                    return obj
                if best is None:
                    best = obj
            except json.JSONDecodeError:
                continue
    if best is not None:
        return best
    raise RuntimeError(f"无法解析 lark-cli JSON 输出: {output[:500]}")


def create_folder(name, parent_token):
    """在飞书创建文件夹"""
    result = run_lark_json([
        "api", "POST", "/open-apis/drive/v1/files/create_folder",
        "--data", json.dumps({"name": name, "folder_token": parent_token}),
    ])
    if result.get("code") == 0:
        return result["data"]["token"]
    raise RuntimeError(f"创建文件夹失败: {name} -> {result}")


def create_doc(title, markdown, folder_token):
    """创建飞书文档，返回 token"""
    result = run_lark_json([
        "docs", "+create",
        "--title", title,
        "--markdown", markdown,
        "--folder-token", folder_token,
    ])
    if result.get("ok"):
        data = result.get("data", {})
        if isinstance(data, dict):
            # 优先 doc_id，fallback token
            for key in ("doc_id", "token"):
                if key in data:
                    return data[key]
        # 尝试从整个输出中提取
        output = json.dumps(result)
        for pattern in [r'"doc_id"\s*:\s*"([a-zA-Z0-9]+)"', r'"token"\s*:\s*"([a-zA-Z0-9]+)"']:
            m = re.search(pattern, output)
            if m:
                return m.group(1)
    raise RuntimeError(f"创建文档失败: {title} -> {result}")


def update_doc(token, markdown):
    """更新飞书文档内容"""
    result = run_lark_json([
        "docs", "+update",
        "--doc", token,
        "--markdown", markdown,
        "--mode", "overwrite",
    ])
    return result.get("ok", False)


def fetch_doc(token):
    """拉取飞书文档内容（Markdown）"""
    result = run_lark_json([
        "docs", "+fetch",
        "--doc", token,
    ])
    # 返回的数据中 content 字段包含 markdown
    if isinstance(result, dict):
        data = result.get("data", result)
        if isinstance(data, dict):
            return data.get("content", data.get("markdown", json.dumps(data)))
        if isinstance(data, str):
            return data
    return str(result)


def upload_file(rel_path, folder_token):
    """上传文件到飞书（必须用相对路径）"""
    result = run_lark_json([
        "drive", "+upload",
        "--file", rel_path,
        "--folder-token", folder_token,
    ])
    if result.get("ok"):
        data = result.get("data", {})
        if isinstance(data, dict):
            for key in ("file_token", "token"):
                if key in data:
                    return data[key]
        output = json.dumps(result)
        for pattern in [r'"file_token"\s*:\s*"([a-zA-Z0-9]+)"', r'"token"\s*:\s*"([a-zA-Z0-9]+)"']:
            m = re.search(pattern, output)
            if m:
                return m.group(1)
    raise RuntimeError(f"上传文件失败: {rel_path} -> {result}")


def download_file(file_token, output_path):
    """从飞书下载文件"""
    run_lark([
        "drive", "+download",
        "--file-token", file_token,
        "--output", output_path,
        "--overwrite",
    ], capture=False)


def list_folder_files(folder_token, max_count=200, since=0):
    """列出飞书文件夹内新增的文件/文档

    通过 search API 搜索最近创建的文档，按 create_time 过滤。
    由于飞书 drive/v1/files API 的 folder_token 参数不生效，
    这里用时间过滤来缩小范围。

    Args:
        folder_token: 飞书文件夹 token（用于 identify，搜索本身不按文件夹过滤）
        max_count: 单次最大请求数
        since: Unix 时间戳，只返回此时间之后创建的文件

    Returns:
        list: [{token, type, name, create_time, ...}, ...]
    """
    all_items = []
    page_token = None
    page_size = 20

    while len(all_items) < max_count:
        args = [
            "docs", "+search",
            "--query", "",
            "--page-size", str(page_size),
        ]
        if page_token:
            args.extend(["--page-token", page_token])

        result = run_lark_json(args)

        data = result.get("data", result) if isinstance(result, dict) else result
        results = data.get("results", []) if isinstance(data, dict) else []

        if not results:
            break

        for r in results:
            meta = r.get("result_meta", {})
            create_time = int(meta.get("create_time", 0))
            # 只取 since 之后创建的文件
            if since > 0 and create_time <= since:
                break

            doc_types = meta.get("doc_types", "file").lower()
            # 映射 doc_types 到我们的 type
            if doc_types == "docx" or doc_types == "doc":
                file_type = "docx"
            else:
                file_type = "file"

            all_items.append({
                "token": meta.get("token", ""),
                "type": file_type,
                "name": r.get("title_highlighted", ""),
                "create_time": create_time,
            })

        page_token = data.get("page_token") if isinstance(data, dict) else None
        has_more = data.get("has_more", False) if isinstance(data, dict) else False
        if not has_more or not page_token:
            break
        time.sleep(0.3)

    return all_items


def list_all_folder_files_recursive(state):
    """递归列出飞书侧所有文件夹中的文件

    Args:
        state: 同步状态

    Returns:
        list: [{token, type, name, folder_token, ...}, ...]
    """
    all_items = []
    # 获取 init 时间（取所有文件中最小的 feishu_modified）
    init_time = min(
        (entry.get("feishu_modified", 0) for entry in state["files"].values()),
        default=0
    )
    # 根文件夹
    folders_to_scan = [(state["folder_token"], "")]
    # 子文件夹
    for rel_dir, folder_token in state.get("folder_map", {}).items():
        folders_to_scan.append((folder_token, rel_dir))

    for folder_token, rel_dir in folders_to_scan:
        items = list_folder_files(folder_token, since=init_time)
        for item in items:
            item["_rel_dir"] = rel_dir
        all_items.extend(items)

    return all_items


def batch_query_metas(token_type_pairs):
    """批量查询飞书文件元数据，每批最多 200 个

    Args:
        token_type_pairs: [(token, type), ...]  type: "docx" 或 "file"

    Returns:
        dict: {token: {title, latest_modify_time, ...}}
    """
    results = {}
    batch_size = 200
    for i in range(0, len(token_type_pairs), batch_size):
        batch = token_type_pairs[i:i + batch_size]
        request_docs = [
            {"doc_token": tok, "doc_type": typ}
            for tok, typ in batch
        ]
        result = run_lark_json([
            "drive", "metas", "batch_query",
            "--data", json.dumps({"request_docs": request_docs, "with_url": False}),
        ])
        code = result.get("code")
        # 兼容两种返回格式：顶层 code 或嵌套在 data 中
        data = result.get("data", result)
        metas = data.get("metas", []) if isinstance(data, dict) else []
        if code == 0 or code is None:
            for meta in metas:
                results[meta["doc_token"]] = meta
        else:
            print(f"  ⚠ 批量查询失败: {result}", file=sys.stderr)
        if i + batch_size < len(token_type_pairs):
            time.sleep(0.3)
    return results


# --- 状态文件操作 ---

def find_state_file(local_base):
    """查找状态文件路径"""
    # 在 local_base 的父目录查找
    parent = os.path.dirname(os.path.abspath(local_base))
    return os.path.join(parent, ".feishu-sync.json")


def load_state(state_path):
    """加载状态文件"""
    if not os.path.exists(state_path):
        raise FileNotFoundError(f"状态文件不存在: {state_path}\n请先运行 init 命令")
    with open(state_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state_path, state):
    """保存状态文件"""
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_folder_token_for_path(rel_path, state):
    """根据相对路径获取飞书 folder token"""
    rel_dir = os.path.dirname(rel_path)
    if not rel_dir:
        return state["folder_token"]
    return state["folder_map"].get(rel_dir, state["folder_token"])


# --- 目录扫描 ---

def scan_local(local_base):
    """扫描本地目录，返回所有文件列表和目录结构

    Returns:
        files: [(rel_path, abs_path), ...]
        dirs: set of relative directory paths (not including base itself)
    """
    files = []
    dirs = set()
    for root, dirnames, filenames in os.walk(local_base):
        dirnames.sort()
        for fn in filenames:
            abs_path = os.path.join(root, fn)
            rel_path = os.path.relpath(abs_path, local_base)
            files.append((rel_path, abs_path))
            # 记录所有层级目录
            rel_dir = os.path.relpath(root, local_base)
            if rel_dir != ".":
                dirs.add(rel_dir)
    return sorted(files), sorted(dirs)


def get_dir_hierarchy(dirs):
    """将目录列表转为按层级排序的创建顺序（父目录优先）"""
    return sorted(dirs, key=lambda d: (d.count("/"), d))


# --- 核心命令 ---

def cmd_init(args):
    """初始化同步：创建飞书文件夹结构 + 上传所有文件"""
    local_base = args.dir
    folder_token = extract_folder_token(args.folder)
    state_path = find_state_file(local_base)

    if os.path.exists(state_path):
        print(f"⚠ 状态文件已存在: {state_path}")
        print("  如需重新初始化，请先删除该文件")
        sys.exit(1)

    if not os.path.isdir(local_base):
        print(f"✗ 目录不存在: {local_base}")
        sys.exit(1)

    files, dirs = scan_local(local_base)
    if not files:
        print(f"✗ 目录为空: {local_base}")
        sys.exit(1)

    print(f"📁 本地目录: {os.path.abspath(local_base)}")
    print(f"☁️  飞书文件夹: {folder_token}")
    print(f"📊 文件数: {len(files)}, 子目录: {len(dirs)}")
    print()

    # 1. 创建文件夹结构
    folder_map = {}
    print("=== 创建文件夹结构 ===")
    for d in get_dir_hierarchy(dirs):
        # 获取父目录 token
        parts = d.split("/")
        if len(parts) == 1:
            parent = folder_token
        else:
            parent = folder_map.get("/".join(parts[:-1]), folder_token)
        name = parts[-1]
        try:
            token = create_folder(name, parent)
            folder_map[d] = token
            print(f"  ✓ {d} → {token}")
        except Exception as e:
            print(f"  ✗ {d} → {e}")
        time.sleep(0.2)

    print()

    # 2. 上传文件
    file_map = {}
    success = 0
    fail = 0

    print("=== 上传文件 ===")
    for rel_path, abs_path in files:
        target_token = get_folder_token_for_path(rel_path, {"folder_token": folder_token, "folder_map": folder_map})
        basename = os.path.basename(rel_path)

        try:
            if rel_path.endswith(".md"):
                title = basename[:-3]  # 去掉 .md
                with open(abs_path, "r", encoding="utf-8") as f:
                    content = f.read()
                token = create_doc(title, content, target_token)
                file_type = "docx"
            else:
                # upload 需要相对于 CWD 的路径
                cwd_rel = os.path.relpath(abs_path)
                token = upload_file(cwd_rel, target_token)
                file_type = "file"

            local_hash = sha256_file(abs_path)
            file_map[rel_path] = {
                "token": token,
                "type": file_type,
                "local_hash": local_hash,
                "feishu_modified": int(time.time()),
            }
            success += 1
            print(f"  ✓ {rel_path}")
        except Exception as e:
            fail += 1
            print(f"  ✗ {rel_path} → {e}")

        time.sleep(0.3)

    # 3. 写入状态文件
    state = {
        "version": 1,
        "folder_token": folder_token,
        "local_base": local_base,
        "folder_map": folder_map,
        "files": file_map,
    }
    save_state(state_path, state)

    print()
    print(f"=== 完成 ===")
    print(f"  成功: {success}, 失败: {fail}")
    print(f"  状态文件: {state_path}")


def cmd_push(args):
    """推送本地变更到飞书"""
    local_base = args.dir
    state_path = find_state_file(local_base)
    state = load_state(state_path)

    if state["local_base"] != local_base:
        print(f"✗ 状态文件中的目录 ({state['local_base']}) 与指定目录 ({local_base}) 不匹配")
        sys.exit(1)

    files, dirs = scan_local(local_base)
    existing_files = set(state["files"].keys())

    # 检测新文件和修改的文件
    new_files = []
    modified_files = []
    deleted_files = []

    for rel_path, abs_path in files:
        if rel_path not in existing_files:
            new_files.append((rel_path, abs_path))
        else:
            current_hash = sha256_file(abs_path)
            if current_hash != state["files"][rel_path]["local_hash"]:
                modified_files.append((rel_path, abs_path))

    for rel_path in existing_files:
        if not os.path.exists(os.path.join(local_base, rel_path)):
            deleted_files.append(rel_path)

    # 检测新目录
    existing_dirs = set(state["folder_map"].keys())
    new_dirs = [d for d in dirs if d not in existing_dirs]

    # 创建新目录
    if new_dirs:
        print("=== 创建新文件夹 ===")
        for d in get_dir_hierarchy(new_dirs):
            parts = d.split("/")
            if len(parts) == 1:
                parent = state["folder_token"]
            else:
                parent = state["folder_map"].get("/".join(parts[:-1]), state["folder_token"])
            try:
                token = create_folder(parts[-1], parent)
                state["folder_map"][d] = token
                print(f"  ✓ {d}")
            except Exception as e:
                print(f"  ✗ {d} → {e}")
            time.sleep(0.2)
        print()

    # 推送新文件
    if new_files:
        print(f"=== 推送新文件 ({len(new_files)}) ===")
        for rel_path, abs_path in new_files:
            target_token = get_folder_token_for_path(rel_path, state)
            basename = os.path.basename(rel_path)
            try:
                if rel_path.endswith(".md"):
                    title = basename[:-3]
                    with open(abs_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    token = create_doc(title, content, target_token)
                    file_type = "docx"
                else:
                    cwd_rel = os.path.relpath(abs_path)
                    token = upload_file(cwd_rel, target_token)
                    file_type = "file"
                state["files"][rel_path] = {
                    "token": token,
                    "type": file_type,
                    "local_hash": sha256_file(abs_path),
                    "feishu_modified": int(time.time()),
                }
                print(f"  ✓ {rel_path}")
            except Exception as e:
                print(f"  ✗ {rel_path} → {e}")
            time.sleep(0.3)
        print()

    # 推送修改的文件
    if modified_files:
        print(f"=== 推送修改 ({len(modified_files)}) ===")
        for rel_path, abs_path in modified_files:
            entry = state["files"][rel_path]
            try:
                if entry["type"] == "docx":
                    with open(abs_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    ok = update_doc(entry["token"], content)
                    if not ok:
                        raise RuntimeError("update returned not ok")
                else:
                    # 重新上传（drive upload 没有更新 API）
                    cwd_rel = os.path.relpath(abs_path)
                    token = upload_file(cwd_rel, get_folder_token_for_path(rel_path, state))
                    entry["token"] = token

                entry["local_hash"] = sha256_file(abs_path)
                entry["feishu_modified"] = int(time.time())
                print(f"  ✓ {rel_path}")
            except Exception as e:
                print(f"  ✗ {rel_path} → {e}")
            time.sleep(0.3)
        print()

    # 删除的文件
    if deleted_files:
        print(f"=== 本地已删除 ({len(deleted_files)}) ===")
        for rel_path in deleted_files:
            print(f"  ? {rel_path}")
        print("  (飞书侧文件未删除，如需清理请手动操作)")

    # 保存状态
    save_state(state_path, state)

    print("=== Push 完成 ===")
    print(f"  新增: {len(new_files)}, 修改: {len(modified_files)}, 删除: {len(deleted_files)}")


def cmd_pull(args):
    """从飞书拉取变更到本地"""
    local_base = args.dir
    state_path = find_state_file(local_base)
    state = load_state(state_path)

    files = state["files"]
    if not files:
        print("没有已同步的文件")
        return

    # 批量查询飞书元数据
    print("=== 检查飞书变更 ===")
    token_type_pairs = [(entry["token"], entry["type"]) for entry in files.values()]
    metas = batch_query_metas(token_type_pairs)
    print(f"  已查询 {len(metas)} 个文件元数据")

    # 检测变更
    changed = []
    for rel_path, entry in files.items():
        meta = metas.get(entry["token"])
        if not meta:
            print(f"  ⚠ {rel_path}: 飞书文件可能已删除")
            continue
        remote_time = int(meta.get("latest_modify_time", 0))
        local_time = entry.get("feishu_modified", 0)
        if remote_time > local_time:
            changed.append(rel_path)

    # 检测飞书侧新增文件
    print("  检测飞书侧新文件...")
    remote_items = list_all_folder_files_recursive(state)
    known_tokens = {entry["token"] for entry in files.values()}
    new_remote = [item for item in remote_items if item["token"] not in known_tokens
                  and item.get("name") != "" and not item.get("deleted")]

    if not changed and not new_remote:
        print("  所有文件已是最新")
        return

    if changed:
        print(f"  发现 {len(changed)} 个文件有变更")

    if new_remote:
        print(f"  发现 {len(new_remote)} 个飞书新增文件")

    print()

    # 拉取已有文件的变更
    now = int(time.time())

    if changed:
        print("=== 拉取变更 ===")
        for rel_path in changed:
            entry = files[rel_path]
            local_path = os.path.join(local_base, rel_path)

            try:
                if entry["type"] == "docx":
                    content = fetch_doc(entry["token"])
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    with open(local_path, "w", encoding="utf-8") as f:
                        f.write(content)
                else:
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    download_file(entry["token"], local_path)

                entry["local_hash"] = sha256_file(local_path)
                entry["feishu_modified"] = now
                print(f"  ✓ {rel_path}")
            except Exception as e:
                print(f"  ✗ {rel_path} → {e}")

            time.sleep(0.3)
        print()

    # 拉取飞书新增文件
    if new_remote:
        print(f"=== 拉取飞书新增文件 ({len(new_remote)}) ===")
        for item in new_remote:
            name = item.get("name", "")
            token = item["token"]
            rel_dir = item.get("_rel_dir", "")
            item_type = item.get("type", "")

            # 跳过文件夹
            if item_type == "folder":
                continue

            # 飞书文档类型：docx, doc, sheet, bitable, mindnote, slide 等
            doc_types = {"docx", "doc", "sheet", "bitable", "mindnote", "slide", "file"}
            is_doc = item_type in doc_types

            if is_doc:
                # 飞书文档 → 拉取为 .md
                rel_path = os.path.join(rel_dir, name) if name.endswith(".md") else os.path.join(rel_dir, f"{name}.md")
                local_path = os.path.join(local_base, rel_path)
                try:
                    content = fetch_doc(token)
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    with open(local_path, "w", encoding="utf-8") as f:
                        f.write(content)

                    files[rel_path] = {
                        "token": token,
                        "type": "docx",
                        "local_hash": sha256_file(local_path),
                        "feishu_modified": now,
                    }
                    print(f"  ✓ {rel_path} (文档)")
                except Exception as e:
                    print(f"  ✗ {name} → {e}")
            else:
                # 云盘文件
                rel_path = os.path.join(rel_dir, name)
                local_path = os.path.join(local_base, rel_path)
                try:
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    download_file(token, local_path)

                    files[rel_path] = {
                        "token": token,
                        "type": "file",
                        "local_hash": sha256_file(local_path),
                        "feishu_modified": now,
                    }
                    print(f"  ✓ {rel_path} (文件)")
                except Exception as e:
                    print(f"  ✗ {name} → {e}")

            time.sleep(0.3)
        print()

    save_state(state_path, state)
    print("=== Pull 完成 ===")


def cmd_status(args):
    """显示同步状态"""
    local_base = args.dir
    state_path = find_state_file(local_base)
    state = load_state(state_path)

    files, dirs = scan_local(local_base)
    existing_files = set(state["files"].keys())

    # 本地变更检测
    push_needed = []  # → 本地改了
    pull_needed = []  # ← 飞书改了
    conflict = []     # ⟷ 双边都改了
    new_local = []    # + 本地新增
    deleted_local = []  # - 本地删除

    # 批量查飞书元数据
    token_type_pairs = [(entry["token"], entry["type"]) for entry in state["files"].values()]
    metas = batch_query_metas(token_type_pairs)

    # 检查已跟踪文件的变更
    for rel_path, abs_path in files:
        if rel_path in existing_files:
            entry = state["files"][rel_path]
            current_hash = sha256_file(abs_path)
            meta = metas.get(entry["token"], {})
            remote_time = int(meta.get("latest_modify_time", entry.get("feishu_modified", 0)))

            local_changed = current_hash != entry["local_hash"]
            remote_changed = remote_time > entry.get("feishu_modified", 0)

            if local_changed and remote_changed:
                conflict.append((rel_path, current_hash, remote_time))
            elif local_changed:
                push_needed.append((rel_path, current_hash, entry["local_hash"]))
            elif remote_changed:
                pull_needed.append((rel_path, remote_time))
        else:
            new_local.append(rel_path)

    for rel_path in existing_files:
        if not os.path.exists(os.path.join(local_base, rel_path)):
            deleted_local.append(rel_path)

    # 检测飞书侧新增文件
    new_remote = []
    remote_items = list_all_folder_files_recursive(state)
    known_tokens = {entry["token"] for entry in state["files"].values()}
    for item in remote_items:
        if item["token"] not in known_tokens and item.get("name") != "" and not item.get("deleted"):
            new_remote.append(item.get("name", "未知"))

    # 输出
    total_tracked = len(existing_files)
    unchanged = total_tracked - len(push_needed) - len(pull_needed) - len(conflict)

    print(f"📁 本地目录: {local_base}")
    print(f"☁️  飞书文件夹: {state['folder_token']}")
    print(f"📊 跟踪文件: {total_tracked}")
    print()

    if push_needed:
        print(f"→ 待推送 ({len(push_needed)}):")
        for rel_path, new_hash, old_hash in push_needed:
            print(f"  {rel_path}  [{old_hash[:8]}→{new_hash[:8]}]")
        print()

    if pull_needed:
        print(f"← 待拉取 ({len(pull_needed)}):")
        for rel_path, ts in pull_needed:
            dt = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
            print(f"  {rel_path}  [{dt}]")
        print()

    if conflict:
        print(f"⟷ 冲突 ({len(conflict)}):")
        for rel_path, new_hash, ts in conflict:
            dt = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
            print(f"  {rel_path}  [{dt}]")
        print()

    if new_local:
        print(f"+ 本地新增 ({len(new_local)}):")
        for rel_path in new_local:
            print(f"  {rel_path}")
        print()

    if deleted_local:
        print(f"- 本地已删除 ({len(deleted_local)}):")
        for rel_path in deleted_local:
            print(f"  {rel_path}")
        print()

    if new_remote:
        print(f"↓ 飞书新增 ({len(new_remote)}):")
        for name in new_remote:
            print(f"  {name}")
        print("  (执行 pull 可拉取到本地)")
        print()

    if not any([push_needed, pull_needed, conflict, new_local, deleted_local, new_remote]):
        print("  ✓ 所有文件已同步，无差异")
        print()


# --- 入口 ---

def main():
    parser = argparse.ArgumentParser(description="feishu-sync: 本地目录 ↔ 飞书云文档双向同步")
    parser.add_argument("action", choices=["init", "push", "pull", "status"], help="操作")
    parser.add_argument("--dir", default="docs", help="本地目录 (默认: docs)")
    parser.add_argument("--folder", help="飞书文件夹 URL 或 token (init 必需)")

    args = parser.parse_args()

    if args.action == "init":
        if not args.folder:
            print("✗ init 命令需要 --folder 参数")
            print("  用法: python sync.py init --folder <url|token> [--dir docs]")
            sys.exit(1)
        cmd_init(args)
    elif args.action == "push":
        cmd_push(args)
    elif args.action == "pull":
        cmd_pull(args)
    elif args.action == "status":
        cmd_status(args)


if __name__ == "__main__":
    main()
