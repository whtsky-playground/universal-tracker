#!/usr/bin/env python3
"""
从 Notion 拉数据，生成静态 HTML。
用法: python3 build.py
"""
import json, subprocess, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH = os.path.expanduser("~/clawd/secrets/notion.json")
DS_ID = "9ac28a84-c975-4267-b29f-6baec463986a"
TEMPLATE = os.path.join(SCRIPT_DIR, "src", "index.html")
OUTPUT = os.path.join(SCRIPT_DIR, "docs", "index.html")

def fetch_notion_data():
    with open(SECRETS_PATH) as f:
        key = json.load(f)["api_key"]

    import urllib.request
    req = urllib.request.Request(
        f"https://api.notion.com/v1/data_sources/{DS_ID}/query",
        data=json.dumps({"sorts": [{"property": "日期", "direction": "descending"}]}).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Notion-Version": "2025-09-03",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    records = []
    for page in data.get("results", []):
        props = page.get("properties", {})
        name = "".join(t.get("plain_text", "") for t in (props.get("项目", {}).get("title") or []))
        date_obj = props.get("日期", {}).get("date")
        date = date_obj.get("start", "") if date_obj else ""
        type_obj = props.get("类型", {}).get("select")
        typ = type_obj.get("name", "") if type_obj else ""
        orig = props.get("原价", {}).get("number", 0) or 0
        paid = props.get("实付", {}).get("number", 0) or 0
        records.append({"name": name, "date": date, "type": typ, "original": orig, "paid": paid, "saved": orig - paid})
    return records

def build():
    records = fetch_notion_data()
    with open(TEMPLATE) as f:
        html = f.read()
    html = html.replace("__DATA__", json.dumps(records, ensure_ascii=False))
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w") as f:
        f.write(html)
    print(f"Built {OUTPUT} with {len(records)} records")

if __name__ == "__main__":
    build()
