# -*- coding: utf-8 -*-

"""Main module."""
from jinja2 import Template
import os
import signal
import subprocess
import tempfile


class BootTorrent:
    def __init__(self, config, wd):
        self.config = config
        self.wd = wd

    def sigint_handler(self, signal, frame):
        t = subprocess.call(["kill", "-9", str(self.dnsmasqpid)])
        exit()

    def start(self):
        """
        To start the DHCP + TFTP + Torrent Seed with the arguments received in config.
        """
        signal.signal(signal.SIGINT, self.sigint_handler)
        assetsdir = os.path.dirname(__file__) + "/assets"
        aria2seedtpl = open(assetsdir+'/tpls/aria2seed.conf.tpl', 'r').read()
        aria2confseed = Template(aria2seedtpl).render(**self.config['aria2']['seed'])
        aria2clienttpl = open(assetsdir+'/tpls/aria2client.conf.tpl', 'r').read()
        aria2confclient = Template(aria2clienttpl).render(**self.config['aria2']['client'])
        # TODO: launch aria2 with these parameters
        dnsmasqconftpl = open(assetsdir+'/tpls/dnsmasq.conf.tpl', 'r').read()
        self.config['dnsmasq']['dhcp_leasefile'] = 'dnsmasq.leases'
        self.config['dnsmasq']['ph1'] = assetsdir+'/ph1'
        dnsmasqconf = Template(dnsmasqconftpl).render(**self.config['dnsmasq'])
        with tempfile.TemporaryDirectory() as tdir:
            dnsmasqconffile = open(os.path.join(tdir, 'dnsmasq.conf'), 'w')
            dnsmasqconffile.write(dnsmasqconf)
            dnsmasqconffile.close()
            dnsmasqprocess = subprocess.Popen(
                    ['dnsmasq', '-C', os.path.join(tdir, "dnsmasq.conf")],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
            self.dnsmasqpid = dnsmasqprocess.pid
            while not dnsmasqprocess.poll():
                for line in dnsmasqprocess.stdout:
                    print("dnsmasq: " + line.decode())
