=========
Internals
=========

Host package
------------

This component runs on the computer that will serve the DHCP requests and act as a seed for the client computers in the network. The software parses the configuration files in the environment and then renders the final configuration file for various components from the parsed values and the template configuration files present in the package's assets/tpls directory. These parsed configuration files are then written to the out/ directory inside the environment. The software also generates torrent metadata for all the folders present in the oss/ directory.

External components that run on the host include:

* **Transmission**
    | For every sub-directory in the oss/ directory, a torrent file is created with the help of transmission-create binary and placed in the environment's out/torrents directory.
    | Transmission-daemon acts as the seeder for all the torrents.

* **bsdtar**
    | Because client computers can unpack RAM disks in their early phase of boot, the torrents metadata is packed into a RAM disk on the host and is unpacked by the client computers on booting the Phase-1 Linux system.
    | bsdtar is programatically used to pack the client configuration and torrent metadata into a RAM disk.

* **Dnsmasq**
    | Dnsmasq provides both a DHCP server and a TFTP server.
    | The DHCP server capability is used to prepare the client computers to start downloading the Phase-1 Linux system and torrent metadata from the TFTP server.
    | The TFTP server serves the Phase-1 Linux system on the TFTP protocol widely used by most PXE implementations.

* **Hefur**
    | Both DHT and LPD are prone to slow start or may not work at all.
    | Hefur is a simple RAM-only torrent tracker which is used to accelerate the discovery of seeds/peers on the network.

An overview of the BootTorrent starting process is as follows:

1. Parse environment configuration files.
2. Write configuration files for external components into out/ directory.
3. Generate and pack the torrent metadata.
4. Start the external components with final configuration settings.
5. Standby and serve requests as they come.

Client Package
--------------

This component (also called Phase-1 Linux system), which is downloaded via TFTP and runs on the client computers, is a 32-bit x86 OS and is based on SliTaz Linux distribution. Bitness of 32-bit was chosen to maximize compatibility with older hardware that may not be able to run 64-bit x86_64/AMD64 binaries.

The included packages are:

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

Interaction
-----------

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

