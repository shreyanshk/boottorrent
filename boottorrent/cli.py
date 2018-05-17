# -*- coding: utf-8 -*-

"""Console script for boottorrent."""
import click
from distutils.dir_util import copy_tree
import os
import sys
import pkg_resources


@click.group()
class main:
    pass


@click.command()
@click.argument('name')
def init(name):
    """Initialize an empty project."""
    click.echo("I'll initialize an empty project.")
    base = pkg_resources.resource_filename('boottorrent', 'assets/skel/config.yaml')
    base = os.path.dirname(base)
    nfolder = os.path.join(os.getcwd(), name)
    copy_tree(base, nfolder)


@click.command()
def start(args=None):
    """Bring the system up and running."""
    click.echo("I'll run the services.")


@click.command()
def stop(args=None):
    """Shutdown the running processes."""
    click.echo("I'll shutdown the services.")


main.add_command(init)
main.add_command(start)
main.add_command(stop)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
