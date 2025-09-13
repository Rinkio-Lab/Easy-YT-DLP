import urllib.parse
import subprocess
import shutil
import sys
import time
from pathlib import Path
from typing import Optional, Callable

from rich.console import Console
from rich.panel import Panel

import questionary

# rich 控制台实例
console = Console()

try:
    import clipboard_monitor  # 剪贴板监听库
except ImportError:
    clipboard_monitor = None


def check_ytdlp() -> None:
    """
    检查本机是否安装了 yt-dlp，并输出版本号。
    """
    if shutil.which("yt-dlp") is None:
        console.print("[bold red]未检测到 yt-dlp，请先安装并确保它在 PATH 中[/]")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["yt-dlp", "--version"], capture_output=True, text=True, check=True
        )
        version: str = result.stdout.strip()
        console.print(f"[bold green]检测到 yt-dlp[/] (版本: [cyan]{version}[/])")
    except subprocess.CalledProcessError:
        console.print("[bold red]yt-dlp 检测失败，请确认安装是否正常[/]")
        sys.exit(1)


def is_valid_url(url: str) -> bool:
    """
    判断输入是否是合法 URL。
    """
    if not url:
        return False
    parsed = urllib.parse.urlparse(url)
    return all([parsed.scheme in ("http", "https"), parsed.netloc])


def clean_url(url: str) -> str:
    """
    去掉 URL 的 query 参数，只保留核心部分。
    """
    parsed = urllib.parse.urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def download_audio(url: str, retries: int = 3, delay: int = 2) -> None:
    """
    使用 yt-dlp 下载音频为 mp3，保存到 ./Download 文件夹。
    - 若文件夹不存在则自动创建。
    - 文件名为视频标题。
    - 自动重试机制（默认最多重试 3 次，每次间隔 2 秒）。
    """
    if not is_valid_url(url):
        console.print("[yellow]请输入合法的 http/https URL[/]")
        return

    clean: str = clean_url(url)
    console.print(f"[cyan]解析结果: {clean}[/]")

    for attempt in range(1, retries + 1):
        try:
            subprocess.run(
                [
                    "yt-dlp",
                    "-f",
                    "bestaudio",
                    "--extract-audio",
                    "--audio-format",
                    "mp3",
                    "-o",
                    str(download_dir / "%(title)s.%(ext)s"),
                    clean,
                ],
                check=True,
            )
            console.print(
                f"[bold green]下载完成[/] → [cyan]{download_dir.resolve()}[/]"
            )
            return
        except subprocess.CalledProcessError:
            console.print(f"[bold red]第 {attempt} 次下载失败[/]")
            if attempt < retries:
                console.print(f"[yellow]{delay} 秒后重试...[/]")
                time.sleep(delay)
            else:
                console.print("[bold red]多次尝试后仍失败，已放弃下载[/]")


def manual_mode() -> None:
    """手动输入模式。"""
    console.print(Panel("[bold]手动输入模式[/] (输入 quit/exit 退出)", style="magenta"))

    while True:
        try:
            url: str = questionary.text("请输入视频 URL").ask()
            if not url:
                console.print("[yellow]输入为空，请重新输入[/]")
                continue
            if url.lower() in ("quit", "exit"):
                break
            download_audio(url)
        except KeyboardInterrupt:
            console.print("\n检测到 Ctrl+C，已退出手动模式", style="yellow")
            break


def clipboard_mode() -> None:
    """剪贴板监控模式。"""
    if clipboard_monitor is None:
        console.print(
            "[bold red]未安装 clipboard_monitor，请先运行: uv add clipboard-monitor[/]"
        )
        return

    console.print(Panel("剪贴板监控模式 (Ctrl+C 退出)", style="blue"))

    def on_clipboard_change(text: str) -> None:
        """回调函数：当剪贴板内容变化时触发"""
        if is_valid_url(text):
            console.print(f"\n检测到 URL: [cyan]{text}[/]")
            download_audio(text)

    clipboard_monitor.start_monitor(on_clipboard_change)  # type: ignore
    try:
        clipboard_monitor.wait()
    except KeyboardInterrupt:
        console.print("\n检测到 Ctrl+C，已退出剪贴板模式", style="yellow")
        clipboard_monitor.stop_monitor()  # type: ignore


def main() -> None:
    """程序入口"""
    
    # 创建 Download 文件夹
    global download_dir
    download_dir = Path("./Download")
    download_dir.mkdir(parents=True, exist_ok=True)

    console.print(Panel("欢迎使用 Easy YT-DLP\n\n作者: Rinkio-Lab\n版本: 1.0.0\nGitHub: https://github.com/Rinkio-Lab/Easy-YT-DLP"))
    
    # 检查依赖
    console.print("正在检查依赖...")
    check_ytdlp()

    choice: str = questionary.select(
        "菜单", choices=["1 运行模式: 手动输入 URL", "2 运行模式: 剪贴板监控 URL", "q 退出程序"]
    ).ask()

    if choice is None:
        console.print("未选择任何选项", style="yellow")
        return

    if choice.startswith("1"):
        manual_mode()
    elif choice.startswith("2"):
        clipboard_mode()
    elif choice.startswith("q"):
        console.print("已退出程序", style="green")
    else:
        console.print("未知选项", style="red")


if __name__ == "__main__":
    main()
