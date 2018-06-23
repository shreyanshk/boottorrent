.. highlight:: shell

============
Installation
============

Dependencies
------------

Components this project depends on include:

* `Python 3.6`_

* `Transmission`_

* `Dnsmasq`_

* `bsdtar`_ (provided by libarchive)

* `Hefur`_ (Optional)

.. _Transmission: https://github.com/transmission/transmission
.. _Dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _Hefur: https://github.com/abique/hefur
.. _Python 3.6: https://www.python.org/
.. _bsdtar: http://www.libarchive.org/

The package itself depends on a few Python libraries which are installed automatically by Pip package manager. These libraries are:

.. (atrent) so 'pip' is a dependency, right?

* `Click`_

* `PyYAML`_

* `Jinja2`_

* `Requests`_

.. _Click: http://click.pocoo.org/
.. _PyYAML: https://github.com/yaml/pyyaml
.. _Jinja2: http://jinja.pocoo.org/
.. _Requests: http://docs.python-requests.org/en/master/

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

**You can skip this section because it is only for documentation purpose as these resources are currently checked in with the repository**

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

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
