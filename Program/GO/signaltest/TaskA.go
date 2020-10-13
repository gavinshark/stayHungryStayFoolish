package main

import (
	"fmt"
	"time"
)

type TaskA struct {

}

func (Task *TaskA) Init() bool {
	fmt.Printf("TaskA Init\n")
	return true
}

func (Task *TaskA) GetInitTimeout() int {
	return 10
}

func (Task *TaskA) Work() int {
	fmt.Printf("woker A Start : current time is %s\n", time.Now().UTC())
	time.Sleep(time.Duration(10) * time.Second)
	fmt.Printf("woker A End   : current time is %s\n", time.Now().UTC())
	return 10
}