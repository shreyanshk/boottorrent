# -*- coding: utf-8 -*-

"""Main module."""
from jinja2 import Template
import pkg_resources


def start(config, wd):
    """
    To start the DHCP + TFTP + Torrent Seed with the arguments received in config.

    Parameters
    ----------
    config : dict
        Parameters that will be passed to the processes of various services.
    wd : str
        Path of the base folder of the configuration.
    """
    aria2confseed = pkg_resources.resource_string(
            'boottorrent',
            'assets/tpls/aria2seed.conf.tpl'
            ).decode()
    aria2confseed = Template(aria2confseed).render(**config['aria2']['seed'])
    aria2confclient = pkg_resources.resource_string(
            "boottorrent",
            "assets/tpls/aria2client.conf.tpl"
            ).decode()
    aria2confclient = Template(aria2confclient).render(**config['aria2']['client'])
    # TODO: launch aria2 with these parameters
    dnsmasqconf = pkg_resources.resource_string(
            'boottorrent',
            'assets/tpls/dnsmasq.conf.tpl'
            ).decode()
    dnsmasqconf = Template(dnsmasqconf).render(**config['dnsmasq'])
    # TODO: launch dnsmasq with these parameters


def stop(config, wd):
    """
    To stop the DHCP + TFTP + Torrent seed that were launched.

    Parameters
    ----------
    config : dict
        Parameters that will be passed to the processes of various services.
    wd : str
        Path of the base folder of the configuration.
    """
    pass
