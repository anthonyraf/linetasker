from rich import box
from rich.align import Align
from rich.table import Table
from rich.console import Console
from linetasker.utils.levelbar import LevelBar
from linetasker.task import Status

console = Console()


class DetailedTask:
    def __init__(self) -> None:
        pass


class TaskTemplate:
    def __init__(
        self,
        id: int,
        created: list,
        description: str,
        priority: int,
        tags: list,
        status: str,
    ) -> None:
        self.id = id
        self.created = f"{created[0]} {created[1]}"
        self.description = description
        self.priority: str = LevelBar(priority)
        self.tags = self.format_tags(tags)
        self.status = self.format_status(status)

    @staticmethod
    def format_status(status: str) -> str | None:
        active_char = "⚙"  # U+2713 CHECK MARK
        done_char = "✔"  # U+2699 GEAR
        if status == Status.ACTIVE:
            return f"[green]{active_char} Active[/green]"
        elif status == Status.DONE:
            return f"[yellow]{done_char} Done[/yellow]"

    @staticmethod
    def format_tags(tags: list[str]) -> str:
        _tags: list[str] = []
        if tags:
            for i in range(len(tags) - 1):
                _tags.append(f"[bold]{tags[i]}, [/bold]")

            _tags.append(f"[bold]{tags[-1]}[/bold]")

        return "".join(_tags)


class TaskList:
    def __init__(self) -> None:
        self.table = Table(box=box.SIMPLE, leading=1)

        self.columns = {
            "[bold yellow]ID[/bold yellow]": dict(
                justify="left", width=None, style="yellow"
            ),
            "[blue]Created[/blue]": dict(
                justify="left", width=None, style="blue"
            ),
            "Description": dict(justify="left", max_width=40),
            "Priority": dict(justify="left", width=None),
            "Tags": dict(justify="left", max_width=20),
            "Status": dict(justify="left", width=None),
        }
        for column, args in self.columns.items():
            self.table.add_column(column, **args)

    def add_rows(self, *tasks: TaskTemplate) -> None:
        for task in tasks:
            self.table.add_row(*list(map(str, task.__dict__.values())))

    def render(self) -> Align:
        return Align.center(self.table)
