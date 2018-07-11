=================
Quick Start Guide
=================

Getting started with BootTorrent is very easy and this guide will show you the way towards booting a Linux based OS with BootTorrent.
This guide assumes that you've a compiled kernel (bzImage) that you want to boot along with it's corresponding initramfs (initrd.gz) and you have complete control over your network.
This guide also assumes that you've successfully installed BootTorrent. If that is not the case please visit the `Installation`_ guide.

.. _`Installation`: https://boottorrent.readthedocs.io/en/latest/installation.html

Make a BootTorrent env
----------------------

Change directory to where you want to create a new env and then execute:

.. code-block:: console

    $ boottorrent init guidetest
    $ cd guidetest

This initializes a new env with sane defaults and then changes to that env.

Configure the Linux kernel
--------------------------

You need to place the kernel and initrd.gz file inside a sub-directory inside the oss/ directory. You can give any name to the sub-directory. Here, we are assuming the name is ``linuxos``. The console command would look like this:

**Please substitute the brackets with appropriate values**

.. code-block:: console

    $ mkdir oss/linuxos
    $ cp <path: bzImage> oss/linuxos/bzImage
    $ cp <path: initrd.gz> oss/linuxos/initrd.gz

Now, you need to add details about how to boot with these files. So, launch your favourite text editor and add a file with this content.

.. code-block:: yaml
    :caption: oss/linuxos/config.yaml

    dispname: LinuxOS
    method: kexec
    kernel: bzImage
    initrd: initrd.gz
    cmdline: <cmdline>

Next, you need to explicitly tell BootTorrent to enable this OS and update default network ports of various components to make sure they don't conflict with other applications already running on your computer.

.. code-block:: yaml
    :emphasize-lines: 3,7
    :caption: Boottorrent.yaml

    boottorrent:
        ...
        default_os: linuxos
        ...
    opentracker:
        ...
        port: <available port number>
        ...

Hint: you can use any port number between 1024 to 65535 (inclusive).

Finally, you need to update some fields to appropriate values to match with your setup.

.. code-block:: yaml
    :emphasize-lines: 3,7,8
    :caption: Boottorrent.yaml

    boottorrent:
        ...
        host_ip: <your computer's IP as visible to the clients>
        ...
    dnsmasq:
        ...
        interface: <interface you want to use>
        dhcp_range: <IPs ranges in same subnet as host_ip>
        ...

Note: Please make sure that the interface you've selected is already configured statically as DHCP protocol needs this to works properly and the statically configured address belongs to the same subnet as configured in the dhcp_range field in ``Boottorrent.yaml``.

That's it about the configuration.

Booting the Kernel
------------------

Enable PXE on your computers. Please look for your computer's BIOS documentation for instructions.

BootTorrent requires superuser access to bind to DHCP+TFTP ports (because they are low-ports). You can provide proper permission by either of two methods:

With elevated shell
~~~~~~~~~~~~~~~~~~~

You can start a root shell (i.e ``sudo bash``) and activate Python/Virtualenv in that shell.

Then, execute these commands on your computer:

.. code-block:: console

    $ whoami
    root
    $ source <virtualenv>/bin/activate # if you're using virtualenv
    $ boottorrent start

With setcap
~~~~~~~~~~~

``setcap`` can be used to persistently set correct permissions to the dnsmasq binary like this:

.. code-block:: console

    $ sudo setcap CAP_NET_BIND_SERVICE,CAP_NET_RAW,CAP_NET_ADMIN=+ep /usr/bin/dnsmasq

Then, you can activate Python/Virtualenv in a console and execute these commands:

.. code-block:: console

    $ whoami
    user
    $ source <virtualenv>/bin/activate # if you're using virtualenv
    $ boottorrent start

Note: You need not use ``sudo`` here as it will start the BootTorrent process inside another environment.
