Use cases
=========

1. Kexec-ing Linux on computers
-------------------------------

A group of clustered distributed nodes can possibly have no permanent storage space and only a processor, RAM and network connectivity if the data to process can be readily obtained via the connected network and can be completely stored in the RAM. This scenario is present when the ratio of computation done to memory required is high. Such cases can be subset of Big data processing and Machine Learning on distributed computers.
In this case, one computer on the network is arbitrarily designated as ‘master’ node and other nodes as ‘nodes’. It’s not necessary that these two types of nodes have similar hardware.

Actors
~~~~~~

**Node**

The computer will load and run the bootstrap operating system obtained via conventional network boot. It’ll also execute the final image provided by the torrent client.
It will be multistage:

1. Downloading bootstrap image via TFTP
2. Execute the torrent client
3. Download final OS image(kernel + rootfs) via torrent
4. Kexec the downloaded kernel.

It will be responsible for doing the actual computation on data obtained via out-of-band communication after the ‘kexec’ step.

**Master**

The computer will have BootTorrent installed as a package. Calling the binary/script inside the correct directory will allow managing the instance of BootTorrent configuration in the directory (similar to how Ansible works). The computer will be executing three processes handling different tasks. They may be executed either directly on the hardware or in containers.

* **DHCP server**
    For providing IP to nodes along with flags (as listed at https://tools.ietf.org/html/rfc2132 , titled: DHCP Options and BOOTP Vendor Extensions)

* **TFTP server**
    Will respond to TFTP requests of bootstrap image on the network.

* **Torrent Seed**
    Will seed the final image to be executed on the worker machines.

**Maintainer** (Human actor)

The person responsible for managing the ‘master’ computer as well as tasked with both maintaining a repository of configuration (a folder with all the files and configuration required to bring up the servers) and the execution of the servers.

Actions available:

* **Start**: starts the processes
* **Stop**: stops the processes

**User** (Human actor, optional)

If a person is attending a computer executing BootTorrent, then the person can have more options available. The person who will be using the ‘node’ computers can provide appropriate input to it.
Actions available:

* Power On/Off the node
* Select the OS

2. Booting a VM
---------------

In certain cases there is a need to start a VM instance on the clients, such as to run Operating Systems that cannot load via Kexec-ing. For example: DOS, Windows etc. In such cases the client will download the files and launch the Hypervisor like Qemu.
Another advantage of loading a VM rather than Kexec-ing is that it becomes possible to silently seed the downloaded OS to other computers on the network indefinitely in the background as long as electricity is supplied. This means that other computers on the network that are booting in future will have the option to download the OS from multiple sources together which can give significantly faster download speeds.

Actors
~~~~~~

**Node**

The computer will load and run the bootstrap operating system obtained via conventional network boot. Then the OS files will be downloaded via torrent with the torrent client running in the background and finally proceeded by executing a binary such as Qemu to start the OS.

It will be multistage:

1. Downloading bootstrap image via TFTP
2. Execute the GUI client to obtain input
3. Execute the torrent client in the background
4. Download final OS image(config + image + binaries) via torrent
5. Launch the configured binary

**Master**

The computer will have BootTorrent installed as a package. Calling the binary/script inside the correct directory will allow managing the instance of BootTorrent configuration in the directory (similar to how Ansible works). The computer will be executing three processes handling different tasks. They may be executed either directly on the hardware or in containers.

* **DHCP server**
    For providing IP to nodes along with flags (as listed at https://tools.ietf.org/html/rfc2132 , titled: DHCP Options and BOOTP Vendor Extensions)

* **TFTP server**
    Will respond to TFTP requests of bootstrap image on the network.

* **Torrent Seed**
    Will seed the final image to be executed on the worker machines.

**Maintainer** (Human actor)

The person responsible for managing the ‘master’ computer as well as tasked with both maintaining a repository of configuration (a folder with all the files and configuration required to bring up the servers) and the execution of the servers.

Actions available:

* **Start**: starts the processes
* **Stop**: stops the processes

**User** (Human actor, optional)

If a person is attending a computer executing BootTorrent, then the person can have more options available. The person who will be using the ‘node’ computers can provide appropriate input to it.
Actions available:

* Power On/Off the node
* Select the OS
