Use the oss/ directory to store the files of the operating systems in their own sub-directories.
Please add an additional config.yaml with relevant fields to all the subfolders.
The fields allowed in the config.yaml file include:

**Common fields**

* dispname
    | type: string, required
    | The friendly name to display for the OS.

* method
    | type: string, required
    | The method via which the OS is to be loaded.
    | Valid values include: [kexec bin bin-qemu-x86_64]

**Fields for Linux/Kexec**

* kernel
    | type: string, required
    | The name of the kernel file.

* initrd
    | type: string, required
    | The name of the initrd file.

* cmdline
    | type: cmdline
    | Kernel cmdline to append to the kernel.

**Fields for Qemu-x86_64**

* args
    | type: string, required
    | This string is directly passed to the Qemu binary as an argument and can include all the parameters accepted by Qemu.

**Fields for bin**

* bin
    | type: string, required
    | This is the path to binary relative to the base directory of the OS

* binargs
    | type: string
    | These are the CLI arguments passed to the binary.

Once you add an OS here, please also update your Boottorrent.yaml file accordingly.

Example: Adding a Linux based OS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With a compiled kernel (vmlinuz) and corresponding initrd (initramfs.img), the process is:

1. Create a new directory.
2. Drop OS related files into the directory.
3. Add a file config.yaml with content (modify according to your needs):

.. code-block:: yaml

    dispname: TestOS # Friendly name to display
    method: kexec
    kernel: vmlinuz
    initrd: initramfs.img
    cmdline: break # cmdline for the new kernel

Example: Adding an OS that runs on Qemu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to use a floppy disk image (test.img) with Qemu, the process is:

1. Create a new directory.
2. Drop OS related files into the directory.
3. Add a file config.yaml with content (modify according to your needs):

.. code-block:: yaml

    dispname: TestOnQemu # Friendly name to display
    method: bin-qemu-x86_64
    args: "-fda test.img" # Arguments to pass to Qemu

Example: Adding an ISO file to BootTorrent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to boot a guest OS from an ISO file (disc.iso), the process is:

1. Create a new directory.
2. Drop the ISO file into the directory.
3. Add a file config.yaml with content (modify according to your needs):

.. code-block:: yaml

    dispname: ISOFile # Friendly name to display
    method: bin-qemu-x86_64
    args: "-cdrom disc.iso" # Arguments to pass to Qemu

Hint: You might want to enable KVM ("-accel kvm") if you're using Qemu as this will give you better performance. You can read full `Qemu documentation`_ for more information.

.. _Qemu documentation: https://qemu.weilnetz.de/doc/qemu-doc.html

Example: Adding a binary to launch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may want to do some housekeeping in the base environment before launching the OS. BootTorrent allows you to run a binary to take care of that on the nodes. To add a binary (named hello), the process is:

1. Create a new directory.
2. Drop the files and binary into the directory.
3. Add a file config.yaml with content (modify according to your needs):

.. code-block:: yaml

    dispname: TestBin # Friendly name to display
    method: bin
    bin: hello
    binargs: "<binary args>"
