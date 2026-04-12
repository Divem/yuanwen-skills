#!/usr/bin/env python3
"""Fetch Bilibili video comments via API.

Usage:
  python3 bilibili_comments.py <BV_ID> [options]

Options:
  --cookie COOKIE    Bilibili cookie string (SESSDATA, bili_jct, DedeUserID, DedeUserID__ckMd5)
  --limit N          Max comments to fetch (default: 100)
  --sort SORT        Sort by: 2=time (default), 1=hot
  --output FILE      Output JSON file (default: stdout)
  --include-sub      Include sub-replies (default: true)
"""

import sys
import json
import time
import re
import subprocess
import argparse


COOKIES_ENV = "BILIBILI_COOKIE"


def fetch_page(oid, pn, ps, sort, cookies):
    url = f"https://api.bilibili.com/x/v2/reply?type=1&oid={oid}&pn={pn}&ps={ps}&sort={sort}&nohot=1"
    result = subprocess.run(
        [
            "curl",
            "-s",
            "-H",
            f"Cookie: {cookies}",
            "-H",
            "User-Agent: Mozilla/5.0",
            url,
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)


def format_time(ts):
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(ts))


def clean_message(msg):
    msg = msg.replace("\n", " ").replace("\r", "")
    return re.sub(r"<[^>]+>", "", msg)


def fetch_comments(bv_id, cookies, limit=100, sort=2, include_sub=True):
    resp = subprocess.run(
        [
            "curl",
            "-s",
            "-H",
            f"Cookie: {cookies}",
            "-H",
            "User-Agent: Mozilla/5.0",
            f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    data = json.loads(resp.stdout)
    if data["code"] != 0:
        print(f"Error fetching video info: {data['message']}", file=sys.stderr)
        return []
    oid = str(data["data"]["aid"])
    title = data["data"]["title"]
    stat = data["data"]["stat"]
    print(f"Video: {title} (aid={oid})", file=sys.stderr)
    print(
        f"Stats: {stat['reply']} comments, {stat['like']} likes, {stat['view']} views",
        file=sys.stderr,
    )

    all_comments = []
    seen = set()

    for pn in range(1, 50):
        if len(all_comments) >= limit:
            break
        page_data = fetch_page(oid, pn, 20, sort, cookies)
        if (
            not page_data
            or page_data["code"] != 0
            or not page_data["data"].get("replies")
        ):
            break

        for r in page_data["data"]["replies"]:
            if r["rpid_str"] in seen:
                continue
            seen.add(r["rpid_str"])
            all_comments.append(
                {
                    "rpid": r["rpid_str"],
                    "uname": r["member"]["uname"],
                    "level": r["member"]["level_info"]["current_level"],
                    "message": clean_message(r["content"]["message"])[:1000],
                    "like": r["like"],
                    "ctime": format_time(r["ctime"]),
                    "rcount": r["rcount"],
                    "is_root": True,
                }
            )

            if include_sub and r.get("replies"):
                for sr in r["replies"]:
                    if sr["rpid_str"] not in seen:
                        seen.add(sr["rpid_str"])
                        all_comments.append(
                            {
                                "rpid": sr["rpid_str"],
                                "uname": sr["member"]["uname"],
                                "level": sr["member"]["level_info"]["current_level"],
                                "message": clean_message(sr["content"]["message"])[
                                    :1000
                                ],
                                "like": sr["like"],
                                "ctime": format_time(sr["ctime"]),
                                "rcount": sr["rcount"],
                                "is_root": False,
                            }
                        )
                        if len(all_comments) >= limit:
                            break

        print(
            f"  Page {pn}: {len(page_data['data']['replies'])} threads, total: {len(all_comments)}",
            file=sys.stderr,
        )
        time.sleep(0.5)

    return all_comments


def build_rows(comments):
    rows = []
    for i, c in enumerate(comments, 1):
        rows.append(
            [
                str(i),
                c["uname"],
                str(c["level"]),
                c["message"],
                str(c["like"]),
                c["ctime"],
                str(c["rcount"]),
                "yes" if c["is_root"] else "no",
            ]
        )
    return rows


def main():
    parser = argparse.ArgumentParser(description="Fetch Bilibili video comments")
    parser.add_argument("bv_id", help="Bilibili video BV ID (e.g. BV1ooDyBmE6v)")
    parser.add_argument("--cookie", default=None, help="Bilibili cookie string")
    parser.add_argument(
        "--limit", type=int, default=100, help="Max comments (default: 100)"
    )
    parser.add_argument(
        "--sort", type=int, default=2, help="Sort: 2=time, 1=hot (default: 2)"
    )
    parser.add_argument("--output", default=None, help="Output JSON file")
    parser.add_argument("--no-sub", action="store_true", help="Exclude sub-replies")
    parser.add_argument(
        "--rows", action="store_true", help="Output as row array for lark-cli"
    )
    args = parser.parse_args()

    import os

    cookies = args.cookie or os.environ.get(COOKIES_ENV, "")
    if not cookies:
        print("Error: provide --cookie or set BILIBILI_COOKIE env var", file=sys.stderr)
        print(
            "Required keys: SESSDATA, bili_jct, DedeUserID, DedeUserID__ckMd5",
            file=sys.stderr,
        )
        sys.exit(1)

    comments = fetch_comments(
        args.bv_id, cookies, args.limit, args.sort, include_sub=not args.no_sub
    )
    print(f"\nTotal collected: {len(comments)} comments", file=sys.stderr)

    if args.rows:
        rows = build_rows(comments)
        output = json.dumps(rows, ensure_ascii=False)
    else:
        output = json.dumps(comments, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
