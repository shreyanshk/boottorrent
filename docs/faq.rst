==========================
Frequently Asked Questions
==========================

Which architectures are supported?
----------------------------------

Currently, BootTorrent only supports x86 architecture and it's 64-bit extension (AMD64/x86_64) on the server and the clients. The server can be either 32-bit or 64-bit regardless of whatever type of Operating system is being served. The client has to additionally support 64-bit extensions to run any 64-bit Operating system being served, in absence os which it can only run 32-bit Operating systems.

Can I mix 32-bit and 64-bit machines?
-------------------------------------

Yes, you can mix them but please note that 32-bit machines will fail to boot any 64-bit Operating System being served.

What happens to previous DHCP configurations, if the host computer is the DHCP server, the DHCP server is active, and I start BootTorrent?
------------------------------------------------------------------------------------------------------------------------------------------

BootTorrent doesn't change any already present DHCP configurations and won't terminate any other running DHCP server. BootTorrent also allows you to limit the interfaces on which it serves DHCP requests by configuring the ``Boottorrent.yaml`` file. Please note that if multiple DHCP servers are running on same interface then there is a possibility of conflict. So, please make sure of this before starting BootTorrent.

Can I run BootTorrent if there is already an external DHCP server on the network?
---------------------------------------------------------------------------------

Because BootTorrent runs it's own DHCP server, it may conflict with the external DHCP server. It's also doubtful that your network administrator will appreciate another DHCP server on the network without explicit persmission. Please discuss with your network administrator on what can be done.

What can I do if I don't have any control over the present DHCP server?
-----------------------------------------------------------------------

In such a case, unfortunately, you may not be able to run BootTorrent. Because BootTorrent depends on using the DHCP protocol to prepare the clients for booting it needs to be the exclusive DHCP server on the network and the present DHCP server may conflict.


