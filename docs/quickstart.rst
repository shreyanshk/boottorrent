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

Now, you need to add details about how to boot with these files. So, launch your favourite text editor and a file with this content.

.. code-block:: yaml
    :caption: oss/linuxos/config.yaml

    dispname: LinuxOS
    method: kexec
    kernel: bzImage
    initrd: initrd.gz
    cmdline: <cmdline>

Next, you need to explicitly tell BootTorrent to enable this OS.

.. code-block:: yaml
    :emphasize-lines: 2

    ...
    display_oss: linuxos
    ...

That's it about the configuration.

Booting the Kernel
------------------

Enable PXE on your computers. Please look for your computer's BIOS documentation for instructions.

Execute this command on your computer:

.. code-block:: console

    $ boottorrent start

Watch BootTorrent spring to action and then start your client computers.
