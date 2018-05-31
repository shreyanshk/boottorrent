.DEFAULT_GOAL := pack

initrd:
	@echo "Adding content of diff into diff.gz";
	@bsdtar -c --format newc -f diff.gz -Cdiff .;

initrd_compressed:
	@echo "(Compressed) Adding content of diff into diff.gz";
	@bsdtar -c --format newc -f diff.gz --lzma -Cdiff .;

unpackorig:
	@echo "Unpacking rootfs_orig.gz"
	@rm -rf rootfs;
	@mkdir rootfs;
	@fakeroot bsdtar -x -f rootfs_orig.gz -C ./rootfs;

.PHONY: initrd initrd_compressed unpackorig
