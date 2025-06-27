import os
import json

# 分类目录及中文标题
subdirs = [
    ("kali-backdoor", "后门技术"),
    ("kali-server-attack", "服务器攻击"),
    ("kali-web-attack", "Web 攻击")
]

# 读取 title_map.json 以获得每篇文档的中文标题（如有）
title_map_path = "title_map.json"
if os.path.exists(title_map_path):
    with open(title_map_path, "r", encoding="utf-8") as f:
        title_map = json.load(f)
else:
    title_map = {}

def get_title(subdir, md):
    key = f"{subdir}/{md}"
    return title_map.get(key, md.replace('.md', ''))

print("nav:")
for subdir, cname in subdirs:
    if not os.path.isdir(subdir):
        continue
    print(f"  - title: {cname}")
    print(f"    url: /{subdir}/")
    print(f"    children:")
    md_files = [f for f in os.listdir(subdir)
                if f.endswith('.md') and f != "index.md"]
    md_files.sort()
    for md in md_files:
        title = get_title(subdir, md)
        url = f"/{subdir}/{md.replace('.md','')}"
        print(f"      - title: {title}")
        print(f"        url: {url}")