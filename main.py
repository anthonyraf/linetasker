import click
from register import Register

register = Register("database.json")

@click.group()
def cli():
    pass

@cli.command()
def init():
    register.init_db()

@cli.command()
@click.option("-m","--message", type=str,help="The task message to add",metavar="<text>", required=True)
@click.option("-p", "--priority", type=click.IntRange(1,5, clamp=True),metavar="<integer>",
              help="Priority of the task", default=1)
def add(message, priority):
    register.init_db()
    register.create_task(message, priority)

@cli.command(help="Remove a task by its partial or full hash [min length=5]")
@click.argument("hash", type=str)
def remove(hash):
    register.init_db()
    register.remove_task(hash)

@cli.command()
def update():
    #TODO
    pass


if __name__ == '__main__':
    cli()
