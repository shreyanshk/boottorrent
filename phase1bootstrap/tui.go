package main

import (
	"bufio"
	"fmt"
	"github.com/jroimartin/gocui"
	"golang.org/x/sys/unix"
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"
)


// Some useful structs
// Exportable/Public variables in Golang start with capitals.
// Variables starts with capitals so that goyaml can parse them.

// configs.yaml is parsed into an array of this struct.
type OS struct {
	// Common to all
	Dispname string
	Method string

	// fields required for kexec
	Cmdline string
	Initrd string
	Kernel string

	// fields required for bin-qemu-x86_64
	Args string

	// fields required for qemu-iso
	Isofile string
}


// Conveniently misses fields for stuff that is probably not needed on client.
type Conf struct {
	Boottorrent struct {
		Version int
		Timeout int
		Seed_time int
		Default_os string
		Host_ip string
		Display_os []string
	}
	Aria2 struct {
		Bt_enable_lpd bool
		Enable_peer_exchange bool
	}
}


// Globals to load and store only configuration
// 'btconfig' stores unmarshalled Boottorrent.yaml
// 'osconfig' stores unmarshalled configs.yaml
// 'display' is a map of friendly name to it's key in osconfig
// 'bool_t' is used to control timer
var btconfig = Conf{}
var osconfig = make(map[string]OS)
var display_names = make(map[string]string)
var bool_t bool


// function to launch the OS
func start(oskey string) {
	download_files(oskey)
	method := osconfig[oskey].Method
	switch method {
	case "kexec":
		load_kexec(oskey)
	case "bin-qemu-x86_64":
		load_bin_qemu_x86_64(oskey)
		// Ctrl+Alt+Backspace terminates Xorg
		// Added wait so that logs can be checked
		bufio.NewReader(os.Stdin).ReadBytes('\n')
	case "qemu-iso":
		load_qemu_iso(oskey)
		// Ctrl+Alt+Backspace terminates Xorg
		// Added wait so that logs can be checked
		bufio.NewReader(os.Stdin).ReadBytes('\n')
	default:
		fmt.Println("Unsupported method! Aborting.")
		bufio.NewReader(os.Stdin).ReadBytes('\n')
	}
}


// function to download the files via aria2 command
func download_files(oskey string) {
	aria2 := exec.Command(
		"/usr/bin/aria2c",
		"--check-integrity",
		"--allow-overwrite=true",
		"--enable-dht=false",
		"--enable-dht6=false",
		"--disable-ipv6=true",
		"--bt-enable-lpd=" + strconv.FormatBool(btconfig.Aria2.Bt_enable_lpd),
		"--seed-time=" + strconv.Itoa(btconfig.Boottorrent.Seed_time/60),
		"--file-allocation=prealloc",
		"--dir=/torrents",
		"/torrents/"+oskey+".torrent",
	)
	aria2.Stdout = os.Stdout
	aria2.Stderr = os.Stderr
	aria2.Run()
}


// function to seed the downloaded files
func seed_files(oskey string) *exec.Cmd {
	aria2 := exec.Command(
		"/usr/bin/aria2c",
		"--check-integrity",
		"--enable-dht=false",
		"--enable-dht6=false",
		"--disable-ipv6=true",
		"--bt-enable-lpd=" + strconv.FormatBool(btconfig.Aria2.Bt_enable_lpd),
		"--seed-ratio=0.0",
		"--file-allocation=prealloc",
		"--dir=/torrents",
		"/torrents/"+oskey+".torrent",
	)
	aria2.Run()
	return aria2
}


// Method string: kexec
// function handling Kexec-ing of new kernels
func load_kexec(oskey string) {
	runconfig := osconfig[oskey]
	// Kexec-ing new kernel now
	kexec := exec.Command(
		"/usr/sbin/kexec",
		"-l", "/torrents/"+oskey+"/"+runconfig.Kernel,
		"--append=\""+runconfig.Cmdline+"\"",
		"--initrd", "/torrents/"+oskey+"/"+runconfig.Initrd,
	)
	kexec.Stdout = os.Stdout
	kexec.Stderr = os.Stderr
	kexec.Run()
	// Clear terminal
	fmt.Println("\033[H\033[2J")
	kexec2 := exec.Command("/usr/sbin/kexec", "-e")
	kexec2.Stdout = os.Stdout
	kexec2.Stderr = os.Stderr
	kexec2.Run()
}


