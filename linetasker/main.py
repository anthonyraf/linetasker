import click
from linetasker.core import Register

register = Register(".py_tasks.json")


@click.group()
def cli():
    """PyTasks is a minimalist todo app with local file database"""
    pass


@cli.command()
@click.argument("task", type=str)
@click.option(
    "-p",
    "--priority",
    type=click.IntRange(1, 5, clamp=True),
    help="Priority of the task",
    default=1,
)
def new(task, priority):
    """Create new task"""
    register.create_task(task, priority)


@cli.command()
@click.argument("id", type=int)
def delete(id):
    """Delete a task by its id"""
    register.delete_task(id)


@cli.command()
@click.argument("id", type=int)
def update(id):
    """Edit existing task"""
    pass


@cli.command()
@click.option("-n", type=int)
def list(n):
    """List the tasks"""
    register.list()


@cli.command()
@click.argument("id", type=int)
def done(id):
    register.done(id)


if __name__ == "__main__":
    cli()
