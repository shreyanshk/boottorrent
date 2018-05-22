# -*- coding: utf-8 -*-

"""Main module."""
from distutils.dir_util import copy_tree
from jinja2 import Template
import os
import pathlib
import yaml
import shutil
import signal
import subprocess


class BootTorrent:
    def __init__(self, config, wd):
        self.config = config
        self.wd = wd
        self.assets = os.path.dirname(__file__) + "/assets"

    def sigint_handler(self, signal, frame):
        subprocess.call(["kill", "-9", str(self.dnsmasqpid)])
        exit()

    def start(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        self.recreate_output_dir()
        self.configure_dnsmasq()
        self.generate_torrents()
        self.generate_initrd()
        # self.configure_torrent_seed
        self.start_processes()

    def configure_dnsmasq(self):
        self.config['dnsmasq']['dhcp_leasefile'] = (
                self.wd
                + '/out/dnsmasq/dnsmasq.leases'
                )
        self.config['dnsmasq']['ph1'] = self.wd+'/out/dnsmasq/ph1'
        self.config['dnsmasq']['enable_tftp'] = True
        with open(self.assets+'/tpls/dnsmasq.conf.tpl', 'r') as dnsmasqtpl:
            data = dnsmasqtpl.read()
            dnsmasqconf = Template(data).render(**self.config['dnsmasq'])
        with open(self.wd+'/out/dnsmasq/dnsmasq.conf', 'w') as dnsmasqfile:
            dnsmasqfile.write(dnsmasqconf)

    def start_processes(self):
        dnsmasqprocess = subprocess.Popen(
                ['dnsmasq', '-C', self.wd+'/out/dnsmasq/dnsmasq.conf'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                )
        self.dnsmasqpid = dnsmasqprocess.pid
        while not dnsmasqprocess.poll():
            for line in dnsmasqprocess.stdout:
                print("dnsmasq: " + line.decode())

    def generate_torrents(self):
        oss = self.config['boottorrent']['display_oss']
        oslist = []
        for os in oss:
            filename = self.wd + '/out/torrents/' + os + '.torrent'
            p = subprocess.Popen(
                    [
                        'transmission-create',
                        self.wd + '/oss' + os,
                        '-o', filename,
                        ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                )
            p.wait()
            oslist.append(os)
            shutil.copyfile(
                    self.wd+'/oss/'+os+'/config.yaml',
                    self.wd+'/out/torrents/'+os+'.yaml'
                    )
            for line in p.stdout:
                print("transmission: " + line.decode())
        with open(self.wd + '/out/torrents/list.yaml', 'w') as f:
            f.write(yaml.dump(oslist))

    def generate_initrd(self):
        t = subprocess.Popen([
            'bsdtar',
            '-c', '--format', 'newc', '--lzma',
            '-f', self.wd+'/out/dnsmasq/ph1/torrents.gz',
            '-C', self.wd+'/out',
            'torrents',
            ])
        t.wait()

    def recreate_output_dir(self):
        shutil.rmtree(self.wd + "/out", ignore_errors=True)
        pathlib.Path.mkdir(
                pathlib.Path(self.wd + "/out/dnsmasq"),
                parents=True,
                exist_ok=False,
                )
        copy_tree(self.assets+"/ph1", self.wd + "/out/dnsmasq/ph1")
        pathlib.Path.mkdir(
                pathlib.Path(self.wd + "/out/torrents"),
                parents=True,
                exist_ok=False,
                )
        pathlib.Path.mkdir(
                pathlib.Path(self.wd + "/out/transmission"),
                parents=True,
                exist_ok=False,
                )
