package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	fmt.Println("vim-go-test")
	bufio.NewReader(os.Stdin).ReadBytes('\n')
}
