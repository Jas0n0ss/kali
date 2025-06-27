import os
import json

subdirs = [
    "kali-backdoor",
    "kali-server-attack",
    "kali-web-attack"
]

title_map = {}

for subdir in subdirs:
    if not os.path.isdir(subdir):
        continue
    md_files = [f for f in os.listdir(subdir)
                if f.endswith('.md') and f != "index.md"]
    for md in sorted(md_files):
        key = f"{subdir}/{md}"
        title_map[key] = md.replace('.md', '')

with open("title_map.json", "w", encoding="utf-8") as f:
    json.dump(title_map, f, ensure_ascii=False, indent=2)

print("已生成 title_map.json，请在其中补充/修改中文标题。")