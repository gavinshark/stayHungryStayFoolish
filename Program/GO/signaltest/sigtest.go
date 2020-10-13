package main

import (
    "fmt"
    "os"
    "os/signal"
    "reflect"
    "sync"
    "syscall"
    "time"
)

type Task interface {
    Init () bool
    GetInitTimeout () int
    Work () int
}

func WorkerDelegator(wg *sync.WaitGroup, task Task){
    defer wg.Done()

    taskName := reflect.TypeOf(task).String()
    fmt.Printf("%s start\n", taskName)

    ch := make(chan os.Signal, 1)
    signal.Notify(ch, syscall.SIGHUP, syscall.SIGQUIT, syscall.SIGTERM, syscall.SIGKILL)

    timeAfter := task.GetInitTimeout()
    for {
        select {
        case <- time.After(time.Duration(timeAfter) * time.Second):
            timeAfter = task.Work()
        case sig := <-ch:
            fmt.Printf("%s: Listened event sig:%s\n", taskName, sig)
            return
        }
        fmt.Printf("%s: timeAfter %d\n", taskName, timeAfter)
    }
}

func main() {
    var wg sync.WaitGroup

    var taskList = [...]Task{
        new(TaskA),
        new(TaskB),
    }

    for _, task := range taskList {
        task.Init()
        wg.Add(1)
        go WorkerDelegator(&wg, task)
    }

    fmt.Println("Main: Waiting for workers to finish")
    wg.Wait()
    fmt.Println("Main: Completed")
}
