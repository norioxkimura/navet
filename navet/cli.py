
import click
import sys

@click.group()
def navet():
    pass

@navet.command()
def version():
    print("navet 0.1")

@navet.command()
@click.argument('path')
def read(path):
    from . import navet
    navet.read(path)
    sys.exit(0)

