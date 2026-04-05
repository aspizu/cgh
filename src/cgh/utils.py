import subprocess
import webbrowser
from pathlib import Path


def open_browser(url: str) -> None:
    if "microsoft" in Path("/proc/version").read_text().lower():
        subprocess.run(
            ["/mnt/c/Windows/System32/cmd.exe", "/c", "start", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    else:
        webbrowser.open(url)
