=========
Internals
=========

This documents focuses on the implementation details of BootTorrent. General details about the architecture and design can be found `here <https://boottorrent.readthedocs.io/en/latest/architecture.html>`_.

Interface implementation
------------------------

Client configuration interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Approach used**

At power-on, the clients are limited in nature and the only supported protocols are DHCP, TFTP and PXE. So, client boot configuration is provided via DHCP, TFTP and PXE.

**Alternative approaches**

None, our choices are limited by hardware.

`Dnsmasq`_
**********

.. _Dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html

Dnsmasq implements various protocols such as DHCP, BOOTP, PXE and TFTP support. It also includes support via Lua scripting language. Three protocols, DHCP, PXE and TFTP are currently being used in BootTorrent.

**Rationale**

* Implements support for DHCP, PXE and TFTP in a single package.
* Is widely available on most distributions.
* It has low requirements for system resources.

**Alternatives software**

.. (atrent) give links to the alternatives

* ISC DHCP: Heavy, more suitable for large deployments.
* Kea DHCP: Considered experimental.
* udhcpd: Doesn't support PXE or BOOTP

Note: None of the alternatives support TFTP. Choosing any other option means that other external software is required for TFTP.

**Provides**

* Client parameters

`bsdtar`_
*********

.. _bsdtar: https://github.com/libarchive/libarchive

bsdtar is a command line tool for reading and writing archives.

**Approach used**

bsdtar is used to create an ``SVR4 with no CRC (newc)`` type of archive containing additional client parameters and torrent metadata files. The archive created by bsdtar is directly mounted by kernel on the client computer as a standard initrd image.

Note: SliTaz kernel only accepts archives in this format. With custom kernel compilation is possible to support other formats (which are supported by GNU tar) but that is a large compromise in: manageability, build creation times, approachability of project etc.

**Alternative approaches**

1. HTTP server to serve metadata and configuration.
    | Another server process is needed.
    | More system resource usage.
    | Additional logic is required to handle on clients.
2. Network broadcast to serve the metadata and configuration.
    | Require another process on server and client both.
    | Known for using high bandwidth sometimes. See `Broadcast storm <https://en.wikipedia.org/wiki/Broadcast_storm>`_.
    | Are sometimes blocked by network admins, see above.
    | Sometimes the computers are isolated in their own VLANs.
3. mkinitcpio/mkinitramfs etc
    | Needs extra configuration files to work that is avoidable on other approaches.
    | Are geared towards creation of full initrd images. We only need to pack a folder.

**Rationale**

* Archives are usable by clients without any additional software/logic.
* No extra process is created either on server or client.
* No configuration files needed.

**Alternative software**

.. (atrent) give links to the alternatives

* GNU cpio

**Provides**

* Client parameters
* Metadata (P2P)

Initial data provider interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Approach used**

Choices limited to BitTorrent.

**Alternative approaches**

None

`Transmission`_
***************

.. _Transmission: https://transmissionbt.com/

Transmission is a BitTorrent client.

**Rationale**

* Popular and available in most distributions.
* Includes both torrent creation and seeding tools.
* Programmable via API.

**Alternative software**

Many choices available: see `Comparison of BitTorrent clients <https://en.wikipedia.org/wiki/Comparison_of_BitTorrent_clients>`_.

Client data sharing interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Approach used**

Choices limited to BitTorrent.

**Alternative approaches**

None

`Aria2`_
********

.. _Aria2: https://github.com/aria2/aria2

Aria2 is a BitTorrent client.

**Rationale**

* Available as a package in SliTaz distribution.
* Fully configurable via commandline.
* Fully configurable programmatically.

**Alternative software**

.. (atrent) give links to the alternatives

* transmission
* ctorrent-dnh
* qbittorrent
* rtorrent

Operating system loading interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Approach used**

