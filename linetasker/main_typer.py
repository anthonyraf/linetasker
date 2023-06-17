import typer
from typing import Annotated
from linetasker.core import Register

app = typer.Typer(add_completion=False)

register = Register(".linetasker.json")


@app.command()
def new(
    task: str,
    priority: Annotated[
        int,
        typer.Option(
            "--priority",
            "-p",
            help="set priority of the task",
            clamp=True,
            min=1,
            max=4,
        ),
    ] = 1,
) -> None:
    """Create new task"""
    register.create_task(task, priority)


@app.command()
def done(id: int) -> None:
    """Mark as done a task by its id."""
    register.done(id)


@app.command()
def delete(id: int) -> None:
    """Delete a task by its id"""
    register.delete_task(id)


@app.command()
def update(id: int) -> None:
    """Edit existing task"""
    pass


@app.command()
def list(
    n: Annotated[
        int, typer.Option("-n", help="Number of tasks to show")
    ] = None  # type: ignore
) -> None:
    """List the tasks"""
    register.list()


if __name__ == "__main__":
    app()
