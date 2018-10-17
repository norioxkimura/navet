
import click
import sys

@click.group()
def navet():
    pass

@navet.command()
def version():
    print("navet 0.1")

@navet.command()
@click.option('-l', '--lines', default=sys.maxint)
@click.argument('path')
def migrate(path, lines):
    from . import navet
    try:
        navet.migrate(path, lines)
    except:
        sys.exit(1)
    sys.exit(0)