The executable /sbin/getty on client's RAM disk is replaced. The new binary is loaded from initrd during boot process. The binary /sbin/getty (previously: Login manager, now: BootTorrent TUI) is invoked for every console by the init system and has root access.

**Alternative approaches**

* Replace with init
    | System will not load other drivers/software etc. (since init system has been removed)
* Launch with init system.
    | Changes needed to be made in the base image are numerous.

`Golang`_ Terminal User Interface (TUI)
***************************************

.. _Golang: https://golang.org/

Golang is a programming language developed by Google. It can easily create cross platform, portable, static binary executable files.

**Rationale**

* System will load other drivers/software etc because proper init system is present.
* Less invasive. Single file need to be replaced on the base image.
* Avoids dependency management as the binary is static.

**Notes**

* Used `GoCUI framework <https://github.com/jroimartin/gocui>`_ for the creating of CUI.
* Used `YAML v2 library <https://gopkg.in/yaml.v2>`_ to read configuration files which are in YAML.

Host Package
------------

This component runs on the computer that will serve the DHCP requests and act as a seed for the client computers in the network. The software parses the configuration files in the environment and then renders the final configuration file for various components from the parsed values and the template configuration files present in the package's assets/tpls directory. These parsed configuration files are then written to the out/ directory inside the environment. The software also generates torrent metadata for all the folders present in the oss/ directory.

An overview of the BootTorrent starting process is as follows:

1. Parse environment configuration files.
2. Write configuration files for external components into out/ directory.
3. Generate and pack the torrent metadata.
4. Start the external components with final configuration settings.
5. Standby and serve requests as they come.

Core components
~~~~~~~~~~~~~~~

External components that run on the host include:

* **Transmission**
    | For every sub-directory in the oss/ directory, a torrent file is created with the help of transmission-create binary and placed in the environment's out/torrents directory.
    | Transmission-daemon acts as the seeder for all the torrents.

* **bsdtar**
    | Because client computers can unpack RAM disks in their early phase of boot, the torrents metadata is packed into a RAM disk on the host and is unpacked by the client computers on booting the Phase-1 Linux system.
    | bsdtar is programmatically used to pack the client configuration and torrent metadata into a RAM disk.

* **Dnsmasq**
    | Dnsmasq provides both a DHCP server and a TFTP server.
    | The DHCP server capability is used to prepare the client computers to start downloading the Phase-1 Linux system and torrent metadata from the TFTP server.
    | The TFTP server serves the Phase-1 Linux system on the TFTP protocol widely used by most PXE implementations.

Support components
~~~~~~~~~~~~~~~~~~

`Hefur`_
********

.. _Hefur: https://github.com/abique/hefur

Hefur is an in-memory, standalone BitTorrent tracker.

**Rationale**

* It allows fast discovery of other seeds/peers in the network. (Compared to LPD & DHT)
* It doesn't need a database or configuration file.
* Integrated web interface to display statistics for the torrents being served.

**Alternative software**

.. (atrent) give links to the alternatives

* Opentracker
    | No integrated web interface
* Chihaya
    | Written in Golang, no web inteface

`Python-Click`_
***************

.. _Python-Click: http://click.pocoo.org/5/

Click is a Python package for creating command line interfaces in a composable way with little code.

**Rationale**

* It is used to implement the CLI in the package.
* Code and it's documentation are placed together. Avoiding changing at multiple places on code changes.
* It automatically generates CLI documentation from code and it's comments.

**Alternate package**

* docopt
* argparse

`Python-PyYAML`_
****************

.. _Python-PyYAML: https://github.com/yaml/pyyaml

It is a YAML parser and emitter for Python.

**Rationale**

* It is used to parse an BootTorrent environment's YAML files.

`Python-Jinja2`_
****************

.. _Python-Jinja2: http://jinja.pocoo.org/

Jinja2 is a templating engine / processor in Python.

**Rationale**

* External components use configuration files. Jinja2 is used to generate configuration files from templates and data models (such as passed variables, maps etc).

**Alternate packages**

