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
	return 2
}

func (Task *TaskB) Work() int {
	fmt.Printf("woker B: current time is %s\n", time.Now().UTC())
	return 2
}