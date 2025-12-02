# 使用你html文件打开用户指南markdown文件

import os
import markdown
import webbrowser
from pathlib import Path

def call_help():
    # 读取Markdown文件
    md_path = os.path.abspath('../resource_/用户指南.md')
    print(md_path)
    html = markdown.markdown(Path(md_path).read_text())

    # 创建临时HTML文件
    temp_html = "text edictor 用户指南.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(f"<html><body>{html}</body></html>")

    # 用浏览器打开
    webbrowser.open(temp_html)
