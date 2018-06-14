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

BootTorrent allows distributed P2P BitTorrent based network booting of various Operating systems.

The advantage of BootTorrent over standard network booting is that the bottleneck caused by a central server serving the image is reduced and BootTorrent reduces the linear scaling factor in total time to bring a cluster online fully functional by utilizing Peer-to-Peer protocol. The nodes share the image data among themselves, hence, improved boot times.

If you have considerable number of independent computers at your disposal and you’re looking to simply deploy any given System image(s) (that may have been hand-crafted according to your needs), such as that of a compute node for an HPC/ML cluster, over the whole network, consider BootTorrent. Upgrading is also as simple as rebooting the nodes in the network after the upgrade has started seeding from the central computer.

.. |img1| image:: http://sl-lab.it/dokuwiki/lib/exe/fetch.php/tesi:txmedia_paper.png
.. |img2| image:: http://sl-lab.it/dokuwiki/lib/exe/fetch.php/tesi:seed-ratio_paper.png
.. |img3| image:: http://sl-lab.it/dokuwiki/lib/exe/fetch.php/tesi:tempiboot_paper.png

+------+------+------+
||img1|||img2|||img3||
+------+------+------+
[Images & Data courtesy of SL-Lab: http://sl-lab.it/dokuwiki/lib/exe/fetch.php/tesi:tesi_bruschi.pdf]

**WARNING: STATUS - ALPHA: DO NOT USE IN PRODUCTION!**

* Free software: GNU General Public License v3
* Documentation: https://boottorrent.readthedocs.io.

Architecture
------------

* TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. (atrent) also refer to usecases, usecases are NOT referenced in any other file, why?!?

.. (shreyansh) I'll write usecases in simpler terms for a new user. They were linked before but were too technical, link you previously said. I'll rewrite and put them back as soon as I get an opportunity.

Features
--------

* TODO

