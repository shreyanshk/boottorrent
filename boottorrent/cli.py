# -*- coding: utf-8 -*-

"""Console script for boottorrent."""
from boottorrent import BootTorrent, __version__
import click
from distutils.dir_util import copy_tree
import os
import pathlib
import shutil
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
        with open(cfgfilepath, 'r', encoding='utf-8') as cfgfile:
            cfg = yaml.load(cfgfile)
            valid = verify_config_v0(cfg, wd)
            if not valid:
                exit()
        bt = BootTorrent(cfg, wd)
        bt.start()
    else:
        click.echo("Error: can't find Boottorrent.yaml in this directory.")
        click.echo("Are you in the right directory?")
        click.echo("Supported filename is: Boottorrent.yaml")
        exit()


@click.command()
def version(args=None):
    """Display the version number"""
    click.echo(f"BootTorrent {__version__}")


def verify_config_v0(cfg, wd):
    """Function to validate the correctness
    of the configuration
    """
    # 0. Assert existence
    # 1. Assert type
    # 2. Assert value
    if cfg is None:
        err("configuration not found.",
            "make sure you're in correct directory.")
    if type(cfg) is not dict:
        err("invalid configuration.", "check configuration.")
    sections = [
            'aria2',
            'boottorrent',
            'dnsmasq',
            'opentracker',
            'transmission',
            ]
    for section in sections:
        s = cfg.get(section, None)
        if not s:
            err(f"Section '{section}' not found.",
                "check your configuration.")
        if type(s) is not dict:
            err(f"invalid value for '{section}'.",
                "check it's value.")
    # check boottorrent section
    bt = cfg['boottorrent']
    if bt.get('version', "") != 0:
        err("Unsupported version.",
            "use correct version of BootTorrent.")
    try:
        int(bt['timeout'])
    except KeyError:
        err("timeout not found.", "add timeout value.")
    except ValueError:
        err("Invalid value for timeout.", "correct it's value.")
    df = bt.get("default_os", "")
    if len(df) == 0:
        err("default_os not set.", "set correct value.")
    if type(df) is not str:
        err("incorrect value for default_os", "check it's value.")
    cts = os.listdir(path=f'{wd}/oss')
    oss = [i for i in cts if os.path.isdir(f"{wd}/oss/{i}")]
    if df not in oss:
        err(f"{df} not found in oss/.", "check default_os value.")
    try:
        st = int(bt['seed_time'])
        if st < 0:
            err("Negative value for seed_time",
                "correct it's value.")
    except KeyError:
        err("seed_time not found.", "set it's value.")
    except ValueError:
        err("Invalid value for seed_time.", "correct it's value.")
    hi = bt.get("host_ip", "")
    if len(hi) == 0:
        err("host IP not set.", "set host_ip field.")
    ip = hi.split('.')
    if len(ip) != 4:
        err("invalid host IP.", "correct it's value.")
    for i in ip:
        try:
            j = int(i)
            if not 0 <= j <= 255:
                err("Invalid host IP.", "correct it's value.")
        except ValueError:
            err("Invalid host IP.", "correct it's value.")
    # check dnsmasq section
    dm = cfg['dnsmasq']
    dm_exists = shutil.which("dnsmasq")
    if not dm_exists:
        err("dnsmasq is not installed.", "install dnsmasq.")
    dhcp = dm.get("enable_dhcp", "")
    if not dhcp:
        inf("DHCP server is disabled.")
    if type(dhcp) is not bool:
        err("Invalid value for dnsmasq.enable_dhcp",
            "set it to a bool value.")
    intf = dm.get("interface", "")
    if not intf:
        err("You've not set the interface.",
            "configure a network interface.")
    dr = dm.get('dhcp_range', "")
    if not dr:
        err("You've not set an IP range for DHCP server."
            "configure it's value.")
    et = dm.get("enable_tftp", "")
    if not et:
        inf("TFTP server is disabled.")
    if type(et) is not bool:
        err("Invalid value for dnsmasq.enable_tftp",
            "set it to a bool value.")
    # check opentracker section
    ot = cfg['opentracker']
    ote = ot.get("enable", "")
    if not ote:
        inf("Internal Tracker disabled.", "Consider enabling it.")
    if type(ote) is not bool:
        err("Invalid value for opentracker.enable",
            "set it to a bool value.")
    ot_exists = shutil.which("opentracker")
    if ote and not ot_exists:
        err("Opentracker enabled but not found.",
            "install Opentracker or update configuration.")
    otp = ot.get("port", "")
    if ote and not otp:
        err("Tracker port not configured.", "configure it's value")
    try:
        otp = int(otp)
        if not 0 < otp < 65536:
            err("Invalid value for Opentracker port.",
                "correct it's value.")
    except ValueError:
        err("Invalid value for Opentracker port.", "correct it's value.")
    # check transmission section
    tr_exists = shutil.which("transmission-daemon")
    if not tr_exists:
        err("Transmission is not installed.", "install Transmission.")
    tr = cfg['transmission']
    trp = tr.get("rpc_port", "")
    if not trp:
        err("Transmission port not configured.", "configure it's value")
    try:
        trp = int(trp)
        if not 0 < trp < 65536:
            err("Invalid value for Transmission port.",
                "correct it's value.")
    except ValueError:
        err("Invalid value for Transmission port.", "correct it's value.")
    tre = tr.get("lpd_enabled", "")
    if tre and type(tre) is not bool:
        err("Invalid value for transmission.lpd_enabled",
            "set it to a bool value.")
    # check aria2 section
    a2 = cfg['aria2']
    a2lpd = a2.get("bt_enable_lpd", "")
    if type(a2lpd) is not bool:
        err("Invalid value for aria2.bt_enable_lpd",
            "set it to a bool value.")
    if not ote and (not tre or not a2lpd):
        err("You've not enabled any peer discovery mechanism.",
            "Please either enable LPD or Opentracker.")
    elif not ote and tre and a2lpd:
        inf("You've enabled LPD but it is slow and unreliable.",
            "consider enabling Opentracker.")
    cll = a2.get("console_log_level", "")
    vcll = ['debug', 'info', 'notice', 'warn', 'error']
    if cll not in vcll:
        err("invalid value for Aria2 log level.",
            "correct it's value.")
    # all checks passed
    return True


def err(err, action):
    click.echo("Error! " + err)
    click.echo("Please " + action)
    exit()


def inf(info, rec=None):
    click.echo("Information: " + info)
    if rec:
        click.echo("Recommendation: " + rec)
    click.echo("Continue? (y/n)")
    i = input()
    if i == 'y' or i == 'Y':
        return
    elif i == 'n' or i == 'N':
        exit()
    else:
        click.echo("Error: Invalid input. Aborting!")
        exit()


main.add_command(init)
main.add_command(start)
main.add_command(version)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
