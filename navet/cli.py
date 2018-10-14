
import click
import sys

@click.group()
def navet():
    pass

@navet.command()
def version():
    print("navet 0.1")

