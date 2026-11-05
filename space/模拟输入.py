"""学习通等网页禁止粘贴时：用键盘模拟逐字输入。
用法（二选一）：
1) 直接复制文本 → 双击「运行模拟输入.bat」→ 5 秒内点进答题框
2) 把文本粘贴进同目录 data.txt 并保存 → 再运行
"""

from __future__ import annotations

import time
from pathlib import Path

from pynput.keyboard import Controller


def read_clipboard() -> str:
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        try:
            text = root.clipboard_get()
        except tk.TclError:
            text = ""
        root.destroy()
        return text if isinstance(text, str) else ""
    except Exception:
        return ""


def read_data_txt() -> str:
    path = Path(__file__).with_name("data.txt")
    if not path.exists():
        return ""
    for encoding in ("utf-8-sig", "utf-8", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def pick_text() -> str:
    clip = read_clipboard().strip()
    file_text = read_data_txt().strip()
    # 优先用剪贴板；剪贴板为空或仍是占位说明时，改用 data.txt
    placeholder = "把要输入的内容粘贴到这里"
    if clip and placeholder not in clip:
        return clip
    if file_text and placeholder not in file_text:
        return file_text
    return clip or file_text


def main() -> None:
    data = pick_text()
    if not data:
        print("剪贴板和 data.txt 都是空的，请先复制要输入的文本。")
        input("按回车退出…")
        return

    print(f"即将输入 {len(data)} 个字符。")
    print("请在倒计时结束前，用鼠标点进学习通答题框！")
    for i in range(5, 0, -1):
        print(f"程序还有 {i} 秒启动…")
        time.sleep(1)

    keyboard = Controller()
    for char in data:
        keyboard.type(char)
        time.sleep(0.01)

    print("\n文本输入完成！")
    input("按回车退出…")


if __name__ == "__main__":
    main()
