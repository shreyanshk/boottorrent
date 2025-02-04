.. highlight:: shell

============
Installation
============

Dependencies
------------

Components this project depends on include:

* `Python 3.6`_ with `Pip`_

* `Aria2`_

* `mktorrent`_

* `Dnsmasq`_

* `bsdtar`_ (provided by libarchive)

* `Opentracker`_ (Optional)

.. _Aria2: https://github.com/aria2/aria2
.. _Dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _Opentracker: http://erdgeist.org/arts/software/opentracker/
.. _Python 3.6: https://www.python.org/
.. _Pip: https://pip.pypa.io/en/stable/
.. _bsdtar: http://www.libarchive.org/
.. _mktorrent: https://github.com/Rudde/mktorrent

After installation, please make sure that binary files are available in your ``PATH`` variable. You can check it with this command (example for ``dnsmasq``):

.. code-block:: console

    $ which dnsmasq
    /usr/sbin/dnsmasq

The package itself depends on a few Python libraries which are installed automatically by Pip package manager. These libraries are:

* `PyYAML`_

* `Jinja2`_

.. _PyYAML: https://github.com/yaml/pyyaml
.. _Jinja2: http://jinja.pocoo.org/

These dependencies are only for the host running BootTorrent. Please check your distribution specific guide for instructions on how to install them. For building BootTorrent and the list of build dependencies, please refer `build dependencies`_.

From sources
------------

Get the code
~~~~~~~~~~~~

The sources for BootTorrent can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/shreyanshk/boottorrent

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/shreyanshk/boottorrent/tarball/dev

.. _Github repo: https://github.com/shreyanshk/boottorrent
.. _tarball: https://github.com/shreyanshk/boottorrent/tarball/dev

Pre-Install: Build assets
~~~~~~~~~~~~~~~~~~~~~~~~~

**You can skip this section if you do not intent to customize BootTorrent as these resources are currently checked in with the repository**

.. _`build dependencies`:

Building assets requires additional software. This includes:

* `Golang`_

* `SliTaz`_ LiveCD/installation with `Tazlito`_

.. _Golang: https://golang.org/
.. _SliTaz: http://slitaz.org/en/
.. _Tazlito: http://doc.slitaz.org/en:handbook:genlivecd

Some Golang dependencies are also required to build, you can download them with these commands:

.. code-block:: console

    $ cd phase1bootstrap/
    $ make dldeps

To build the SliTaz live image that is run on the client, copy the phase1bootstrap/slitaz/ directory to a Virtual Machine or computer running SliTaz with `Tazlito`_ installed. Then, open a console and execute:

.. code-block:: console

    $ cd <path to copied directory>
    $ sudo tazlito gen-distro

Hint: You can also customize the built image to include more packages, drivers or files etc. Read more `here in the FAQ`_.

.. _here in the FAQ: <https://boottorrent.readthedocs.io/en/latest/faq.html#i-have-exotic-hardware-and-boottorrent-doesn-t-include-it-s-software-what-can-i-do-to-make-it-work>

It will ask if you want to 'Repack packages from rootfs?', please press 'n' and then enter. This will download SliTaz packages from the internet and make a custom live distribution usable with BootTorrent.

We only need the final Kernel image and the initrd file which are generated in this process. These files are rootcd/boot/bzImage and rootcd/boot/rootfs.gz, please copy these files from this Virtual Machine or computer and place them inside boottorrent/assets/ph1 directory.

To build the client TUI, execute:

.. code-block:: console

    $ cd phase1bootstrap
    $ make initrd

This will create the assets and place them at proper locations in the repository.

Install
~~~~~~~

First, check if you have a compatible version (>3.6) of Python.

.. code-block:: console

    $ python --version
    Python 3.6.5

Otherwise, look at your distribution's documentation to install it or use tools such as `pyenv`_.

.. _`pyenv`: https://github.com/pyenv/pyenv

You can install BootTorrent just for your account (this doesn't require sudo) with pip:

.. code-block:: console

    $ pip install --user <repository path>

You can also do a global install with pip:

.. code-block:: console

    $ sudo pip install <repository path>

If BootTorrent conflicts with your previously installed packages. You can use `virtualenv`_ to setup a virtual environment and install inside it:

.. code-block:: console

    $ virtualenv -p python3.6 venv
    $ source venv/bin/activate
    $ pip install <repository path>

.. _virtualenv: https://github.com/pypa/virtualenv

From Pip
--------

First, check if you have a compatible version (>3.6) of Python.

.. code-block:: console

    $ python --version
    Python 3.6.5

Otherwise, look at your distribution's documentation to install it or use tools such as `pyenv`_.

.. _`pyenv`: https://github.com/pyenv/pyenv

After installing runtime dependencies, to install BootTorrent, you can install it just for your account (this doesn't require sudo) with pip:

.. code-block:: console

    $ pip install --user git+https://github.com/shreyanshk/boottorrent

You can also do a global install with pip:

.. code-block:: console

    $ sudo pip install git+https://github.com/shreyanshk/boottorrent

If BootTorrent conflicts with your previously installed packages. You can use `virtualenv`_ to setup a virtual environment and install inside it:

.. code-block:: console

    $ virtualenv -p python3.6 venv
    $ source venv/bin/activate
    $ pip install git+https://github.com/shreyanshk/boottorrent

.. _virtualenv: https://github.com/pypa/virtualenv

These are the preferred methods to install BootTorrent, as they will always install the most recent release.

If you don't have `Pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Updating/Reinstalling
---------------------

First, please uninstall the previous version with these commands:

If you've installed BootTorrent locally only for the current user:

.. code-block:: console

    $ pip uninstall boottorrent

If you've installed BootTorrent globally (installed with sudo):

.. code-block:: console

    $ sudo pip uninstall boottorrent

Or, If you've used virtualenv:

.. code-block:: console

    $ source <path to virtualenv>/bin/activate
    $ pip uninstall boottorrent

Then, you can install BootTorrent back by any of the above methods.
