.DEFAULT_GOAL := initrd

initrd:
	@echo "Building assets now..."
	@env GOOS=linux GOARCH=386 go build tui.go
	@mkdir -p diff/sbin
	@mv tui diff/sbin/bttui
	@rm -rf diff/sbin/getty
	@echo "Packing assets into diff.gz";
	@bsdtar -c --format newc -f diff.gz --lzma -Cdiff .;
	@echo "Placing files in correct locations..."
	@cp diff.gz ../boottorrent/assets/ph1/diff.gz
	@cp diff.gz ../envtest/out/dnsmasq/ph1/diff.gz 2>/dev/null || :

unpackorig:
	@echo "Unpacking rootfs_orig.gz"
	@rm -rf rootfs;
	@mkdir rootfs;
	@fakeroot bsdtar -x -f rootfs_orig.gz -C ./rootfs;

dldeps:
	@go get github.com/jroimartin/gocui
	@go get gopkg.in/yaml.v2
	@go get golang.org/x/sys/unix

.PHONY: dldeps initrd unpackorig
