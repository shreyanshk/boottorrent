=====
Usage
=====

After installation, a new binary named ``boottorrent`` should be available in your console. This program is your entry point and the way to interact with the system.

You can verify the installation by checking for the installed version inside your console.

.. code-block:: console

    $ boottorrent version
    BootTorrent 0.1.0

Please make sure that you've activated the virtualenv and/or Python version where you've installed BootTorrent.

Available commands
------------------

* init
    | Initializes a new BootTorrent project.
    | Check the `Quick start`_ guide for instructions on how to work with BootTorrent.

.. _Quick start: https://boottorrent.readthedocs.io/en/latest/quickstart.html

* start
    | Starts the BootTorrent process.

* version
    | Show the current installed version.

Initializing a BootTorrent env
------------------------------

Let's create a directory (a dedicated env for BootTorrent) for keeping all the required files together.
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
Documentation for various parameters is included further in this document and inside the env.

Configuring BootTorrent
-----------------------

.. include:: ../boottorrent/assets/skel/README.rst

Adding Operating Systems
------------------------

.. include:: ../boottorrent/assets/skel/oss/README.rst

Start BootTorrent
-----------------

Note:

* Please be sure that other DHCP servers and/or TFTP servers are not running on your computer/network as they may conflict with BootTorrent.
* Please make sure that the chosen ports are not being used by other applications.

BootTorrent requires superuser access to bind to DHCP+TFTP ports (because they are low-ports). You can provide proper permission by either of two methods:

With elevated shell
~~~~~~~~~~~~~~~~~~~

You can start a root shell (i.e ``sudo bash``) and activate Python/Virtualenv in that shell.

Then, execute these commands on your computer:

.. code-block:: console

    # whoami
    root
    # source <virtualenv>/bin/activate # if you're using virtualenv
    # boottorrent start

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

You can learn more details about the permissions on `Capabilities man page`_.

.. _Capabilities man page: https://linux.die.net/man/7/capabilities

Go ahead and try to network boot other machines. Look for an options with the names of added OSs and select your choice to start the booting process in clients.
