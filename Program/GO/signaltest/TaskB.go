package main

import (
	"fmt"
	"time"
)

type TaskB struct {

}

func (Task *TaskB) Init() bool {
	fmt.Printf("TaskB Init\n")
	return true
}

func (Task *TaskB) GetInitTimeout() int {
	return 20
}

func (Task *TaskB) Work() int {
	fmt.Printf("woker B Start : current time is %s\n", time.Now().UTC())
	time.Sleep(time.Duration(2) * time.Second)
	fmt.Printf("woker B End   : current time is %s\n", time.Now().UTC())
	return 2
}