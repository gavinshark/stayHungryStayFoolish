package main

import (
	"fmt"
)

type MyStruct struct {
   name string
   kind int
}

var items = [...]MyStruct{
   {"Lucy", 1},
   {"Kelly", 2},
   {"Mike", 1},
}

func main() {
   for _, item := range items {
     fmt.Printf("name:%v, kind:%v\n", item.name, item.kind)
   }
}