BootTorrent - Identified use cases
==================================

Diskless clustered distributed computers (unattended)
-----------------------------------------------------

A group of clustered distributed nodes can have no permanent storage space and only a processor, RAM and network connectivity if the data to process can be readily obtained via the connected network and can be completely stored in the RAM. This scenario is present when the ratio of computation done to memory required is high. Such cases can be subset of Big data processing and Machine Learning on distributed computers.
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

**Maintainer (Human actor)**

The person responsible for managing the ‘master’ computer as well as tasked with both maintaining a repository of configuration (a folder with all the files and configuration required to bring up the servers) and the execution of the servers.

Actions available:

* Start: starts the processes
* Stop: stops the processes


Diskless clustered computers (with human input/attended)
--------------------------------------------------------

A university laboratory can have multiple computers with students wishing to run different distributions/versions of operating systems. They will provide sufficient input to the program executing in the bootstrap image and the program will initiate the download of correct torrent and kexec the downloaded kernel.
Another reason could be that the Lab supervisor want to centrally manage the operating systems. The person can modify the base OS images on his computer and those changes will be reflected to the other computers on their reboot.
In this case the computer managed by the supervisor can be designated as ‘server’ and other computers can be called ‘node’. Only the ‘node’ computer is controlled by the students.

Actors
~~~~~~
**Node**

The computer will load and run the bootstrap operating system obtained via conventional network boot. It’ll also execute the final image provided by the torrent client.

It will be multistage:

1. Downloading bootstrap image via TFTP
2. Execute the GUI client to obtain input
3. Execute the torrent client
4. Download final OS image(kernel + rootfs) via torrent
5. Kexec the downloaded kernel.

**Server**

The computer will have BootTorrent installed as a package. Calling the binary/script inside the correct directory will allow managing the instance of BootTorrent configuration in the directory (similar to how Ansible works). The computer will be executing three processes handling different tasks. They may be executed either directly on the hardware or in containers.

* **DHCP server**
    For providing IP to workers along with flags (as listed at https://tools.ietf.org/html/rfc2132 , titled: DHCP Options and BOOTP Vendor Extensions)

* **TFTP server**
    Will respond to TFTP requests of bootstrap image on the network.

* **Torrent Seed**
    Will seed the final image to be executed on the worker machines.

**Maintainer (Human actor)**

The person responsible for managing the ‘server’ computer as well as tasked with both maintaining a repository of configuration (a folder with all the files and configuration required to bring up the servers) and the execution of the server.

Actions available:

* **Start**: starts the processes

* **Stop**: stops the processes

**User (Human actor)**

The person who will be using the ‘node’ computers and provide appropriate input to it.
Actions available:

* Power On/Off the node
* Select the OS
