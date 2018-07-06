2018/07/06
~~~~~~~~~~

* Merged method 'qemu-iso' into 'bin-qemu-x86_64'
* Add method 'bin' to execute binaries
* Detection of available OSs programmatically
* Slimed down SliTaz image (56 MiB -> 28 MiB)
* Add parameter aria2.console_log_level, remove display_oss
* Fixed bug of not highlighting correctly default OS

2018/06/30
~~~~~~~~~~

* Enable boot of ISO files with Qemu on client computers.
* Switched to Opentracker for the tracker service.
* Added code to verify the validity of input parameters.
* Removed DHT from the project on recommendation.
* In addition to client TUI, enabled additional shell (tty2).
* Few documentation updates and bug fixes.

2018/06/23
~~~~~~~~~~

* Added an option to launch a shell on the client
* Implemented a timer to load default OS on no user input
* Clean up of some code in the client
* updates to the documentation according to the suggestions of mentors and developments in the code

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