// Method string: bin-qemu-x86_64
// function to start Qemu process under Xorg
func load_bin_qemu_x86_64(oskey string) {
	c := osconfig[oskey]
	xorg := exec.Command("/usr/bin/Xorg")
	xorg.Stdout = os.Stdout
	xorg.Stderr = os.Stderr
	xorg.Start()
	// wait for Xorg to load
	time.Sleep(1 * time.Second)
	qemu := exec.Command("/usr/bin/qemu-system-x86_64")
	qemu.Args = append(qemu.Args, strings.Fields(c.Args)...)
	// Qemu requires this env variable
	qemu.Env = []string{"DISPLAY=:0"}
	qemu.Dir = "/torrents/" + oskey
	qemu.Stdout = os.Stdout
	qemu.Stderr = os.Stderr
	qemu.Start()
	// now start seeding
	seedp := seed_files(oskey)
	xorg.Wait()
	qemu.Process.Kill()
	seedp.Process.Kill()
}


// Method string: qemu-iso
// function to start Qemu process with ISO file under Xorg
func load_qemu_iso(oskey string) {
	c := osconfig[oskey]
	xorg := exec.Command("/usr/bin/Xorg")
	xorg.Stdout = os.Stdout
	xorg.Stderr = os.Stderr
	xorg.Start()
	// wait for Xorg to load
	time.Sleep(1 * time.Second)
	qemu := exec.Command("/usr/bin/qemu-system-x86_64")
	fields := "-cdrom " + c.Isofile
	qemu.Args = append(qemu.Args, strings.Fields(fields)...)
	// Qemu requires this env variable
	qemu.Env = []string{"DISPLAY=:0"}
	qemu.Dir = "/torrents/" + oskey
	qemu.Stdout = os.Stdout
	qemu.Stderr = os.Stderr
	qemu.Start()
	// now start seeding
	seedp := seed_files(oskey)
	xorg.Wait()
	qemu.Process.Kill()
	seedp.Process.Kill()
}


// function to execute when event KeyArrowDown is received
func cursorDown(g *gocui.Gui, v *gocui.View) error {
	if v != nil {
		cx, cy := v.Cursor()
		// check if the cursor can go down
		if l, err := v.Line(cy+1); err != nil || len(l) == 0 {
			return nil
		}
		// set new cursor position
		if err := v.SetCursor(cx, cy+1); err != nil {
			ox, oy := v.Origin()
			if err := v.SetOrigin(ox, oy+1); err != nil {
				return err
			}
		}
	}
	return nil
}


// function to execute when event KeyArrowUp is received
func cursorUp(g *gocui.Gui, v *gocui.View) error {
	if v != nil {
		ox, oy := v.Origin()
		cx, cy := v.Cursor()
		// check if the cursor can go up
		if l, err := v.Line(cy-1); err != nil || len(l) == 0 {
			return nil
		}
		// set new cursor position
		if err := v.SetCursor(cx, cy-1); err != nil && oy > 0 {
			if err := v.SetOrigin(ox, oy-1); err != nil {
				return err
			}
		}
	}
	return nil
}


// function to read the line in the OS list
// and start it's corresponding OS.
func getLine(g *gocui.Gui, v *gocui.View) error {
	var l string
	var err error

	// Read line at the location of the cursor
	_, cy := v.Cursor()
	if l, err = v.Line(cy); err != nil {
		panic(err)
	}
	if len(l) == 0 {
		panic("The line has zero length! This should not happen. Aborting!")
	}
	disableTimer(g, v)
	g.Close()
	oskey := display_names[l]
	start(oskey)
	return nil
}


// function to disable timer
func disableTimer(g *gocui.Gui, v *gocui.View) error {
	bool_t = false
	err := g.DeleteView("timer")
	if err != nil && err != gocui.ErrUnknownView {
		panic(err)
	}
	return nil
}


// function to handle Ctrl+C on the program
func quit(g *gocui.Gui, v *gocui.View) error {
	g.Close()
	err := unix.Exec("/bin/busybox", []string{"-ash"}, os.Environ())
	if err != nil {
		panic("Failed to launch shell.")
	}
	return gocui.ErrQuit
}


