# -*- coding: utf-8 -*-

"""Console script for boottorrent."""
from boottorrent import BootTorrent, __version__
from distutils.dir_util import copy_tree
import os
import pathlib
import shutil
import sys
import yaml


def parse_args():
    arg = sys.argv[1:]
    argl = len(arg)
    if argl == 0:
        print_help()
    elif argl == 1:
        if arg[0] == "--help":
            print_help()
        elif arg[0] == "start":
            start()
        elif arg[0] == "version":
            version()
        else:
            print("Invalid command")
            print_help()
    elif argl == 2:
        if arg[0] == "init":
            init(arg[1])
        else:
            print("Invalid command")
            print_help()


def print_help():
    print("""
    Usage: boottorrent [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      init     Initialize an new project.
      start    Bring the system up and running.
      version  Display the version number
    """)


def init(name):
    """Initialize an new project."""
    base = os.path.dirname(__file__) + '/assets/skel'
    nfolder = os.getcwd() + '/' + name
    copy_tree(base, nfolder)


def start():
    """Bring the system up and running."""
    wd = os.getcwd()
    cfgfilepath = wd + '/Boottorrent.yaml'
    if pathlib.Path(cfgfilepath).exists():
        if not os.access(wd, os.W_OK):
            print(
                    "Error: Unable to create intermediate files "
                    "as current directory is not writable.\n"
                    "Aborting!"
                    )
            return
        with open(cfgfilepath, 'r', encoding='utf-8') as cfgfile:
            cfg = yaml.load(cfgfile)
            valid = verify_config_v0(cfg, wd)
            if not valid:
                return False
        bt = BootTorrent(cfg, wd)
        bt.start()
    else:
        print(
            "Error: can't find Boottorrent.yaml in this directory.\n"
            "Are you in correct directory?"
        )


def version():
    """Display the version number"""
    print(f"BootTorrent {__version__}")


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
        return False
    if type(cfg) is not dict:
        err("invalid configuration.", "check configuration.")
        return False
    sections = [
            'aria2',
            'boottorrent',
            'dnsmasq',
            'opentracker',
            ]
    for section in sections:
        s = cfg.get(section, None)
        if not s:
            err(f"Section '{section}' not found.",
                "check your configuration.")
            return False
        if type(s) is not dict:
            err(f"invalid value for '{section}'.",
                "check it's value.")
            return False
    mk_exists = shutil.which("mktorrent")
    if not mk_exists:
        err("mktorrent is not installed.",
            "install it.")
        return False
    # check boottorrent section
    bt = cfg['boottorrent']
    if bt.get('version', "") != 0:
        err("Unsupported version.",
            "use correct version of BootTorrent.")
        return False
    try:
        int(bt['timeout'])
    except KeyError:
        err("timeout not found.", "add timeout value.")
        return False
    except ValueError:
        err("Invalid value for timeout.", "correct it's value.")
        return False
    df = bt.get("default_os", "")
    if len(df) == 0:
        err("default_os not set.", "set correct value.")
        return False
    if type(df) is not str:
        err("incorrect value for default_os", "check it's value.")
        return False
    cts = os.listdir(path=f'{wd}/oss')
    oss = [i for i in cts if os.path.isdir(f"{wd}/oss/{i}")]
    if df not in oss:
        err(f"{df} not found in oss/.", "check default_os value.")
        return False
    try:
        st = int(bt['seed_time'])
        if st < 0:
            err("Negative value for seed_time",
                "correct it's value.")
            return False
    except KeyError:
        err("seed_time not found.", "set it's value.")
        return False
    except ValueError:
        err("Invalid value for seed_time.", "correct it's value.")
        return False
    hi = bt.get("host_ip", "")
    if len(hi) == 0:
        err("host IP not set.", "set host_ip field.")
        return False
    ip = hi.split('.')
    if len(ip) != 4:
        err("invalid host IP.", "correct it's value.")
        return False
    for i in ip:
        try:
            j = int(i)
            if not 0 <= j <= 255:
                err("Invalid host IP.", "correct it's value.")
                return False
        except ValueError:
            err("Invalid host IP.", "correct it's value.")
            return False
    # check dnsmasq section
    dm = cfg['dnsmasq']
    dm_exists = shutil.which("dnsmasq")
    if not dm_exists:
        err("dnsmasq is not installed.", "install dnsmasq.")
        return False
    dhcp = dm.get("enable_dhcp", "")
    if not dhcp:
        t = inf("DHCP server is disabled.")
        if t is False:
            return False
    if type(dhcp) is not bool:
        err("Invalid value for dnsmasq.enable_dhcp",
            "set it to a bool value.")
        return False
    intf = dm.get("interface", "")
    if not intf:
        err("You've not set the interface.",
            "configure a network interface.")
        return False
    dr = dm.get('dhcp_range', "")
    if not dr:
        err("You've not set an IP range for DHCP server."
            "configure it's value.")
        return False
    et = dm.get("enable_tftp", "")
    if not et:
        t = inf("TFTP server is disabled.")
        if t is False:
            return False
    if type(et) is not bool:
        err("Invalid value for dnsmasq.enable_tftp",
            "set it to a bool value.")
        return False
    # check opentracker section
    ot = cfg['opentracker']
    ote = ot.get("enable", "")
    if not ote:
        t = inf("Internal Tracker disabled.", "Consider enabling it.")
        if t is False:
            return False
    if type(ote) is not bool:
        err("Invalid value for opentracker.enable",
            "set it to a bool value.")
        return False
    ot_exists = shutil.which("opentracker")
    if ote and not ot_exists:
        err("Opentracker enabled but not found.",
            "install Opentracker or update configuration.")
        return False
    otp = ot.get("port", "")
    if ote and not otp:
        err("Tracker port not configured.", "configure it's value")
        return False
    try:
        otp = int(otp)
        if not 0 < otp < 65536:
            err("Invalid value for Opentracker port.",
                "correct it's value.")
            return False
    except ValueError:
        err("Invalid value for Opentracker port.", "correct it's value.")
        return False
    # check aria2 section
    a2_exists = shutil.which("aria2c")
    if not a2_exists:
        err("Aria2 not found.", "install Aria2.")
        return False
    a2 = cfg['aria2']
    a2lpd = a2.get("bt_enable_lpd", "")
    if type(a2lpd) is not bool:
        err("Invalid value for aria2.bt_enable_lpd",
            "set it to a bool value.")
        return False
    if not ote and not a2lpd:
        err("You've not enabled any peer discovery mechanism.",
            "Please either enable LPD or Opentracker.")
        return False
    elif not ote and a2lpd:
        t = inf(
            "You've enabled LPD but it is slow and unreliable.",
            "consider enabling Opentracker."
            )
        if t is False:
            return False
    cll = a2.get("console_log_level", "")
    vcll = ['debug', 'info', 'notice', 'warn', 'error']
    if cll not in vcll:
        err("invalid value for Aria2 log level.",
            "correct it's value.")
        return False
    # checking the OS configs.
    friendlynamelist = []
    for osdir in oss:
        cfgfilepath = f"{wd}/oss/{osdir}/config.yaml"
        if not pathlib.Path(cfgfilepath).exists():
            err(f"config.yaml for {osdir} doesn't exist.", "check config.")
            return False
        with open(cfgfilepath, 'r', encoding='utf-8') as f:
            oscfg = yaml.load(f)
            method = oscfg.get("method", None)
            if not method:
                err(f"method for {osdir} not defined.", "define method.")
                return False
            if method not in ['bin', 'kexec', 'bin-qemu-x86_64']:
                err(f"Invalid method for {osdir}.", "check config.")
                return False
            dispname = oscfg.get("dispname", "")
            if dispname == "":
                err(f"display name not set for {osdir}.", "set display name.")
                return False
            if dispname in friendlynamelist:
                err(f"{dispname} found multiple times.", "correct it.")
                return False
            friendlynamelist.append(dispname)
            ospath = f"{wd}/oss/{osdir}"
            if method == 'bin':
                valid = verify_config_v0_method_bin(oscfg, ospath)
                if not valid:
                    return False
            elif method == 'kexec':
                valid = verify_config_v0_method_kexec(oscfg, ospath)
                if not valid:
                    return False
            else:
                valid = verify_config_v0_method_qemu(oscfg, ospath)
                if not valid:
                    return False
    # all checks passed
    return True


