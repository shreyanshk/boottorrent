=====
Usage
=====

BootTorrent allows you to boot your computers over network with torrents as the main method of data transfer. It brings a lot of different technologies together. The main package contains only the application logic to work with the system. Since, these technologies have a lot of switches and parameters and no single combination with work on wildly differing hardware/software configurations at different organizations, the configuration has been decoupled from the system.

Getting started with BootTorrent is a multi-stage process with:

1. Installation of BootTorrent
2. Initialize a new directory with base configuration.
3. Add Operating systems and their specific configuration.
4. Starting the system.


Install
------------

BootTorrent can be installed by executing the command::

    $ pip install git+https://github.com/shreyanshk/boottorrent

A new binary 'boottorrent' should now be available in your console.


Initialize base config
-------------------------------

The configuration is stored (with a very specific structure) in another directory outside of the package and is controlled directly by the user.
The project includes logic to help you quickly create it.
To create a configuration directory with the name 'testdir', execute::

    $ boottorrent init testdir

A new directory named 'testdir' will be created in the working directory. The file 'config.yaml' is of importance as it controls the parameters that will be passed to various components.


Add more OSs
----------------------------------------------------------

The base project directory will have a new directory named 'oss'. Present inside this (oss) directory will be more directories (eg: mint, ubuntu1604 etc) containing all the files (generally: kernel, initrd-- but not limited to) needed to boot an operating system present in that directory.

[WIP: incomplete]


Start the system
-------------------

Change your console's working directory to the configuration directory and invoke::

    $ sudo boottorrent start

This will start the processes and then you can try to network boot the computers connected to the host.
