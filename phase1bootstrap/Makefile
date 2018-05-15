.DEFAULT_GOAL := pack

pack:
	@echo "Packing folder rootfs into rootfs.gz";
	@rm rootfs.gz
	@fakeroot bsdtar -c --format cpio -f rootfs.gz --lzma rootfs

unpack:
	@echo "Unpacking rootfs_orig.gz"
	@rm -rf rootfs;
	@mkdir rootfs;
	@fakeroot bsdtar -x -f rootfs_orig.gz -C ./rootfs;

.PHONY: pack unpack
