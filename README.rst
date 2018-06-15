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

The advantage of BootTorrent over standard network booting is that the bottleneck caused by a central server serving the image is reduced and BootTorrent reduces the linear scaling factor in total time to bring a cluster online fully functional by utilizing Peer-to-Peer protocols. The nodes share the image data among themselves, hence, improved boot times.

Cases where BootTorrent may be useful would be:

* If the clients in your network are not getting enough bandwidth individually and have significant bandwidth being left unused, which causes increased boot times. With BootTorrent you can repurpose the remaining bandwidth to help clients mutually share it among themselves.

* If your server (such as a laptop) can only connect to your cluster of computers via a comparatively slow link (such as WiFi or Fast-ethernet) then BootTorrent can help you mitigate the low bandwidth issues of network link.

* If you have large number of computers at your disposal and you're simply looking to deploy any given system image(s) (that may have been hand-crafted according to your needs) as painlessly as possible. BootTorrent can help you deploy it in `three easy steps <https://boottorrent.readthedocs.io/en/latest/quickstart.html>`_ to the whole network.

* If your current network boot server is unable to meet your requirements and deliver much needed performance, consider giving BootTorrent a try. It's distributed architecture will reduce the dependence on server, which means improved boot performance.

For more details on use cases please refer to `Use cases list <https://boottorrent.readthedocs.io/en/latest/usecases.html>`_ and visit the `documentation <https://boottorrent.readthedocs.io/en/latest/index.html>`_.

We have data to back our claims. Check out the performance improvements here:

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

Features
--------

* TODO