def verify_config_v0_method_kexec(oscfg, ospath):
    """Function to verify for method kexec
    """
    kernel = oscfg.get("kernel", "")
    initrd = oscfg.get("initrd", "")
    if kernel == "":
        err(f"kernel not set for {oscfg['dispname']}.", "set it.")
        return False
    if initrd == "":
        err(f"initrd not set for {oscfg['dispname']}.", "set it.")
        return False
    if not pathlib.Path(f"{ospath}/{kernel}").exists():
        err(f"Specified kernel for {oscfg['dispname']} doesn't exists.",
            "correct it.")
        return False
    if not pathlib.Path(f"{ospath}/{initrd}").exists():
        err(f"Specified initrd for {oscfg['dispname']} doesn't exists.",
            "correct it.")
        return False
    return True


def verify_config_v0_method_qemu(oscfg, ospath):
    """Function to verify for method bin-qemu-x86_64
    """
    # nothing to check here
    # leaving stub just in case needed
    return True


def verify_config_v0_method_bin(oscfg, ospath):
    """Function to verify for method bin
    """
    binfile = oscfg.get("bin", "")
    if binfile == "":
        err(f"binary isn't specified for {oscfg['dispname']}.",
            "specify it.")
        return False
    if not pathlib.Path(f"{ospath}/{binfile}").exists():
        err(f"binary for {oscfg['dispname']} not found.", "check it.")
        return False
    return True


def err(err, action):
    print("Error! " + err)
    print("Please " + action)
    return False


def inf(info, rec=None):
    print("Information: " + info)
    if rec:
        print("Recommendation: " + rec)
    print("Continue? (y/n)")
    i = input()
    if i == 'y' or i == 'Y':
        return True
    elif i == 'n' or i == 'N':
        return False
    else:
        print("Error: Invalid input. Aborting!")
        return False


if __name__ == "__main__":
    sys.exit(parse_args())  # pragma: no cover