Numerous: Visit `Python's templating documentation <https://wiki.python.org/moin/Templating>`_ for information.

`Python-Requests`_
******************

.. _Python-Requests: http://docs.python-requests.org/en/master/

Requests is an HTTP library for Python.

**Rationale**

* It is used to interact with Transmission's HTTP API to add torrents to it's daemon process.

**Alternate packages**

.. (atrent) give links to the alternatives

* Python-urllib3

Client Package
--------------

This component (also called Phase-1 Linux system), which is downloaded via TFTP and runs on the client computers, is a 32-bit x86 OS and is based on SliTaz Linux distribution. Bitness of 32-bit was chosen to maximize compatibility with older hardware that may not be able to run 64-bit x86_64/AMD64 binaries.

Core components
~~~~~~~~~~~~~~~

.. (atrent) give links to these components' projects

* **Aria2**
    | It is used to download the actual files from the torrent metadata.

* **Kexec-tools**
    | It is used to load any Linux based OS via kexec process.

* **Qemu-x86_64**
    | It is a hypervisor to run user provided non-Linux OS.

* **Xorg**
    | It is used to provide Graphical display capabilities needed by Qemu.

* **BootTorrent TUI**
    | It is used to either accept user input and/or read client configuration and programatically calls above tools as necessary.

An overview of client's process is as follows:

1. PXE on client requests DHCP address.
2. Client receives DHCP address + PXE configuration.
3. Client downloads and executes the PXE Linux loader.
4. Linux loader downloads and executes the Phase-1 Linux kernel and initrd(s).
5. TUI binary is launched by the init system.
6. OS to load is chosed either via user input or configuration.
7. Download of the OS is initiated and saved to RAM.
8. OS is loaded via appropriate method.

Support components
~~~~~~~~~~~~~~~~~~

`GoCUI`_
********

.. _GoCUI: https://github.com/jroimartin/gocui

It is a minimalist Go package for creating console user interfaces.

`Go YAML`_
**********

.. _Go YAML: https://github.com/go-yaml/yaml

It is a YAML parser and emitter for Golang.

Host process at a glance
------------------------

The BootTorrent executable uses env's out/ directory as it's working directory. It is cleaned before every run to remove any stale/old data.

1. Parsing Boottorrent.yaml
    | Boottorrent.yaml is parsed via PyYAML Python library and stored internally by the program into 'config' variable.

2. Write configuration for Dnsmasq.
    | 'dnsmasq' section of 'config' and assets/tpls/dnsmasq.conf.tpl are send to Jinja2 to get final configuration file for Dnsmasq which is then written to env's out/dnsmasq/dnsmasq.conf file.
    | Files for Phase 1 Linux system are also copied to out/dnsmasq/ph1 directory.

3. Generation of torrents.
    | For all the OSs present in the boottorrent.display_oss field, torrent file for individual OS is generated via transmission-create binary and placed into env's out/torrents directory.
    | If Hefur is enabled, it is added as external tracker to the torrents generated.

4. Write configuration for the client TUI.
    | TUI configuration is composed of two YAML files. These two files are parsed on the client to either display a TUI or load an OS.
    | out/torrents/configs.yaml file stores the booting information for the OSs.
    | out/torrents/Boottorrent.yaml file is a copy of env's Boottorrent.yaml file.

5. Generation of initrd carrying the client configuration.
    | Client configuration is transferred to clients via an additional initrd during boot process.
    | SliTaz kernel can unpack 'newc' type of initrd file. So, the env's out/torrents directory (containing torrent metadata + TUI configuration) is packed into a 'newc' archive which is then mounted by the kernel on client during its boot process without any additional software.
    | This new initrd is placed at out/dnsmasq/ph1/torrents.gz location.

6. Write configuration for Transmission.
    | 'transmission' section of the 'config' and assets/tpls/transmission.json.tpl are send to Jinja2 to get final configuration file for Transmission which is then written to env's out/transmission/settings.json file.

