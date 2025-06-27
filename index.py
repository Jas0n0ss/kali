import os

subdirs = [
    "kali-backdoor",
    "kali-server-attack",
    "kali-web-attack"
]

titles = {
    "kali-backdoor": "后门技术",
    "kali-server-attack": "服务器攻击",
    "kali-web-attack": "Web 攻击"
}

# 生成各子目录 index.md
for subdir in subdirs:
    if not os.path.isdir(subdir):
        continue
    md_files = [f for f in os.listdir(subdir)
                if f.endswith('.md') and f != "index.md"]
    md_files.sort()
    lines = [f"# {titles.get(subdir, subdir)}\n"]
    for md in md_files:
        title = md.replace('.md', '')
        lines.append(f"- [{title}]({md})")
    content = "\n".join(lines) + "\n"
    with open(os.path.join(subdir, "index.md"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {subdir}/index.md")

# 生成根目录 README.md
readme_lines = ["# Kali 技术文档合集\n"]
for subdir in subdirs:
    if os.path.isdir(subdir):
        readme_lines.append(f"- [{titles.get(subdir, subdir)}]({subdir}/)")
readme_content = "\n".join(readme_lines) + "\n"
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
print("Generated README.md")