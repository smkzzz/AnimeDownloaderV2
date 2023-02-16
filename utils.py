from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.console import Console
from config import *
console = Console()


def create_loading(msg, color, process, *args):
    with console.status(f"[bold {color}]{msg}") as status:
        process(*args)


def create_msg(msg_title, msg, colors,):
    console.print(
        f"[bold {colors['title']}]{msg_title}: [/bold {colors['title']}][bold {colors['text']}]{msg}")


def create_prompt(prompt_msg):
    return Prompt.ask(f"[{USER_PROMPT}]\n\t\t{prompt_msg}")


def create_panel(banner_msg, banner_inner_text):
    Panel(Text(f"{banner_msg}",
               justify="center", style=f"bold {BANNER['banner_border']}"), title=f"[bold {BANNER['banner_title']}]{banner_inner_text}", border_style=f"{BANNER['banner_border']}", padding=1)
