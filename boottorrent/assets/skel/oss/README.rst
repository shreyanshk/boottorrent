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
    | Valid values include: [kexec bin-qemu-x86_64 qemu-iso]

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

**Fields for running from ISO files**

* isofile
    | type: string, required
    | The name of the ISO file that is to be run.


Once you add an OS here, please also update your Boottorrent.yaml file to include it.

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

    dispname: ISOFile
    method: qemu-iso
    isofile: disc.iso
