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

.. (atrent) why mentioning diskless nodes? it's not the main advantage

BootTorrent allows you to easily transfer and execute an Operating System image over the network to your distributed cluster of computers via BitTorrent’s distributed protocol while giving you central manageability of the said Operating system image. Upgrading is as simple as rebooting the nodes in the network after the upgrade has started seeding from the central computer.

.. (atrent) Speed and bottlenecks avoidance should be mentioned soon. The phrase "upgrading..." does not mean something special



If you have considerable number of independent computers at your disposal and you’re looking to simply deploy any given System image(s) (that may have been hand-crafted according to your needs), such as that of a compute node for an HPC/ML cluster, over the whole network, consider BootTorrent.

.. (atrent) still waiting for the main feature...


The advantage of BootTorrent over standard network booting is that the bottleneck caused by a central server serving the image is reduced and BootTorrent removes the linear scaling factor in total time to bring a cluster online fully functional by utilizing Peer-to-Peer protocol. The nodes share the image data among themselves, hence, improved boot times.

.. (atrent) at last! but it should be the first concept



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

Features
--------

* TODO

