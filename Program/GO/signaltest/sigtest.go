package main

import (
    "fmt"
    "os"
    "os/signal"
    "sync"
    "syscall"
    "time"
)

func WorkerFunc(id int) int{
    fmt.Printf("woker %d: current time is %s\n", id, time.Now().UTC())
    return id
}

func WorkerDelegator(wg *sync.WaitGroup, id int){
    defer wg.Done()

    ch := make(chan os.Signal, 1)
    signal.Notify(ch, syscall.SIGHUP, syscall.SIGQUIT, syscall.SIGTERM, syscall.SIGKILL)

    timeAfter := id
    for {
        select {
        case <- time.After(time.Duration(timeAfter) * time.Second):
            timeAfter = WorkerFunc(id)
        case sig := <-ch:
            fmt.Printf("worker %d: Listened event sig:%s\n", id, sig)
            return
        }
        fmt.Printf("worker %d: timeAfter %d\n", id, timeAfter)
    }
}

func main() {
    var wg sync.WaitGroup

    for id := 1; id < 3; id++ {
        fmt.Printf("Main: Start working with goroutinge %d\n", id)
        wg.Add(1)
        go WorkerDelegator(&wg, id)
    }

    fmt.Println("Main: Waiting for workers to finish")
    wg.Wait()
    fmt.Println("Main: Completed")
}
