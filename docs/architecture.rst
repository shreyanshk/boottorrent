======================
Architectural document
======================

Version: 0, Revision: 0

Last revision date: 15-June-2018

Introduction
------------

The goal of BootTorrent is to enable P2P network boot of computers in a cluster.

This document is written by `Shreyansh Khajanchi`_. Please raise an issue at `Github <https://www.github.com/shreyanshk/boottorrent>`_ to provide feedback on this document.

This document details the architecture for the project BootTorrent submitted to Debian Open source project under Google Summer of Code 2018.

The purpose of this document is to share details of the needs and requirements of the project from a single authoritative place.

The audience for this document is, first and foremost, `Andrea Trentini`_ and `Giovanni Biscuolo`_ for Debian (See the project on the `official Debian website`_), and any open source contributor who wishes to learn more about the project and contribute.

.. _Andrea Trentini: https://atrent.it
.. _Giovanni Biscuolo: https://github.com/gbiscuolo
.. _Shreyansh Khajanchi: https://www.shreyanshja.in/
.. _official Debian website: https://wiki.debian.org/SummerOfCode2018/Projects/BootTorrent

Revision history:

+------------+------------+---------------------+
| Date       | Version    |  Description        |
+------------+------------+---------------------+
| 2018/06/15 | V:0, R:0   |  Initial draft      |
+------------+------------+---------------------+

Creation date: 15-June-2018

System Purpose
--------------

Context of the project
~~~~~~~~~~~~~~~~~~~~~~

Currently, the standard network boot process for computers is as follows:

* A central server computer serves all the necessary data required to network boot other computers.

* Other computers (clients) download from this central server and then start the operating system.

The inclusion of this 'central server' creates problems identified below:

* The performance of the server becomes a bottleneck.

* Centralized nature of this server mean that it may not be able to scale to large clusters.

BootTorrent is intended to help solve this problem with the help of distributed P2P data sharing technologies such as BitTorrent. It explores the idea of using these techniques to program clients to share data among themselves, reducing the need of a single server providing all the data. This, in effect makes the clients a provider of the data as well. In other words, the clients become 'peers' to each other in a large cluster of computers.

::

    +--------+                  +------------------------------+
    |        |   Share data     |                              |
    | client | <--------------- |   +------+        +------+   |
    |        | + configuration  |   | peer |        | peer |   |
    +--------+                  |   +------+        +------+   |
        ^                       |                              |
        |                       |                              |
        | Provides data         |                              |
        | + configuration       |   +------+        +------+   |
        |                       |   | peer |        | peer |   |
    +--------+                  |   +------+        +------+   |
    |        | Provides data    |                              |
    | server | ---------------> |                              |
    |        | + configuration  +------------------------------+
    +--------+                     cluster of clients / peers

    Fig 1: Interaction of computers sharing data together.

The ideal use case of BootTorrent is when a considerably large operating system (measured in bytes) is required to be run on the clients via network booting and the server providing the data is not performant enough to serve all the client on its own in constrained time requirements.

BootTorrent interface
~~~~~~~~~~~~~~~~~~~~~

BootTorrent should implement the following:

* Client configuration interface.
    | Capability to prepare the computers for booting process.
    | Clients do not come pre-programmed with support of any form of P2P booting process.
    | Clients generally only support simpler client-server protocols such as TFTP.
    | Fulfill this responsibility by using these simpler protocols to create a environment to enable P2P protocols in the clients.

* Initial data provider interface.
    | Capability to work as a seeding peer for the cluster.
    | A computer is needed to provide the first-hand copy of the shared data for the cluster to be able to download it and share it among themselves.
    | Fulfill this responsibility by becoming a part of the cluster itself and then sharing data.

* Client data sharing interface.
    | Capability to act as peers to other computers.
    | P2P protocols work on the assumption that >=1 other computer(s) in the network are willing to share data.
    | Fulfill this responsibility by becoming a peer in the network and initiating sharing.

* Operating System loading interface.
    | Capability to load a download Operating System
    | Fulfill this responsibility by loading the Operating system via correct method such as Kexec.

In addition to that, client computer include pre-programmed:

* BIOS/UEFI network boot interface.
    | This is programmed and included by the manufacturer of the computer.
    | It has various names: PXE, Network Boot, Ethernet boot ROM... etc.
    | It needs to be enabled on the clients.

Non-functional requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Qualities**

    - The system should continue to work even if peers go online or offline during run.

* **Constraints**

    - Should be small in size so that it can be quickly loaded.

* **Principles**

    - Use small base system so that constraints can be satisfied.

Structure
---------

Overview
~~~~~~~~

The general overview of the architecture is as follows:

::

    Fig 2: Placement and structure of components:

      Server                   Client                        Peer(s)
    +------------------+     +----------------------+     +----------------------+
    |                  |     | +------------------+ |     | +------------------+ |
    |                  |     | |Operating system  | |     | |Operating system  | |
    |                  |     | |loading interface | |     | |loading interface | |
    |                  |     | +------------------+ |     | +------------------+ |
    |                  |     |          ^           |     |                      |
    |                  |     |          | (4)       |     |                      |
    | +--------------+ |     | +------------------+ |     | +------------------+ |
    | |Initial data  | <-----> |Client data       | <-----> |Client data       | |
    | |provider intf | | (3) | |sharing interface | | (3) | |sharing interface | |
    | +--------------+ |     | +------------------+ |     | +------------------+ |
    |                  |     |          ^           |     |                      |
    |                  |     |          | (2)       |     |                      |
    | +--------------+ |     | +------------------+ |     | +------------------+ |
    | |Client config | |     | |BIOS/UEFI network | |     | |BIOS/UEFI network | |
    | |interface     | ------> |boot interface    | |     | |boot interface    | |
    | +--------------+ | (1) | +------------------+ |     | +------------------+ |
    +------------------+     +----------------------+     +----------------------+

