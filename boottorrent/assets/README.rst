ph1: Phase 1 kernel + image
===========================

* bzImage64
    This is the kernel image that will be send to the clients over TFTP.

* rootfs.gz
    Initrd image compiled against the above kernel.

* pxelinux.0 & ldlinux.c32
    This is the PXE Linux loader along with COM32R executable for loading the kernel.

* pxelinux.cfg
    Confiugration file that is send to client computers over TFTP.

* diff.gz
    Files in this directory unpack over SliTaz's rootfs.gz and
    replaces previous files if another file with same name is already present


tpls: Template file for external components
===========================================

* dnsmasq.conf.tpl
    Template for Dnsmasq DHCP + TFTP server
    Placed at out/dnsmasq/dnsmasq.conf after processing

* transmission.json.tpl
    Transmission settings.json template


skel: Skeletal folder for new BootTorrent project
=================================================

This folder is copied as a base for new BootTorrent project when invoked with::

    $ boottorrent init <new_project_name>
