package main

import (
	"fmt"
	"github.com/jroimartin/gocui"
	"gopkg.in/yaml.v2"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"strconv"
)

// Some useful structs
// Variables starts with capital so that goyaml can parse them

// configs.yaml is parsed into an array of this struct.
type OS struct {
	Cmdline string
	Dispname string
	Initrd string
	Kernel string
	Method string
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
		Check_integrity bool
		Enable_dht bool
		Enable_dht6 bool
		Enable_peer_exchange bool
	}
}

// Globals to load and store only configuration
// 'btconfig' stores unmarshalled Boottorrent.yaml
// 'osconfig' stores unmarshalled configs.yaml
// 'display' is a map of friendly name to it's key in osconfig
var btconfig = Conf{}
var osconfig = make(map[string]OS)
var display_names = make(map[string]string)


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


// function to read the line in the OS list.
func getLine(g *gocui.Gui, v *gocui.View) error {
	var l string
	var err error

	_, cy := v.Cursor()
	if l, err = v.Line(cy); err != nil {
		panic(err)
	}
	g.Close()
	if len(l) == 0 {
		panic("The line has zero length! This should not happen. Aborting!")
	}
	fmt.Println("About to start the process...")
	start(l)
	return nil
}


// function to launch the OS
func start(l string) {
	// Preparing to download the torrent
	oskey := display_names[l]
	aria2 := exec.Command(
		"aria2c",
		"--enable-dht=" + strconv.FormatBool(btconfig.Aria2.Enable_dht),
		"--enable-dht6=" + strconv.FormatBool(btconfig.Aria2.Enable_dht6),
		"--bt-enable-lpd=" + strconv.FormatBool(btconfig.Aria2.Bt_enable_lpd),
		"--disable-ipv6=true",
		"--seed-time=" + strconv.Itoa(btconfig.Boottorrent.Seed_time/60),
		"--file-allocation=prealloc",
		"--allow-overwrite=true",
		"--dir=/",
		"-j5",
		"/torrents/"+oskey+".torrent",
	)
	aria2.Stdout = os.Stdout
	aria2.Stderr = os.Stderr
	aria2.Run()
	runconfig := osconfig[oskey]
	// Kexec-ing new kernel now
	kexec := exec.Command(
		"kexec",
		"-l", "/"+oskey+"/"+runconfig.Kernel,
		"--append=\""+runconfig.Cmdline+"\"",
		"--initrd", "/"+oskey+"/"+runconfig.Initrd,
	)
	kexec.Stdout = os.Stdout
	kexec.Stderr = os.Stderr
	kexec.Run()
	// Clear terminal
	fmt.Println("\033[H\033[2J")
	kexec2 := exec.Command("kexec", "-e")
	kexec2.Stdout = os.Stdout
	kexec2.Stderr = os.Stderr
	kexec2.Run()
}


// function to handle Ctrl+C on the program
func quit(g *gocui.Gui, v *gocui.View) error {
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
	if err := g.SetKeybinding("", gocui.KeyCtrlC, gocui.ModNone, quit); err != nil {
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
		if err != gocui.ErrUnknownView {
			return err
		}
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

	// This block starts the TUI
	g, err := gocui.NewGui(gocui.OutputNormal)
	if err != nil {
		log.Panicln(err)
	}

	g.SetManagerFunc(layout)

	if err := keybindings(g); err != nil {
		log.Panicln(err)
	}

	if err := g.MainLoop(); err != nil && err != gocui.ErrQuit {
		log.Panicln(err)
	}
}
