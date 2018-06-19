.DEFAULT_GOAL := initrd

initrd:
	@echo "Building assets now..."
	@env GOOS=linux GOARCH=386 go build tui.go
	@mkdir -p diff/sbin
	@mv tui diff/sbin/getty
	@echo "Packing assets into diff.gz";
	@bsdtar -c --format newc -f diff.gz --lzma -Cdiff .;
	@echo "Placing files in correct locations..."
	@cp diff.gz ../boottorrent/assets/ph1/diff.gz
	@cp diff.gz ../venv/bt_dummy/out/dnsmasq/ph1/diff.gz 2>/dev/null || :

unpackorig:
	@echo "Unpacking rootfs_orig.gz"
	@rm -rf rootfs;
	@mkdir rootfs;
	@fakeroot bsdtar -x -f rootfs_orig.gz -C ./rootfs;

.PHONY: initrd unpackorig
