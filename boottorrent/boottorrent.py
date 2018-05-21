# -*- coding: utf-8 -*-

"""Main module."""
from jinja2 import Template
import os
import subprocess
import tempfile


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
    assetsdir = os.path.dirname(__file__) + "/assets"
    aria2seedtpl = open(assetsdir+'/tpls/aria2seed.conf.tpl', 'r').read()
    aria2confseed = Template(aria2seedtpl).render(**config['aria2']['seed'])
    aria2clienttpl = open(assetsdir+'/tpls/aria2client.conf.tpl', 'r').read()
    aria2confclient = Template(aria2clienttpl).render(**config['aria2']['client'])
    # TODO: launch aria2 with these parameters
    dnsmasqconftpl = open(assetsdir+'/tpls/dnsmasq.conf.tpl', 'r').read()
    config['dnsmasq']['dhcp_leasefile'] = 'dnsmasq.leases'
    config['dnsmasq']['assets'] = assetsdir+'/ph1'
    dnsmasqconf = Template(dnsmasqconftpl).render(**config['dnsmasq'])
    with tempfile.TemporaryDirectory() as tdir:
        dnsmasqconffile = open(os.path.join(tdir, 'dnsmasq.conf'), 'w')
        dnsmasqconffile.write(dnsmasqconf)
        dnsmasqconffile.close()
        dnsmasq = subprocess.Popen(
                ['dnsmasq', '-C', os.path.join(tdir, "dnsmasq.conf")],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        while True:
            for line in dnsmasq.stdout:
                print("dnsmasq: " + line.decode())


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
