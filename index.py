import os
import re

subdirs = [
    "kali-backdoor",
    "kali-server-attack",
    "kali-web-attack"
]

def extract_num(fname):
    m = re.match(r'^(\d+)\.', fname)
    return int(m.group(1)) if m else 9999

for subdir in subdirs:
    if not os.path.isdir(subdir):
        continue
    md_files = [f for f in os.listdir(subdir)
                if f.endswith('.md') and f != "index.md"]
    # 按数字编号排序
    md_files.sort(key=extract_num)
    lines = ["# {} 文档列表\n".format(subdir)]
    for fname in md_files:
        lines.append(f"- [{fname[:-3]}]({fname})")
    with open(os.path.join(subdir, "index.md"), "w", encoding="utf-8") as f:
        f.write('\n'.join(lines) + '\n')
    print(f"已生成 {subdir}/index.md，顺序与文件名一致。")
