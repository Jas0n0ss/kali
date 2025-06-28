import os
import re
import requests
from urllib.parse import urlparse, unquote
import time

subdirs = [
    "kali-backdoor",
    "kali-server-attack",
    "kali-web-attack"
]

img_dir = "imgs"
os.makedirs(img_dir, exist_ok=True)

img_pattern = re.compile(r'!\[(.*?)\]\((http[s]?://[^\)]+)\)')

# 支持的图片后缀
img_exts = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']

def get_img_filename(url):
    parsed = urlparse(url)
    fname = os.path.basename(parsed.path)
    fname = unquote(fname)
    # 去掉参数和-wm等后缀
    fname = fname.split('?')[0]
    # 保留图片格式后缀
    for ext in img_exts:
        if fname.lower().endswith(ext):
            base = fname[:fname.lower().rfind(ext)]
            return base + ext
    # 如果没有图片后缀，默认加.png
    return fname + ".png"

def download_image(url, save_dir, retries=3, timeout=30):
    filename = get_img_filename(url)
    save_path = os.path.join(save_dir, filename)
    base, ext = os.path.splitext(filename)
    i = 1
    while os.path.exists(save_path):
        filename = f"{base}_{i}{ext}"
        save_path = os.path.join(save_dir, filename)
        i += 1
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(resp.content)
            print(f"下载图片: {url} -> {save_path}")
            return filename
        except Exception as e:
            print(f"下载失败: {url} (第{attempt+1}次, {e})")
            time.sleep(2)
    return None

for subdir in subdirs:
    if not os.path.isdir(subdir):
        continue
    for fname in os.listdir(subdir):
        if fname.endswith('.md'):
            fpath = os.path.join(subdir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = content
            for match in img_pattern.finditer(content):
                alt, url = match.groups()
                img_filename = download_image(url, img_dir)
                if img_filename:
                    # 保持原有描述，替换为本地图片路径
                    new_content = new_content.replace(url, f"../imgs/{img_filename}")
            if new_content != content:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"已更新图片链接: {fpath}")

print("处理完成。")