package main

import (
    "fmt"
    "os"
    "os/signal"
    "syscall"
)


func main() {
    ch := make(chan os.Signal, 1)
    signal.Notify(ch, syscall.SIGHUP, syscall.SIGQUIT, syscall.SIGTERM, syscall.SIGKILL, syscall.SIGSTOP, syscall.SIGUSR1)
    for {
        s := <-ch
        switch s {
        case syscall.SIGQUIT:
            fmt.Printf("Singal Got: SIGQUIT\n")
            return
        case syscall.SIGSTOP:
            fmt.Printf("Singal Got: SIGSTOP\n")
            return
        case syscall.SIGHUP:
            fmt.Printf("Singal Got: SIGHUP\n")
            return
        case syscall.SIGTERM:
            fmt.Printf("Singal Got: SIGTERM\n")
            return
        case syscall.SIGKILL:
            fmt.Printf("Singal Got: SIGKILL\n")
            return
        case syscall.SIGUSR1:
            fmt.Printf("Singal Got: SIGUSR1\n")
            return
        default:
            fmt.Printf("Singal Got: default\n")
            return
        }
    }
}