// Set the keybindings on the interface.
func keybindings(g *gocui.Gui) error {
	if err := g.SetKeybinding("list", gocui.KeyArrowDown, gocui.ModNone, cursorDown); err != nil {
		return err
	}
	if err := g.SetKeybinding("list", gocui.KeyArrowUp, gocui.ModNone, cursorUp); err != nil {
		return err
	}
	if err := g.SetKeybinding("list", gocui.KeyCtrlS, gocui.ModNone, quit); err != nil {
		return err
	}
	if err := g.SetKeybinding("list", gocui.KeyCtrlC, gocui.ModNone, disableTimer); err != nil {
		return err
	}
	if err := g.SetKeybinding("list", gocui.KeyEnter, gocui.ModNone, getLine); err != nil {
		return err
	}
	return nil
}


// Function responsible for creating the User Interface.
func layout(g *gocui.Gui) error {
	vw, vh := g.Size()
	maxlen := 0
	// Finding max length of the list to display so as to center the screen
	// Also populates display_names variable.
	for k, v := range osconfig {
		dname := v.Dispname
		l := len(dname)
		display_names[dname] = k
		if l > maxlen {
			maxlen = l
		}
	}
	// set field to display timer
	if bool_t {
		if v, err := g.SetView(
			"timer", 1, 0, vw-1, 3,
		); err != nil {
			v.Highlight = false
			v.Frame = false
		}
	}
	// display information
	if v, err := g.SetView(
		"info", 1, vh-3, vw-1, vh,
	); err != nil {
		v.Highlight = false
		v.Frame = false
		fmt.Fprintln(v, "Ctrl+S: Launch shell | Ctrl+C: disable timer")
	}
	// Calculating the coordinates of a centered rectangle in which
	// options will be displayed on screen.
	topleftx := (vw/2) - maxlen/2 - 1
	toplefty := (vh/2) - len(display_names)/2 - 2
	bottomrightx := (vw/2) + maxlen/2 + 1
	bottomrighty := (vh/2) + len(display_names)/2 + 2
	// display the list
	if v, err := g.SetView(
		"list",
		topleftx,
		toplefty,
		bottomrightx,
		bottomrighty,
	); err != nil {
		v.Highlight = true
		v.Frame = false
		v.SelBgColor = gocui.ColorGreen
		v.Autoscroll = true
		for k, _ := range display_names {
			fmt.Fprintln(v, k)
		}
		if _, err := g.SetCurrentView("list"); err != nil {
			return err
		}
	}
	return nil
}


func main() {
	// This block sets global variables.
	boottorrent, err := ioutil.ReadFile("/torrents/Boottorrent.yaml")
	if err != nil {
		fmt.Println("Couldn't read Boottorrent.yaml file!")
		panic(err)
	}
	err = yaml.Unmarshal([]byte(boottorrent), &btconfig)
	if err != nil {
		fmt.Println("Couldn't parse Boottorrent.yaml!")
		panic(err)
	}
	configs, err := ioutil.ReadFile("/torrents/configs.yaml")
	if err != nil {
		fmt.Println("Couldn't read configs.yaml file!")
		panic(err)
	}
	err = yaml.Unmarshal([]byte(configs), &osconfig)
	if err != nil {
		fmt.Println("Couldn't parse configs.yaml!")
		panic(err)
	}

	timeout := btconfig.Boottorrent.Timeout

	if timeout == 0 {
		start(btconfig.Boottorrent.Default_os)
	}

	// This block sets up the TUI
	g, err := gocui.NewGui(gocui.OutputNormal)
	if err != nil {
		panic(err)
	}

	g.SetManagerFunc(layout)

	if err := keybindings(g); err != nil {
		panic(err)
	}

	// this block handles the timer
	if timeout < 0 {
		bool_t = false
	} else {
		bool_t = true
		ticker := time.NewTicker(1 * time.Second)
		go func() {
			// iterate timeout times to wait for user input
			for i := timeout; i > 0; i-- {
				// check if ticker was disabled from interface
				if !bool_t {
					ticker.Stop()
					return
				}
				// schedule an update to the interface
				updfunc := func(g *gocui.Gui) error {
					v, err := g.View("timer")
					if err == nil {
						v.Clear()
						fmt.Fprintln(
							v,
							"Booting default OS in "+strconv.Itoa(i)+" seconds...",
						)
					}
					return nil
				}
				g.Update(updfunc)
				// wait for next tick
				<-ticker.C
			}
			// timeout passed... now loading OS
			bool_t = false
			ticker.Stop()
			g.Close()
			start(btconfig.Boottorrent.Default_os)
			os.Exit(0)
		}()
	}

	// this block starts the main event loop
	if err := g.MainLoop(); err != nil && err != gocui.ErrQuit {
		panic(err)
	}
}
