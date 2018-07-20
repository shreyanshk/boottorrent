==========================
Frequently Asked Questions
==========================

Why does BootTorrent require superuser network access?
------------------------------------------------------

Binding to low network ports (<1024) on Unix like computers requires superuser access. Because BootTorrent needs access to port 67 (DHCP) and port 69 (TFTP), it needs superuser access. So, either you can run BootTorrent in an elevated shell or you could use ``setcap`` utility to provide appropriate permissions.

Which architectures are supported?
----------------------------------

Currently, BootTorrent only supports x86 architecture and it's 64-bit extension (AMD64/x86_64) on the server and the clients. The server can be either 32-bit or 64-bit regardless of whatever type of Operating system is being served. The client has to additionally support 64-bit extensions to run any 64-bit Operating system being served, in absence of which it can only run 32-bit Operating systems.

Can I mix 32-bit and 64-bit machines?
-------------------------------------

Yes, you can mix them but please note that 32-bit machines will fail to boot any 64-bit Operating System being served.

What happens to previous DHCP configuration, if BootTorrent is started on a host with active DHCP server?
---------------------------------------------------------------------------------------------------------

BootTorrent doesn't change any present DHCP configurations and won't terminate any other running DHCP server. BootTorrent also allows you to limit the interfaces on which it serves DHCP requests by configuring the ``Boottorrent.yaml`` file. Please note that if multiple DHCP servers are running on same interface then there is a possibility of conflict. So, please make sure of this before starting BootTorrent.

Can I run BootTorrent if there is already an external DHCP server on the network?
---------------------------------------------------------------------------------

Because BootTorrent runs it's own DHCP server, it may conflict with the external DHCP server. It's also doubtful that your network administrator will appreciate another DHCP server on the network without explicit persmission. Please discuss with your network administrator on what can be done.

What can I do if I don't have any control over the present DHCP server?
-----------------------------------------------------------------------

Your network administrator will have to manually set the DHCP server to point to BootTorrent server. Please disable DHCP server provided by BootTorrent and ask your network administrator to set PXE boot file to "<IP of BootTorrent server>/pxelinux.0" and DHCP option 209 to "<IP of BootTorrent server>/pxelinux.cfg" (https://tools.ietf.org/html/rfc5071) in the active DHCP server. Please refer to your DHCP server's documentation for instructions on how to set these options.

You'll also need to disable the DHCP server provided by BootTorrent. Please read more about usage documentation for more details.

I have exotic hardware and BootTorrent doesn't include it's software. What can I do to make it work?
----------------------------------------------------------------------------------------------------

BootTorrent's Phase 1 Linux system is an easy to modify/extend customized SliTaz distribution. All the files required to generate this distribution are placed in phase1bootstrap/slitaz/ directory inside source repository and can be generated with `Tazlito`_. The file ``distro-packages.list`` lists all the packages that are installed in the generated live image and more SliTaz packages can be added if desired.

You can modify these files according to your needs and then place the generated files at their correct location as specified in the `build documentation`_. You can also read the SliTaz's `hacking guide`_ for information on how you can further modify the live image.

.. _Tazlito: http://doc.slitaz.org/en:handbook:genlivecd
.. _build documentation: https://boottorrent.readthedocs.io/en/latest/installation.html#from-sources
.. _hacking guide: http://doc.slitaz.org/en:handbook:hacklivecd

How can I add support for more architectures to BootTorrent?
------------------------------------------------------------

You can start with porting the runtime and build dependencies to the new architecture. Then you can proceed to port the client package to the new architecture. This include the files in the boottorrent/assets/ph1 directory: PXE Linux loader and Phase 1 Linux system. If you've made it this far, please consider creating a pull request.

The client package (boottorrent/assets/ph1) consists of:

* pxelinux.0
	| It is the PXE Linux bootloader (based on Syslinux).

* pxelinux.cfg
	| It is the configuration file for the above bootloader.

* ldlinux.c32
	| It is a COM32 library for loading Linux kernel. It is provided with Syslinux.

* bzImage
	| It is the Linux kernel image (currently for x86 architecture).

* rootfs.gz
	| It is the rootfs corresponding with the kernel image.

* diff.gz
	| Diff file containing BootTorrent specific changes to the SliTaz image.

The client TUI package (phase1bootstrap) consists of:

* tui.go
	| BootTorrent TUI written in Golang.

* Makfile
	| Makefile to automate the process of compiling the TUI software.
	| Variables ``GOOS`` and ``GOARCH`` will be of interest if you want to port the software to other architectures. Read more at `Golang documentation`_.

.. _Golang documentation: https://golang.org/doc/install/source#environment

What are the differences between BootTorrent and the original 'boottorrent' UniMi project?
------------------------------------------------------------------------------------------

The improvements over the 'boottorrent' UniMi project includes:

1. No need to fiddle with any cpio or lzma archives.
2. Allows you to run Qemu images as well.
3. You can choose between multiple OS to boot at runtime.
4. Eliminate the need for an HTTP server.

Where are the logs and how can I configure them? (verbosity, target file/daemon, etc.)
--------------------------------------------------------------------------------------

The logs for Dnsmasq and Aria2 are currenly prepended with 'DNSMASQ:' and 'ARIA2:' and are displayed on the terminal screen. It's possible to control Aria2's logging via console_log_level parameter. You can also use shell redirection to write the logs to any file.

Where are the downloaded OS files saved on the client?
------------------------------------------------------

The images are saved to the RAM on download. Which means their execution is very fast but it also means that Qemu based methods (such as qemu-iso) may have usable RAM that is less than total available RAM and is roughly equal to (total RAM - image size - size of Phase 1 Linux system).

Kexec based method can use full RAM because the new OS is loaded in-place and is given complete ownership of all the underlying hardware.

What mode is used to run Qemu in BootTorrent?
---------------------------------------------

Currently, Qemu is run in system emulation mode. That is, a complete computer is emulated/virtualized by Qemu.
