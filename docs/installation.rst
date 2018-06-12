.. highlight:: shell

============
Installation
============

Dependencies (Runtime / Server)
-------------------------------

This project depends on:

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

Please check your distribution specific guide for instructions on how to install them.

Pre-Install: Building assets
----------------------------

**You can skip this section because it is only for documentation purpose as these resources are currently checked in with the repository**

Building assets requires additional software. This includes:

* `Golang`_ (For the client TUI)

.. _Golang: https://golang.org/

Some Golang dependencies are also required to build, you can download them with these commands:

.. code-block:: console

    $ go get github.com/jroimartin/gocui
    $ go get gopkg.in/yaml.v2

Then you can build.

.. code-block:: console

    $ cd phase1bootstrap
    $ make initrd

This will create the assets and place them at proper locations in the repository.

Install package
---------------

First, check if you have a compatible version (>3.6) of Python.

.. code-block:: console

    $ python --version
    Python 3.6.5

Otherwise, you can use tools such as `virtualenv`_, `pyenv`_, or `pipenv`_ to get Python 3.6

.. _`virtualenv`: https://github.com/pypa/virtualenv
.. _`pyenv`: https://github.com/pyenv/pyenv
.. _`pipenv`: https://github.com/pypa/pipenv

After installing runtime dependencies, to install BootTorrent, run this command in your terminal:

.. code-block:: console

    $ pip install git+https://github.com/shreyanshk/boottorrent

This is the preferred method to install BootTorrent, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
