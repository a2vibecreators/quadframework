"""
Console utilities for QUAD CLI
==============================

Provides consistent styling for terminal output.
"""

from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint


class Console:
    """Simple console utilities for interactive prompts"""

    _console = RichConsole()

    @classmethod
    def header(cls, text: str):
        """Print a section header"""
        print(f"\n  {text}")
        print(f"  {'─' * len(text)}\n")

    @classmethod
    def success(cls, text: str):
        """Print success message"""
        rprint(f"  [green]✓[/green] {text}")

    @classmethod
    def info(cls, text: str):
        """Print info message"""
        rprint(f"  [blue]→[/blue] {text}")

    @classmethod
    def error(cls, text: str):
        """Print error message"""
        rprint(f"  [red]✗[/red] {text}")

    @classmethod
    def warn(cls, text: str):
        """Print warning message"""
        rprint(f"  [yellow]⚠[/yellow] {text}")

    @classmethod
    def step(cls, num: int, text: str):
        """Print numbered step"""
        print(f"  {num}. {text}")

    @classmethod
    def ask(cls, question: str, default: str = None) -> str:
        """Ask a text question"""
        if default:
            prompt = f"  {question} [{default}]: "
        else:
            prompt = f"  {question}: "

        answer = input(prompt).strip()
        return answer if answer else default

    @classmethod
    def confirm(cls, question: str, default: bool = True) -> bool:
        """Ask yes/no question"""
        suffix = "[Y/n]" if default else "[y/N]"
        answer = input(f"  {question} {suffix}: ").strip().lower()

        if not answer:
            return default
        return answer in ("y", "yes")

    @classmethod
    def select(cls, question: str, options: list, default: int = 0) -> int:
        """Ask multiple choice question"""
        print(f"\n  {question}\n")
        for i, option in enumerate(options):
            marker = "●" if i == default else "○"
            print(f"    [{i + 1}] {marker} {option}")
        print()

        while True:
            answer = input(f"  Select [1-{len(options)}]: ").strip()
            if not answer:
                return default
            try:
                idx = int(answer) - 1
                if 0 <= idx < len(options):
                    return idx
            except ValueError:
                pass
            cls.error(f"Please enter a number between 1 and {len(options)}")

    @classmethod
    def table(cls, title: str, columns: list, rows: list):
        """Print a formatted table"""
        table = Table(title=title, show_header=True, header_style="bold")
        for col in columns:
            table.add_column(col)
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        cls._console.print(table)

    @classmethod
    def panel(cls, content: str, title: str = None):
        """Print content in a panel"""
        cls._console.print(Panel(content, title=title))
