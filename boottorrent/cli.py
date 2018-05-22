# -*- coding: utf-8 -*-

"""Console script for boottorrent."""
from boottorrent import BootTorrent
import click
from distutils.dir_util import copy_tree
import os
import pathlib
import sys
import yaml


@click.group()
class main:
    pass


@click.command()
@click.argument('name')
def init(name):
    """Initialize an new project."""
    base = os.path.dirname(__file__) + '/assets/skel'
    nfolder = os.getcwd() + '/' + name
    copy_tree(base, nfolder)


@click.command()
def start():
    """Bring the system up and running."""
    wd = os.getcwd()
    cfgfilepath = wd + '/Boottorrent.yaml'
    if pathlib.Path(cfgfilepath).exists():
        if not os.access(wd, os.W_OK):
            click.echo(
                    "Error: Unable to create intermediate files "
                    "as current directory is not writable. "
                    "Hence, cannot continue."
                    )
            exit()
        with open(cfgfilepath, 'r') as cfgfile:
            cfg = yaml.load(cfgfile)
        bt = BootTorrent(cfg, wd)
        bt.start()
    else:
        click.echo("Error: can't find suitable configuration file in this directory.")
        click.echo("Are you in the right directory?")
        click.echo("Supported filename is: Boottorrent.yaml")
        exit()


@click.command()
def stop(args=None):
    """Shutdown the running processes."""
    click.echo("I'll shutdown the services.")


main.add_command(init)
main.add_command(start)
main.add_command(stop)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
