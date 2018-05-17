.DEFAULT_GOAL := pack

initrd:
	@echo "Adding/Replacing content of diff and rootfs_orig.gz into rootfs.gz";
	@bsdtar -c --format cpio -f rootfs.gz @rootfs_orig.gz -Cdiff .;

initrd_compressed:
	@echo "(Compressed) Adding/Replacing content of diff and rootfs_orig.gz into rootfs.gz";
	@bsdtar -c --format cpio -f rootfs.gz --lzma @rootfs_orig.gz -Cdiff .;

unpackorig:
	@echo "Unpacking rootfs_orig.gz"
	@rm -rf rootfs;
	@mkdir rootfs;
	@fakeroot bsdtar -x -f rootfs_orig.gz -C ./rootfs;

.PHONY: initrd initrd_compressed unpackorig
