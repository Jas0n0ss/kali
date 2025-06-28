import os
import re

subdirs = [
    "kali-backdoor",
    "kali-server-attack",
    "kali-web-attack"
]

# 代码语言识别规则
def guess_lang(code):
    code = code.strip()
    if code.startswith('$ ') or code.startswith('sudo ') or code.startswith('apt ') or code.startswith('ls ') or code.startswith('cat '):
        return 'bash'
    if code.startswith('python ') or code.startswith('pip '):
        return 'bash'
    if code.startswith('def ') or code.startswith('import ') or code.startswith('print('):
        return 'python'
    if code.startswith('#include') or code.startswith('int main'):
        return 'c'
    if code.startswith('function ') or code.startswith('echo ') or code.startswith('sh '):
        return 'bash'
    if code.startswith('SELECT ') or code.startswith('INSERT ') or code.startswith('UPDATE '):
        return 'sql'
    if code.startswith('<html>') or code.startswith('<!DOCTYPE html>'):
        return 'html'
    if code.startswith('var ') or code.startswith('let ') or code.startswith('console.log'):
        return 'javascript'
    if code.startswith('<?php') or code.startswith('echo "') or code.startswith('echo \''):
        return 'php'
    return ''

def format_code_blocks(lines):
    new_lines = []
    in_code = False
    code_lines = []
    for i, line in enumerate(lines):
        # 检测三反引号代码块
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
                code_lang = line.strip().strip('`')
            else:
                in_code = False
                if code_lang:
                    new_lines.append(f"```{code_lang}")
                else:
                    # 自动识别
                    lang = guess_lang(code_lines[0]) if code_lines else ''
                    new_lines.append(f"```{lang}")
                new_lines.extend(code_lines)
                new_lines.append("```")
            continue
        if in_code:
            code_lines.append(line)
        else:
            # 检测以4空格或tab开头的代码块
            if (line.startswith('    ') or line.startswith('\t')):
                # 收集连续的代码块
                code_block = [line.lstrip()]
                j = i + 1
                while j < len(lines) and (lines[j].startswith('    ') or lines[j].startswith('\t')):
                    code_block.append(lines[j].lstrip())
                    j += 1
                lang = guess_lang(code_block[0])
                new_lines.append(f"```{lang}")
                new_lines.extend(code_block)
                new_lines.append("```")
                # 跳过已处理的行
                for _ in range(j - i - 1):
                    next(lines, None)
                continue
            # 检测 shell 行
            if re.match(r'^\s*\$ .+', line):
                new_lines.append("```bash")
                new_lines.append(line.lstrip('$ ').strip())
                new_lines.append("```")
            else:
                new_lines.append(line)
    # 文件结尾如果还在代码块
    if in_code and code_lines:
        lang = guess_lang(code_lines[0])
        new_lines.append(f"```{lang}")
        new_lines.extend(code_lines)
        new_lines.append("```")
    return new_lines

for subdir in subdirs:
    if not os.path.isdir(subdir):
        continue
    for fname in os.listdir(subdir):
        if fname.endswith('.md'):
            fpath = os.path.join(subdir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.splitlines()
            lines = format_code_blocks(lines)
            new_content = '\n'.join(lines)
            if new_content != content:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"已自动格式化代码块: {fpath}")

print("所有 Markdown 文件已自动识别并格式化代码块。")