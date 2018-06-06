.DEFAULT_GOAL := initrd

initrd:
	@go build tui.go
	@mkdir -p diff/sbin
	@mv tui diff/sbin/getty
	@echo "(Compressed) Adding content of diff into diff.gz";
	@bsdtar -c --format newc -f diff.gz --lzma -Cdiff .;
	@cp diff.gz ../boottorrent/assets/ph1/diff.gz

unpackorig:
	@echo "Unpacking rootfs_orig.gz"
	@rm -rf rootfs;
	@mkdir rootfs;
	@fakeroot bsdtar -x -f rootfs_orig.gz -C ./rootfs;

.PHONY: initrd initrd_compressed unpackorig
