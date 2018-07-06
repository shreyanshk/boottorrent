Refactoring
===========

The scope of this document is to put forward the ideas that can be explored to reduce complexity or the project without impacting functionality in any significant way.

There are two sections of this document.

* Deps that can be potentially removed.

* Deps that can be potentially replaced with lighter/simpler tools.

Removable Deps
--------------

Opentracker
~~~~~~~~~~~

Functionality
+++++++++++++

Opentracker runs on the host computer and is used to provide a torrent tracker so that the client can discover each other and the seed (server) fast and efficiently because, as noted in documentation, LPD can be very slow to work.

Alternate
+++++++++

With DHT enabled, every node in a BitTorrent based network can effectively work as a tracker because, for every torrent (on a node), the node store the connection details of it's neighbourhood peers (neighbourhood means close proximity according to preselected distance function, does not imply geographical proximity). Effectively allowing discovery of the whole network by iteratively asking discovered peers for their peer list.

Replacement program
+++++++++++++++++++

Replacement (server):

* Transmission
    | Already a dependency and included

* `Aria2`_ + `mktorrent`_
    | Much more lightweight combination that Transmission.

.. _mktorrent: https://packages.debian.org/stretch/mktorrent
.. _Aria2: https://packages.debian.org/stretch/aria2

Replacement (client): None, no changes to client. Scope of work limited to server.

Notes
+++++

1. Transmission tries to connect to host ``dht.transmission.com`` to connect with global DHT network (this host works as entry point to network), if DHT is enabled. It's a public network and may pose privacy risk and it cannot be disabled from Transmission.

2. Transmission should work as a local DHT network if access to ``dht.transmission.com`` is blocked via any means such as firewall or IP tables.

3. Aria2 doesn't connect to any external host (as per knowledge) and simply listens on a port for other DHT client. Effectively making a local DHT network.

Python Click
~~~~~~~~~~~~

Functionality
+++++++++++++

It is a small library used to make the task of writing CLI tools in Python easier. It is used on the host/server to parse CLI commands.

Alternate
+++++++++

Manually parse CLI commands in Python.

Low complexity of CLI interface in BootTorrent makes it possible to handle all cases simply with Standard Library.

Replacement
+++++++++++

Python Standard Library (included with any Python installation)

Python Requests
~~~~~~~~~~~~~~~

Functionality
+++++++++++++

To add torrents files for seeding purposes, HTTP interface of Transmission is used.

Requests is the de facto/recommended HTTP client library in Python. Though, it is being only used for 1 line of code (Requests is very terse).

Alternate
+++++++++

Since, the complexity is not high. It's possible to use Python Standard Library to do the HTTP request.

Replacement
+++++++++++

Python Standard Library (included with any Python installation)

Replaceable Deps
----------------

bsdtar
~~~~~~

Functionality
+++++++++++++

It is used to pack ``SVR4 with no CRC (newc)`` type of archive to be used by client computers. The archive contains torrent metadata.

Alternate
+++++++++

`GNU cpio`_ has significantly less dependencies than bsdtar/libarchive.

.. _GNU cpio: https://packages.debian.org/stretch/cpio
