# -*- coding: utf-8 -*-

"""Main module."""
from distutils.dir_util import copy_tree
from jinja2 import Template
import json
import os
import pathlib
import queue
import requests
import shutil
import signal
import subprocess
import threading
import time
import yaml


class BootTorrent:
    def __init__(self, config, wd):
        """Initialize a new instance

        Parameters
        ----------
        config : dict
            Dictionary generated from parsing BootTorrent.yaml

        wd : str
            Working directory of the command where BootTorrent.yaml is found
        """
        # path to assets/ folder
        self.assets = os.path.dirname(__file__) + "/assets"
        self.config = config
        # This is the output queue where external
        # components (transmission, dnamasq, opentracker) send their stdout.
        self.output = queue.Queue()
        # store handles to threads and processes
        self.process = dict({})
        self.threads = dict({})
        self.wd = wd

    def sigint_handler(self, signal, frame):
        """Handle system signals such as Ctrl+C (SIGINT)
        We handle only SIGINT for now
        Check https://docs.python.org/3/library/signal.html
        for information on the parameters passed

        Parameters
        ----------
        signal
            Signal as it was received
        frame
            Current stack frame
        """
        print('Attempting to terminate the processes...')
        for _, process in self.process.items():
            process.terminate()
        # Putting None ends the output thread
        self.output.put(None)

    def start(self):
        """
        Start the process from creation of out/ directory to
        starting the processes
        """
        # Attach signal handler
        signal.signal(signal.SIGINT, self.sigint_handler)
        # Setup the configurations for external components
        self.recreate_output_dir()
        self.configure_dnsmasq()
        self.generate_torrents()
        self.generate_client_config()
        self.generate_initrd()
        self.configure_transmission_host()

        # Launching the processes
        # (in another thread so as to not block main thread)
        t_thread = threading.Thread(
                target=self.start_process_transmission,
                )
        self.threads['transmission'] = t_thread
        d_thread = threading.Thread(
                target=self.start_process_dnsmasq,
                )
        self.threads['dnsmasq'] = d_thread

        if self.config['opentracker']['enable']:
            h_thread = threading.Thread(
                    target=self.start_process_opentracker,
                    )
            self.threads['opentracker'] = h_thread

        o_thread = threading.Thread(
                target=self.display_output,
                )
        self.threads['output'] = o_thread

        for _, val in self.threads.items():
            val.start()

        # wait for the transmission process to start and
        # initialize before adding torrents
        time.sleep(3)
        self.add_generated_torrents()

        # wait for threads to finish before exiting
        for _, val in self.threads.items():
            val.join()

    def display_output(self):
        """Function to display the output on the user console"""
        while True:
            # Set as blocking because the function is launched as a thread.
            line = self.output.get(block=True, timeout=None)
            if line is None:
                break
            print(line, end="")
            self.output.task_done()

    def add_generated_torrents(self):
        """
        Function to add the generated .torrent files
        to the Transmission process.
        """
        port = self.config['transmission']['rpc_port']
        # get X-Transmission-Session-Id; To make torrent-add request later
        # Transmission's security mechanism to avoid CSRF
        text = requests.get(f"http://localhost:{port}/transmission/rpc").text
        csrftoken = text[522:570]
        for os in self.config['boottorrent']['display_oss']:  # noqa
            args = {
                    'paused': False,
                    'download-dir': f"{self.wd}/oss",
                    'filename': f"{self.wd}/out/torrents/{os}.torrent",
                    }
            # adding torrent file now, see
            # https://trac.transmissionbt.com/browser/branches/1.7x/doc/rpc-spec.txt
            # for API details
            req = requests.post(
                    f"http://localhost:{port}/transmission/rpc",
                    data=json.dumps({
                        "method": "torrent-add",
                        "arguments": args,
                        }),
                    headers={
                        'X-Transmission-Session-Id': csrftoken,
                        }
                    )
            if req.status_code == 200:
                self.output.put(f"TRANSMISSION: Added torrent for {os}.\n")

    def configure_dnsmasq(self):
        """Render dnsmasq.conf.tpl according to the configuration."""
        # Lease file is used to store what IP is given to which client
        self.config['dnsmasq']['dhcp_leasefile'] = (
                f"{self.wd}/out/dnsmasq/dnsmasq.leases"
                )
        # Set the location where the Phase 1 bootloader files can be found
        self.config['dnsmasq']['ph1'] = f'{self.wd}/out/dnsmasq/ph1'
        with open(
                f'{self.assets}/tpls/dnsmasq.conf.tpl',
                'r', encoding='utf-8'
                ) as dnsmasqtpl:
            data = dnsmasqtpl.read()
            dnsmasqconf = Template(data).render(**self.config['dnsmasq'])
        with open(
                self.wd+'/out/dnsmasq/dnsmasq.conf',
                'w', encoding='utf-8'
                ) as dnsmasqfile:
            dnsmasqfile.write(dnsmasqconf)  # write config file

    def configure_transmission_host(self):
        """Render settings.json file according to configuration"""
        # location where the transmission process can find files
        self.config['transmission']['osdir'] = f"{self.wd}/oss"
        with open(
                f"{self.assets}/tpls/transmission.json.tpl",
                'r', encoding='utf-8'
                ) as f:
            data = f.read()
            transmissionconf = Template(data).render(
                    **self.config['transmission']
                    )
        with open(
                f"{self.wd}/out/transmission/settings.json",
                'w', encoding='utf-8'
                ) as f:
            f.write(transmissionconf)  # write config

    def start_process_dnsmasq(self):
        """Start the Dnsmasq process"""
        process = subprocess.Popen(
                ['dnsmasq', '-C', f'{self.wd}/out/dnsmasq/dnsmasq.conf'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                )
        self.process['dnsmasq'] = process
        for line in process.stdout:
            self.output.put(f"DNSMASQ: {line}")

    def start_process_opentracker(self):
        """Start the Opentracker process"""
        process = subprocess.Popen(
                [
                    "opentracker",
                    "-p", str(self.config['opentracker']['port']),
                    ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                )
        self.process['opentracker'] = process
        for line in process.stdout:
            self.output.put(f"OPENTRACKER: {line}")

    def start_process_transmission(self):
        """Start the Transmissio process"""
        process = subprocess.Popen(
                [
                    'transmission-daemon',
                    '-f', '-g',  # Stay in foreground, do not fork
                    f'{self.wd}/out/transmission',
                    ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                )
        self.process['transmission'] = process
        for line in process.stdout:
            self.output.put(f"TRANSMISSION: {line}")

    def generate_torrents(self):
        """
        Function to generate torrents for the folders in oss/ directory.
        """
        if self.config['opentracker']['enable']:
            opentracker = True
            try:
                host_ip = self.config['boottorrent']['host_ip']
                port = self.config['opentracker']['port']
            except KeyError:
                print("Please check configuration!")
                print("Missing host IP or Opentracker port.")
                exit()
        else:
            opentracker = False
        oss = self.config['boottorrent']['display_oss']
        # generating torrents now
        for os in oss:  # noqa
            filename = f"{self.wd}/out/torrents/{os}.torrent"
            cmd = [
                    "transmission-create",
                    f"{self.wd}/oss/{os}",  # folder for which to generate
                    "-o", filename,  # where should the files be placed
                    ]
            if opentracker:
                # add Opentracker as external tracker, if enabled
                cmd.extend(["-t", f"http://{host_ip}:{port}/announce"])
            p = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )
            p.wait()
            for line in p.stdout:
                self.output.put(f"TRANSMISSION-CREATE: {line}\n")

    def generate_client_config(self):
        """
        Generate the configuration files that are transferred to the clients.
        These files include the Boottorrent.yaml file as is and a squashed
        config.yaml file containing the config for all displayed OSs.
        """
        shutil.copyfile(
            f"{self.wd}/Boottorrent.yaml",
            f"{self.wd}/out/torrents/Boottorrent.yaml",
            )
        config = dict()
        for os in self.config['boottorrent']['display_oss']:  # noqa
            osconfig = open(
                    f"{self.wd}/oss/{os}/config.yaml",
                    "r", encoding='utf-8'
                    ).read()
            config[os] = yaml.load(osconfig)
        configcontent = yaml.dump(config)
        with open(
                f"{self.wd}/out/torrents/configs.yaml",
                "w", encoding='utf-8'
                ) as f:
            f.write(configcontent)

    def generate_initrd(self):
        """Generate torrents.gz file from the out/torrents folder
        which is then transferred to the clients.
        """
        t = subprocess.Popen([
            'bsdtar',
            '-c', '--format', 'newc', '--lzma',
            '-f', self.wd+'/out/dnsmasq/ph1/torrents.gz',
            '-C', self.wd+'/out',
            'torrents',
            ])
        t.wait()

    def recreate_output_dir(self):
        """Creates the out/ directory.
        On every invocation, out/ directory is recreated
        because configuration may have changed and we may
        need to update.
        """
        # remove stuff present already
        shutil.rmtree(self.wd + "/out", ignore_errors=True)
        # make directory structure
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
