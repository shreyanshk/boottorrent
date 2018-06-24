The ``Boottorrent.yaml`` file present in an environment is used to configure the internal working of BootTorrent. Available sections and parameters are as follows:

**Section: boottorrent**

This section stores configurations parameters that are related to the working of core system.

* version
    | type: int, required
    | Handle backward/forward compatibility.

* display_oss
    | type: list of strings, required
    | Operating Systems choices available to clients.
    | Populated with the name of the folders in the oss/ directory.

* timeout
    | type: int, default 30
    | In case of multiple OSs, BootTorrent waits this long (seconds) for user input before booting default OS.
    | If this value is 0, then the default OS will be started as soon as possible.
    | If this value is negative, then the timer is disabled and BootTorrent will wait forever for user input.

* default_os
    | type: string, required if timeout is set
    | The default choice in case of no input from user.
    | Must be a value from the display_oss list.

* seed_time [WIP]
    | type: int, default 30, required
    | BootTorrent seeds downloaded OS for at least this long (seconds) before loading.
    | Ideal value: (image size / client interface speed) + BootTorrent boot time on client.
    | If this value is 0 or negative, BootTorrent will load the OS as soon as possible.

* host_ip
    | type: string, required
    | IPv4 of the host as visible to the clients.

**Section: dnsmasq**

Dnsmasq is used to provide a DHCP server and a TFTP server for the purpose of network boot to the clients.
The parameters in this sections have one-to-one correlation with those of Dnsmasq. When in doubt, please visit it's official `documentation`_.

.. _`documentation`: http://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html

* enable_dhcp
    | type: boolean, required
    | Enable the build-in DHCP server

* user
    | type: string
    | Switch to this user when dropping root privileges.

* interface
    | type: string, required, default eth0
    | Interface on which the DHCP server should run.

* bind_interfaces
    | type: boolean, default: true
    | Useful when the interface can go up/down or change addresses during runtime.

* dhcp_range
    | type: string, default: "192.168.1.50,192.168.1.150,12h"
    | Range of IPs the DHCP server will provide with the lease time for each IP.

* enable_tftp
    | type: boolean, default: true
    | Enable build-in TFTP server.

**Section: opentracker**

Opentracker is a BitTorrent peer tracker that is designed to be fast and low on resource usage. It is used to accelerate peer/seed discovery in the network.
Enabling Opentracker requires that you set host_ip field as well.

* enable
    | type: boolean, default: true
    | Used to enable/disable the tracker

* port
    | type: int, required if Opentracker is enabled, default: 10001
    | Port on which to run the tracker.

**Section: transmission**

An instance of Transmission is launched on the host to server the OS files to the clients via torrents.

* rpc_port
    | type: int, required, default: 9091
    | The port where Transmission will provide it's WebUI and API.

* lpd_enabled
    | type: boolean, required, default: false
    | Local Peer Discovery (LPD) can be enabled if it is not possible to enable Opentracker as a tracker. Though, Opentracker is recommended.
    | Seed/Peer discovery via LPD can be slow or might not work at all.

**Section: aria2**

Aria2 is used on client side to download files via torrents.

* bt_enable_lpd
    | type: boolean, required, default: false
    | Enable LPD on clients.

* check_integrity
    | type: boolean, default: false
    | Additionally verify authenticity of downloaded data on the clients.

* enable_peer_exchange
    | type: boolean, required, default: true
    | Enable Peer Exchange (PEX) protocol. Can improve download speeds if only LPD is enabled.
