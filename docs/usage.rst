=====
Usage
=====

After installation, a new binary named ``boottorrent`` should be available in your console. This program is your entry point and the way to interact with the system.

You can verify the installation by checking for the installed version inside your console.

.. code-block:: console

    $ boottorrent version
    BootTorrent 0.1.0

Please make sure that you've activated the environment and/or Python version where you've installed BootTorrent.

Available commands
------------------

* init
    | Initializes a new BootTorrent project.
    | Check the 'Get Started' guide for instructions on how to work with a BootTorrent project.

* start
    | Starts the BootTorrent process.

* version
    | Show the current installed version.

Initializing a BootTorrent env
------------------------------

Let's create a directory(a dedicated env for BootTorrent) for keeping all the required files together.
BootTorrent can set you up with a basic configuration with sane values for most variables.
For example to create a new env with the name ``test``, execute:

.. code-block:: console

    $ boottorrent init test

This should create a new folder named ``test`` with the following structure:

.. code-block:: console

    test
    ├── Boottorrent.yaml
    └── oss

Now, your environment is ready.
Consider updating the Boottorrent.yaml files according to your hardware/software setup.
Documentation for various parameters is included inside the new env itself.

Configuring BootTorrent
-----------------------

The ``Boottorrent.yaml`` file present in an env is used to configure the internal working of BootTorrent.
Available Parameters are as follows.

.. include:: ../boottorrent/assets/skel/README.rst

Adding Operating Systems
------------------------

.. include:: ../boottorrent/assets/skel/oss/README.rst

Start BootTorrent
-----------------

To start the processes:

1. Change directory to your env (where Boottorrent.yaml file is placed).
2. Execute:

.. code-block:: console

    $ boottorrent start

Note: You may have to provide root access as Dnsmasq requires direct access to the network interface.
You can avoid giving root access if you use setcap to provide proper permission to dnsmasq binary.

.. code-block:: console

    $ sudo setcap CAP_NET_BIND_SERVICE,CAP_NET_RAW,CAP_NET_ADMIN=+ep /usr/bin/dnsmasq

Go ahead and try to network boot other machines. Look for an options with the names of added OSs and select your choice to start the booting process in clients.
