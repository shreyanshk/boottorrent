BootTorrent uses these packages:

* aria2

* busybox
    | Provides various essential system utilities.

* kexec-tools

* qemu-x86_64

* slitaz-boot-scripts
    | Provides SliTaz specific init scripts.

* xdotool
    | Used to focus window after launching Xorg.

* xorg-server

* xorg-xf86-video-vesa
    | Video driver

If you want to add more packages, you can append the package names to ``distro-packages.list`` file.

For the list of all packages supported by SliTaz you can search `here <http://pkgs.slitaz.org/search.sh>`_.

.. (atrent) actually I'd like to add some package that could be useful, such as ssh (both client and server), netstat/ss, a small web browser (there was midori, but also ncurses ones would be good), mc (midnight commander), tmux, if it does not fatten the image size, anyway let's stay minimal and let the user customize
