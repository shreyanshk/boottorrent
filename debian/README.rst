To build the package, the following packages are needed:

* debhelper
* dh-python
* python3-all
* python3-setuptools
* python3-pip
* python3-wheel
* python3-shpinx
* python3-sphinxcontrib.seqdiag
* python3-sphinxcontrib.blockdiag
* dnsmasq
* aria2
* mktorrent
* python3 (>= 3.6)
* python3-jinja2
* python3-yaml

You can install them with this command:

.. code-block:: console

        # apt install debhelper dh-python python3-all python3-pip python3-sphinx python3-sphinxcontrib.seqdiag python3-sphinxcontrib.blockdiag dnsmasq aria2 mktorrent python3-jinja2 python3-yaml

Then, you can build the package with this command:

.. code-block:: console

        $ cd boottorrent
        $ dpkg-buildpackage

This should create boottorrent_*.tar.gz package file. This file can be install with this command:

Note: substitute correct version number.

.. code-block:: console

        # dpkg -i boottorrent_*.tar.gz
