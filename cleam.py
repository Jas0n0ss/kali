import os
import re

img_dir = "imgs"
subdirs = [
    "kali-backdoor",
    "kali-server-attack",
    "kali-web-attack"
]

# 收集所有 md 文件内容
all_md_content = ""
for subdir in subdirs:
    if not os.path.isdir(subdir):
        continue
    for fname in os.listdir(subdir):
        if fname.endswith('.md'):
            with open(os.path.join(subdir, fname), "r", encoding="utf-8") as f:
                all_md_content += f.read()

# 检查 imgs 目录下所有图片
if os.path.isdir(img_dir):
    for img_file in os.listdir(img_dir):
        img_path = os.path.join(img_dir, img_file)
        # 检查是否被引用（../imgs/ 或 imgs/）
        if (f"../imgs/{img_file}" not in all_md_content) and (f"imgs/{img_file}" not in all_md_content):
            os.remove(img_path)
            print(f"已删除未引用图片: {img_path}")

print("未被引用图片清理完成。")