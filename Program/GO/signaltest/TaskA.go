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
	return 1
}

func (Task *TaskA) Work() int {
	fmt.Printf("woker A: current time is %s\n", time.Now().UTC())
	return 1
}