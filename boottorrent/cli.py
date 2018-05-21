# -*- coding: utf-8 -*-

"""Console script for boottorrent."""
from boottorrent import BootTorrent
import click
from distutils.dir_util import copy_tree
import os
import pkg_resources
import sys
import yaml


@click.group()
class main:
    pass


@click.command()
@click.argument('name')
def init(name):
    """Initialize an new project."""
    base = pkg_resources.resource_filename('boottorrent', 'assets/skel/config.yaml')
    base = os.path.dirname(base)
    nfolder = os.path.join(os.getcwd(), name)
    copy_tree(base, nfolder)


@click.command()
def start():
    """Bring the system up and running."""
    pdir = os.getcwd()
    config = open(os.path.join(pdir, 'config.yaml'), 'r')
    pconfig = yaml.load(config)
    config.close()
    bt = BootTorrent(pconfig, pdir)
    bt.start()


@click.command()
def stop(args=None):
    """Shutdown the running processes."""
    click.echo("I'll shutdown the services.")


main.add_command(init)
main.add_command(start)
main.add_command(stop)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