At this point, configuration for these components is present in the out/ directory and these processes are ready to be launched.
Note: Hefur doesn't require configuration file and its CLI is simple. So, it's not written.

7. Launch external components on the host.
    | After the configuration(s) is written for components, they are launched and passed the path to their respective configuration.

8. Add generated torrents to Transmission.
    | Torrent metadata present in the out/torrents directory is then added to Transmission via it's Web API.

At this point:

* Dnsmasq is ready to serve any DHCP/TFTP requests.
* Transmission is seeding the torrents.
* Hefur tracker (if enabled) is ready to serve the clients.

So, BootTorrent goes standby and waits for requests to come.

Interactions at a glance
------------------------

Loading of PXE Linux loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a computer starts and PXE boot is enabled in it's BIOS, it will send a DHCP request to any DHCP server on the network and anticipate PXE booting information with the response.
The DHCP protocol provides methods to instruct clients to launch a predefined PXE binary when responding with DHCP requests. These methods are used to launch a PXELinux loader (assets/ph1/pxelinux.0) on clients to prepare for the launch of the Phase 1 Linux system. Dnsmasq is configured to utilize these methods.

Loading of Phase 1 Linux kernel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once PXELinux loader is running, it will download it's configuration file (pxelinux.cfg, which is static and doesn't passes via Jinja2) from the TFTP server and read the details on how to load the Phase 1 Linux system.
It will then download a total of 4 files (again via TFTP):

* bzImage
    | The Linux kernel

* rootfs.gz
    | SliTaz initrd containing all the drivers, programs, utilities ... etc

* diff.gz
    | Contains the changes we want over rootfs.gz which are then overlaid on rootfs.gz
    | Currently contains only BootTorrent TUI, replacing /sbin/getty binary for minimal changes to rootfs.gz

* torrents.gz
    | Contains the torrent metadata + the TUI configuration

Once these files are downloaded, the PXELinux loader loads the Kernel.

Loading of the TUI
~~~~~~~~~~~~~~~~~~

The init system on the SliTaz image then attempts to load /sbin/getty binary which launches the TUI on client.

The below diagram illustrates how the booting process on client takes place.

.. seqdiag::

    seqdiag {
        host.DHCP; client.PXE; host.TFTP; client.LL; client.Ph1; client.TUI;
        client.PXE -> host.DHCP [label = "Req. DHCP address"]
        client.PXE <- host.DHCP [label = "IP Addr + PXE Config"]
        client.PXE -> host.TFTP [label = "Req. PXE Linux loader binary"]
        client.PXE <- host.TFTP [label = "Linux loader binary"]
        client.PXE -> client.LL [label = "Start Linux loader", leftnote = "PXE exits"]
        client.LL -> host.TFTP [label = "Req Kernel + initrd(s)"]
        client.LL <- host.TFTP [label = "Kernel + initrd(s)"]
        client.LL -> client.Ph1 [label = "Execute Phase-1 Kernel", leftnote = "Linux loader exits"]
        client.Ph1 -> client.TUI [label = "Init launches TUI"]
    }

[If you're having trouble read the image, view it at full resolution by right clicking it and opening it in another tab.]

The nodes in this chart are as follows:

+---------------+-----------------------------------------------+
|Name           |Description                                    |
+---------------+-----------------------------------------------+
|host.DHCP      |DHCP server running on the host.               |
+---------------+-----------------------------------------------+
|client.PXE     |Portable execution environment on the client.  |
+---------------+-----------------------------------------------+
|host.TFTP      |TFTP server running on the host                |
+---------------+-----------------------------------------------+
|client.LL      |PXE Linux loader running on the client         |
+---------------+-----------------------------------------------+
|client.Ph1     |Phase 1 Linux system running on client         |
+---------------+-----------------------------------------------+
|client.TUI     |BootTorrent Terminal user interface            |
+---------------+-----------------------------------------------+

