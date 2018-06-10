===========
BootTorrent
===========

.. image:: https://img.shields.io/pypi/v/boottorrent.svg
        :target: https://pypi.python.org/pypi/boottorrent

.. image:: https://img.shields.io/travis/shreyanshk/boottorrent.svg
        :target: https://travis-ci.org/shreyanshk/boottorrent

.. image:: https://readthedocs.org/projects/boottorrent/badge/?version=latest
        :target: https://boottorrent.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

BitTorrent based distributed network booting of various Operating systems... even on diskless nodes.

BootTorrent allows you to easily transfer and execute an Operating System image over the network to your distributed cluster of computers via BitTorrent’s distributed protocol while giving you central manageability of the said Operating system image. Upgrading is as simple as rebooting the nodes in the network after the upgrade has started seeding from the central computer.

Checkout the `Install`_ and `Get Started`_ guide for information on how to get started.

.. _`Install`: https://github.com/shreyanshk/boottorrent#installation
.. _`Get Started`: https://github.com/shreyanshk/boottorrent#get-started

If you have considerable number of independent computers at your disposal and you’re looking to simply deploy any given System image(s) (that may have been hand-crafted according to your needs), such as that of a compute node for an HPC/ML cluster, over the whole network, consider BootTorrent.

The advantage of BootTorrent over standard network booting is that the bottleneck caused by a central server serving the image is reduced and BootTorrent removes the linear scaling factor in total time to bring a cluster online fully functional by utilizing Peer-to-Peer protocol. The nodes share the image data among themselves, hence, improved boot times.

We have tried to identify some usecases in [usecases] file. Consider reading it to find out how BootTorrent can be useful to you.

**WARNING: STATUS - ALPHA: DO NOT USE IN PRODUCTION!**

* Free software: GNU General Public License v3
* Documentation: https://boottorrent.readthedocs.io.


Features
--------

* TODO


Installation
------------

This project depends on:

* `Python 3.6`_

* `Transmission`_

* `Dnsmasq`_

* `bsdtar`_ (provided by libarchive)

* `Hefur`_ (Optional)

* `Golang`_ (build dependency)

.. _Transmission: https://github.com/transmission/transmission
.. _Dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _Hefur: https://github.com/abique/hefur
.. _Python 3.6: https://www.python.org/
.. _bsdtar: http://www.libarchive.org/
.. _Golang: https://golang.org/

Please check your distribution specific guide for instructions on how to install them.


Get the source code
~~~~~~~~~~~~~~~~~~~

Downloading source code with ``git`` is very straightforward.

.. code-block:: bash

    $ git clone git@github.com:shreyanshk/boottorrent.git


Pre-Install: Building assets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**You can skip this section because it is only for documentation purpose as these resources are currently checked in with the repository**

.. code-block:: bash

    $ cd phase1bootstrap
    $ make initrd

This will create the assets and place them at proper locations in the repository.


Install package
~~~~~~~~~~~~~~~

Next, Please install the package itself:

.. code-block:: bash

    $ pip install -e boottorrent


Get Started
-----------


Prepare your environment
~~~~~~~~~~~~~~~~~~~~~~~~

First, Let's create directory for keeping all the required files.
BootTorrent can set you up with a basic config with sane values for most variables.
For example to create a new directory with the name ``proj``, execute:

.. code-block:: bash

    $ boottorrent init proj

This should initialize a new folder ``proj`` with the following structure:

.. code-block::

    proj
    ├── Boottorrent.yaml
    └── oss

Now, your environment is ready.
Consider updating the Boottorrent.yaml files according to your hardware/software setup.
Documentation for various parameters is included inside the file itself.


Adding a Linux based OS
~~~~~~~~~~~~~~~~~~~~~~~

Let's say that you have a compiled kernel (vmlinuz) and corresponding initrd (initramfs.img) ready with you, the process is:

1. Create a new folder in the oss/ directory, let's say ``testos``.
2. Drop the files into oss/testos.
3. Add a file oss/testos/config.yaml with content (modify according to your needs):

.. code-block:: yaml

    dispname: TestOS # Friendly name to display
    method: kexec
    kernel: vmlinuz
    initrd: initramfs.img
    cmdline: break # cmdline for the new kernel

4. Update display_oss variable in the Boottorrent.yaml file to include the new folder name

Booting added OSs
~~~~~~~~~~~~~~~~~

To start the processes:

1. Change to your project directory (where Boottorrent.yaml file is placed).
2. Execute:

.. code-block:: bash

    $ boottorrent start

Note: You may have to provide root access as Dnsmasq requires direct access to the network interface.
You can avoid giving root access if you use setcap to provide proper permission to dnsmasq binary.

.. code-block:: bash

    $ sudo setcap CAP_NET_BIND_SERVICE,CAP_NET_RAW,CAP_NET_ADMIN=+ep /usr/bin/dnsmasq

Go ahead and try to network boot other machines. Look for an options with the names of added OSs and select your choice to start the booting process in clients.


Authors
-------

GSoC'18 project by `Shreyansh Khajanchi`_ under the mentorship of `Andrea Trentini`_ and `Giovanni Biscuolo`_ for Debian. `Click here`_ to view the project on the official Debian website.

.. _Andrea Trentini: https://atrent.it
.. _Giovanni Biscuolo: https://github.com/gbiscuolo
.. _Shreyansh Khajanchi: https://www.shreyanshja.in/
.. _Click here: https://wiki.debian.org/SummerOfCode2018/Projects/BootTorrent


Credits
-------

This project is inspired from the Academic `Thesis`_ of Davide Bruschi (mentored by Andrea Trentini).
See the videos of test run at:

* `https://www.youtube.com/watch?v=3gTfrIiJf74 <https://www.youtube.com/watch?v=3gTfrIiJf74>`_
* `https://www.youtube.com/watch?v=ihFOw8eJZzc <https://www.youtube.com/watch?v=ihFOw8eJZzc>`_
* `https://www.youtube.com/watch?v=Quj_Ztipjw8 <https://www.youtube.com/watch?v=Quj_Ztipjw8>`_
* `https://www.youtube.com/watch?v=GZMQaSjfqKY <https://www.youtube.com/watch?v=GZMQaSjfqKY>`_


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Thesis`: http://sl-lab.it/dokuwiki/doku.php/tesi:boottorrent_en
