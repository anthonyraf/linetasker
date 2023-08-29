import click
import typer
from click.core import Context
from typer.core import MarkupMode, TyperGroup
from typing import Annotated, Any
from collections.abc import Sequence
from linetasker.core import Register


class DisableAutoSort(TyperGroup):
    def __init__(
        self,
        *,
        name: str | None = None,
        commands: dict[str, click.Command]
        | Sequence[click.Command]
        | None = None,
        rich_markup_mode: MarkupMode = None,
        rich_help_panel: str | None = None,
        **attrs: Any,
    ) -> None:
        super().__init__(
            name=name,
            commands=commands,
            rich_markup_mode=rich_markup_mode,
            rich_help_panel=rich_help_panel,
            **attrs,
        )

    def list_commands(self, ctx: Context) -> dict[str, click.Command]:
        return self.commands


app = typer.Typer(
    cls=DisableAutoSort,
    add_completion=False,
    help="LineTasker is a command line task manager for your project",
    rich_markup_mode="rich",
)

register = Register(".linetasker.json")


bo = "Basic operations"
add = "Additional"


@app.command(rich_help_panel=bo)
def new(
    task: str,
    tags: Annotated[
        list[str],
        typer.Option(
            "--tags", "-t", help="Add tags to the task", show_default=False
        ),
    ] = [],
    priority: Annotated[
        int,
        typer.Option(
            "--priority",
            "-p",
            help="Set priority of the task",
            clamp=True,
            min=1,
            max=4,
        ),
    ] = 1,
) -> None:
    """Create new task"""
    register.create_task(task, priority, tags)


@app.command(rich_help_panel=bo, name="del")
def delete(id: int) -> None:
    """Delete a task by its id"""
    register.delete_task(id)


@app.command(rich_help_panel=bo)
def done(id: int) -> None:
    """Mark as done a task by its id."""
    register.done(id)


@app.command(rich_help_panel=bo)
def undone(id: int) -> None:
    """Mark as undone a task by its id."""
    register.undone(id)


@app.command(rich_help_panel=add)
def list(
    n: Annotated[
        int, typer.Option("-n", help="Number of tasks to show")
    ] = None  # type: ignore
) -> None:
    """List the tasks"""
    register.list_tasks()


@app.command(rich_help_panel=add)
def edit(id: int) -> None:
    """Edit existing task"""
    pass


@app.command(rich_help_panel=add)
def clean() -> None:
    """Delete all [bold green]done[/] tasks"""
    register.clean()


@app.command(rich_help_panel=add)
def reset(
    bypass_flag: Annotated[
        bool, typer.Option("--yes", "-y", help="Bypass confirmation prompt")
    ] = False
) -> None:
    """Delete [bold red]all[/] tasks"""
    register.reset(bypass_flag)


if __name__ == "__main__":
    app()
