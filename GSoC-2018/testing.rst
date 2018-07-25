===================
Testing BootTorrent
===================

The goal of testing is:

1. To check if features work correctly on rebuilds of Phase1 Linux System because it's build process is out of control of BootTorrent project and it's result may not be reproducible.

2. To ensure any contributed code from other sources do not break BootTorrent.

3. To help quickly test the package when porting to other architectures.

Brief stack overview
--------------------

BootTorrent is composed of two main components. Those are:

Server application
~~~~~~~~~~~~~~~~~~

The server application is the central point to control the process and is run on the computer which will provide configuration/data to other client nodes (discussed later in this document).

Components
++++++++++

The server is composed of various components:

* A torrent client           : Aria2
    | Uses BitTorrent protocol

* A file server              : Dnsmasq
    | Uses TFTP protocol

* A configuration server     : Dnsmasq
    | Uses DHCP protocol

* A torrent tracker          : Opentracker
    | Uses HTTP/UDP protocol

Responsibilities
++++++++++++++++

1. Write correct configuration files for the components and place the files at the correct position.

2. Launch the 3rd party programs with correct parameters.

Client application
~~~~~~~~~~~~~~~~~~

The application is downloaded on the clients via TFTP server and then executed by the bootloader.

Components
++++++++++

The client is build on these components:

* A PXE Linux bootloader    : Syslinux
    | Loads the Linux kernel from the PXE environment.

* A Linux environment       : SliTaz
    | Composed of precompiled custom SliTaz distribution (Kernel + Initrd).

* OS Loader                 : Kexec, Qemu
    | Available in SliTaz repository.

* BootTorrent TUI           : Golang
    | Uses GoCUI, GoYAML packages
    | Depends on OS Loaders

Responsibilities
++++++++++++++++

1. Download the requested OS via BitTorrent.

2. Call correct OS loader on the OS.

Unit testing
------------

1. Components are external (except TUI + Python package).

2. Components are isolated from each other and can be tested with their own test suite.

3. Business logic in BootTorrent is limited to string substitutions and file I/O (reading/writing configuration files) and launching processes as there is little decision making in the code.

Concerns
~~~~~~~~

Testing code should not have same complexity as tested code (otherwise it becomes a reimplementation of the latter). And, there is little value in writing unit tests as code complexity of BootTorrent is very low. Writing unit tests ends up testing for these external components and not code written in the BootTorrent application. Cases in point:

1. Testing whether configuration file is written ends up testing Python's file I/O.

2. Testing if processes are launched ends up testing Python's subprocess module.

3. Testing for loading of OS ends up testing Qemu and Kexec.

4. Testing if substitutions are being done ends up testing Jinja2 templating engine.

This is better served by these package's own test suite. Hence, unit testing may not be suitable for BootTorrent.

Integration testing
-------------------

Basic requirements
~~~~~~~~~~~~~~~~~~

1. Be able to test if the client computer loads Phase 1 Linux System.

2. Be able to test if SliTaz image is able to load the correct OSs.

Suggested methodology
~~~~~~~~~~~~~~~~~~~~~

The constraints of BootTorrent is that testing it requires launching multiple computers (either physical or virtual). The host OS / BootTorrent / Application code on the client computer also loses control of the hardware in case of Kexec. So, any client side testing code won't work. In case of Qemu based boot, the host OS on client cannot get the status of the guest OS until guest OS exits (at which point Qemu returns control) because Qemu takes control.

This means that the server computer needs to use out-of-band methods to verify that tested feature work. One method is to capture the screenshot of the client computer as a user would see it and work with screenshots to test if the software behaves as expected. This, in turn, means that client computer needs to be simulated on the host computer itself because in this case the server can use standard Xorg protocols to capture the screenshot of the VirtualBox VM window. This captured image can then be used to reason about the state of the system and identify if a feature worked.

**Note: This testing code may not work on Wayland because the protocol doesn't allow capturing other windows due to security reasons.**

As work around for these contraints, all testing code must reside on the server and the whole process should be simulated on the server, where BootTorrent code will always be in control.

Hence, the testing process is:

1. Launch an Xorg based session.

2. Launch VMs on local machine.
    | VirtualBox can be used to launch VMs.

3. Scrape VM window to get it's state.
    | Python package pyscreenshot can be used to grab screen.

4. Compare captured image to provided testing image.
    | Pixel to pixel comparison need to be done. Python Imaging Library (PIL) can be used.

 **Note: These requirements are additional over the runtime requirements.**

Process
~~~~~~~

1. Configures a host-only network on the host.
    | May need to be manual as Superuser may be required.

2. Test launches a BootTorrent server instance.

3. Test launches a VM on VBox

4. Test grabs a screenshot of the screen using pyscreenshot

5. The screenshot is cropped to the area of VM window

6. The cropped screenshot is compared against known screenshot and result is returned

Concerns
~~~~~~~~

The suggested testing methodology has the following issues:

1. The testing won't work with Wayland based sessions which is increasingly becoming the default session type in various popular distributions.

2. The written code may be dependent on the GUI / User Interface of the server as the code is working with screenshots. This means that, for example, even changing width of title bar may result in apparent failure of a test because of mismatch at pixel level in the "truth" screenshots.

3. Software that change display color characteristics such as Redshift / Gamma correction / Tone correction may influence testing because they change the RGB intensity at the pixel level which will invalidate all "truth" screenshots.

i.e: The code will be very dependent on the display settings of the computer.