This architecture was chosen after considering the limitations that are present on the current network boot implementations pre-programmed widely in the hardware by manufacturers.

The constraint is that BIOS/UEFI ROMs of the hardware do not support any form of P2P networking technologies and have build-in support for only simpler protocols such as HTTP/TFTP etc. So, to be able to utilize P2P networking technologies, it is necessary load the client computers with custom software (that supports Client data sharing interface, in other words, P2P networking) via simpler protocols like TFTP.

The server contains two interfaces, that are: Client configuration interface and Initial data provider interface. For each client in the network, the client configuration interface provide the initial configuration details to the clients.

On receiving the initial configuration details, client's network boot interface will be able to start the client's data sharing interface. The data sharing interface connects to other computers to mutually share data.

The server's Client configuration interface programs client's network boot interface to load an executable binary. This binary sets in motion the precedence of loading client data sharing interface on the clients. Which then proceeds to initiate sharing of data with other peers via a peer's client data sharing interface.

Once the download is finished, the client data sharing interface will call Operating system loading interface to load the Operating system with the correct method.

Components
~~~~~~~~~~

This section provides more details about each component in the architecture.

DHCP/TFTP server
****************

* **Responsibilities**
    | To setup the clients to load necessary software to activate data sharing interface.
    | **Provides interface**: client configuration interface
    | **Rationale**: Client computers include support for DHCP and TFTP protocol for network booting process.

* **Collaborators**
    | BIOS/UEFI network boot interface

* **Notes**
    | Uses DHCP to instruct clients to download PXE binary and uses TFTP to send the PXE binary.
    | Runs on the server.

Torrent software - server
*************************

* **Responsibilities**
    | Seeds first-hand copy of Operating system files to the P2P network.
    | **Provides interface**: Initial data provider interface
    | **Rationale**: P2P networks need that, collectively, the whole network should have one complete copy of the necessary files to successfully download them. Transmission makes sure that one complete copy is available at any point of time.

* **Collaborators**
    | Client data sharing interface

* **Notes**
    | Runs on the server.

Torrent software - client
*************************

* **Responsibilities**
    | Download the Operating System files to client computers via torrents.
    | **Provides interface**: Client data sharing interface

* **Collaborators**
    | Initial data provider interface

* **Notes**
    | Runs on the client.

Operating system loader
***********************

* **Responsibilities**
    | Loads the downloaded Operating system.
    | **Provides interface**: Operating system loading interface

* **Collaborators**
    | Client data sharing interface

* **Notes**
    | Runs on the client.
    | Tools such as Kexec, Qemu can be used to load.

Process overview
~~~~~~~~~~~~~~~~

1. Initialization of Client configuration interface
***************************************************

The client configuration interface is on the server. During the bring-up of this interface, the server computes the following details:

* Host parameters such as Network interface, IP addresses, Operating systems images available etc.
* Client parameters such as information on Operating systems, list of protocols to use etc.
* Metadata about the files and folders that need to be distributed via BitTorrent P2P protocols.

After the computation of these details, the Client configuration interface is activated in the system and is on standby to respond to any requests by BIOS/UEFI network boot interface.

Additionally, it exports the following information for consumption by other interfaces:

* Host parameters
* Client parameters
* Metadata (P2P)

2. Initialization of Initial data provider interface
****************************************************

Requires: Client configuration interface (Host parameters, Metadata (P2P))

The initial data provider interface is on the server. During the bring-up of this interface, the server does the following:

* Using the host parameters, the server becomes the part of P2P network as discribed in the parameters.
* Using the metadata, the server will start sharing first-hand copy of the files and becomes available to respond to any sharing requests.

The Initial data provider interface now goes standby and responds to any requests from Client data sharing interface.

**Note: at this point, the server is ready with all it's components**

3. Initialization of BIOS/UEFI network boot interface
*****************************************************

Requires: Client configuration interface (Client parameters, Metadata (P2P))

This interface is available pre-programmed inside the ROM on the client computers. After power is applied to client computers, client initialize this interface automatically.

After initialization, it copies Client parameters and Metadata (P2P) from the server via Client configuration interface and loads Client data sharing interface.

It provides the following for consumption by other interfaces:

* Suitable environment for Client data sharing interface.

4. Initialization of Client data sharing interface
**************************************************

Requires: BIOS/UEFI network boot interface (Suitable environment)

This interface is loaded on clients by BIOS/UEFI network boot interface. During the bring-up of this interface the server does the following:

* Initialize networking stack on the client.
* Load P2P networking support software on the client.
* Download Operating system image files from the network to local memory.

After the above tasks are finished it calls Operating system loading interface.

It provides the following for consumption by other interfaces:

* Operating system image files.

5. Initialization of Operating system loading interface
*******************************************************

Requires: Client data sharing interface (Operating system image files)

This interface is loaded on clients by Client data sharing interface. During the bring-up of this interface the server does the following:

* Read operating system image files.
* Decide appropriate method to load the Operating system.
* Launch the Operating system.

After loading the operating system, BootTorrent exits from the client.

Mechanisms
----------

Loading client data sharing interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BIOS/UEFI network boot interface has very limited functionality but this limited functionality is flexible enough that it allows loading a small Operating System. This Operating system will be pre-programmed to be able to fully use any form of distributed P2P data sharing technology such as BitTorrent or anything else that may be desired.

