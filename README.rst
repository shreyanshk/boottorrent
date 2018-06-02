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

WARNING: STATUS - ALPHA: DO NOT USE IN PRODUCTION!

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

* `Hefur`_ (Optional)

.. _Transmission: https://github.com/transmission/transmission
.. _Dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _Hefur: https://github.com/abique/hefur
.. _Python 3.6: https://www.python.org/

Please check your distribution specific guide for instructions on how to install them.

Next, Please install the package itself:

.. code-block:: bash

    $ pip install -e https://github.com/shreyanshk/boottorrent

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

.. _Andrea Trentini: https://github.com/atrent
.. _Giovanni Biscuolo: https://github.com/gbiscuolo
.. _Shreyansh Khajanchi: https://www.shreyanshja.in/
.. _Click here: https://wiki.debian.org/SummerOfCode2018/Projects/BootTorrent

Credits
-------

This project is inspired from the Academic `Thesis`_ of Andrea Trentini.
See the videos of test run at:

* `https://www.youtube.com/watch?v=3gTfrIiJf74 <https://www.youtube.com/watch?v=3gTfrIiJf74>`_
* `https://www.youtube.com/watch?v=ihFOw8eJZzc <https://www.youtube.com/watch?v=ihFOw8eJZzc`_
* `https://www.youtube.com/watch?v=Quj_Ztipjw8 <https://www.youtube.com/watch?v=Quj_Ztipjw8>`_
* `https://www.youtube.com/watch?v=GZMQaSjfqKY <https://www.youtube.com/watch?v=GZMQaSjfqKY>`_


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Theses`: http://sl-lab.it/dokuwiki/doku.php/tesi:boottorrent_en
