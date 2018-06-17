2018/06/15
~~~~~~~~~~

* Took a dive in the SliTaz ecosystem and learned how to properly
generate custom live images. Previously I was hacking away their base
image.
* Figured out how to setup Xorg and load Qemu on the custom image.
* Activated readthedocs.org to publish documentation. It is live at:
https://boottorrent.readthedocs.io
* Added Quick start guide, architecture, internals, frequently asked
questions sections and similar slew of updates.

2018/06/09
~~~~~~~~~~

This week has been mostly about documenting the project. Also, readying the project for a test run.

* There is now a functional user interface on clients.
* Refactored the TUI code to use Go-YAML and gocui

2018/06/02
~~~~~~~~~~

Got project to work end-to-end.
Was facing some problems with the clients being unable to discovery seeds but, finally, was able to sort it.

* Implemented basic TUI for clients in Golang.
* Implemented download and kexec on clients.
* Added Hefur as a tracker for the torrents.
* Pushed some documentation.
