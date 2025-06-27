import os
import json

# 分类目录及中文标题
subdirs = [
    ("kali-backdoor", "后门技术"),
    ("kali-server-attack", "服务器攻击"),
    ("kali-web-attack", "Web 攻击")
]

title_map_path = "title_map.json"

def scan_and_update_title_map():
    """自动扫描所有md文件，生成/更新title_map.json"""
    title_map = {}
    for subdir, _ in subdirs:
        if not os.path.isdir(subdir):
            continue
        md_files = [f for f in os.listdir(subdir)
                    if f.endswith('.md') and f != "index.md"]
        for md in sorted(md_files):
            key = f"{subdir}/{md}"
            title_map[key] = md.replace('.md', '')
    # 保留已填写的中文标题
    if os.path.exists(title_map_path):
        with open(title_map_path, "r", encoding="utf-8") as f:
            old_map = json.load(f)
        for k in title_map:
            if k in old_map and old_map[k] != title_map[k]:
                title_map[k] = old_map[k]
    with open(title_map_path, "w", encoding="utf-8") as f:
        json.dump(title_map, f, ensure_ascii=False, indent=2)
    print(f"已生成/更新 {title_map_path}，可在其中补充中文标题。")

def generate_indexes():
    """为每个分类目录生成index.md"""
    with open(title_map_path, "r", encoding="utf-8") as f:
        title_map = json.load(f)
    for subdir, cname in subdirs:
        if not os.path.isdir(subdir):
            continue
        md_files = [f for f in os.listdir(subdir)
                    if f.endswith('.md') and f != "index.md"]
        md_files.sort()
        lines = [f"# {cname}文档列表\n"]
        for md in md_files:
            key = f"{subdir}/{md}"
            title = title_map.get(key, md.replace('.md', ''))
            lines.append(f"- [{title}]({md})")
        content = "\n".join(lines) + "\n"
        with open(os.path.join(subdir, "index.md"), "w", encoding="utf-8") as f:
            f.write(content)
        print(f"已生成 {subdir}/index.md")

def clean_extra_indexes():
    """清理各分类目录下多余的index*.md文件，只保留index.md"""
    for subdir, _ in subdirs:
        if not os.path.isdir(subdir):
            continue
        for fname in os.listdir(subdir):
            if fname.lower().startswith('index') and fname != "index.md":
                os.remove(os.path.join(subdir, fname))
                print(f"已删除多余文件: {subdir}/{fname}")

if __name__ == "__main__":
    scan_and_update_title_map()
    generate_indexes()
    clean_extra_indexes()