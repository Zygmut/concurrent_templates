package main

import (
    "fmt"
    "runtime"
    "time"
)

const (
    Procs            = 8
    Enanos           = 7
    MaxNumberOfMeals = 2

    Sit    = 1
    Hungry = 2
    GTFO   = 3
)

var (
    nombreEnanos = []string{"Hermenegildo", "Hugo", "Hector", "Eructo", "Fulgencio", "UwU", "OwO"}
    enanos       [Enanos]chan Empty
)

type Empty struct{}

type Request struct {
    id     int
    status int
}

func enan(id int, done chan Empty, mayordomo chan Request) {
    //Canal para recibir mensajes del proveedor
    enanos[id] = make(chan Empty)

    eat := func() {
        fmt.Printf("%s come \n", nombreEnanos[id])
        time.Sleep(1500 * time.Millisecond)
        fmt.Printf("%s acaba de comer \n", nombreEnanos[id])
    }
    mining := func() {
        fmt.Printf("%s minea \n", nombreEnanos[id])
        time.Sleep(5000 * time.Millisecond)
    }
    complain := func() {
        fmt.Printf("%s wants to fucking GTFO\n", nombreEnanos[id])
        time.Sleep(1000 * time.Millisecond)
    }
    plsCanISit := func() {
        mayordomo <- Request{id: id, status: Sit}
        <-enanos[id]
    }
    plsCanIEat := func() {
        mayordomo <- Request{id: id, status: Hungry}
        <-enanos[id]
    }
    plsCanIStandUp := func() {
        mayordomo <- Request{id: id, status: GTFO}
        <-enanos[id]
    }
    fmt.Printf("Soy el enano: %s \n", nombreEnanos[id])
    for i := 0; i < MaxNumberOfMeals; i++ {
        mining()
        //Si no puede sentarse se quedarÃ¡ bloqueado
        plsCanISit()
        plsCanIEat()
        eat()
        complain()
        plsCanIStandUp()
        fmt.Printf("%s se levanta y vuelve a la mina\n", nombreEnanos[id])

    }
    fmt.Printf("++++++++++ ACABA el enano %s !!!\n", nombreEnanos[id])
    done <- Empty{}
}
func butler(channel chan Request) {

    esperen := [Enanos]int{0, 0, 0, 0, 0, 0, 0}
    available := 4
    canSit := func() bool {
        return available > 0
    }
    check_waiting := func() int {
        for i := 0; i < Enanos; i++ {
            if esperen[i] != 0 {
                return i
            }
        }
        return -1
    }

    for {
        rq := <-channel

        switch rq.status {
        case Sit:
            if canSit() {
                fmt.Printf("***** El mayordomo le da una silla a %s  \n", nombreEnanos[rq.id])
                available--
                enanos[rq.id] <- Empty{}
            } else {
                fmt.Printf("***** El enano %s no puede sentarse y se queda esperando\n", nombreEnanos[rq.id])
                esperen[rq.id] = 1
            }
        case Hungry:
            fmt.Printf("***** El mayordomo le da al enano %s un plato de comida\n", nombreEnanos[rq.id])
            enanos[rq.id] <- Empty{}
        case GTFO:
            enanos[rq.id] <- Empty{}
            fmt.Printf("Sillas disponibles %d", available)
            if !canSit() {
                wd := check_waiting()
                if wd != -1 {
                    fmt.Printf("***** El mayordomo le da permiso al enano %s para levantarse y le da la silla al %s \n", nombreEnanos[rq.id], nombreEnanos[wd])
                    esperen[wd] = 0
                    enanos[wd] <- Empty{}

                }
            }
            available++
        }

    }
}
func main() {
    runtime.GOMAXPROCS(Procs)
    done := make(chan Empty, 1)
    alfonsinChan := make(chan Request)

    for i := 0; i < Enanos; i++ {
        go enan(i, done, alfonsinChan)
    }
    go butler(alfonsinChan)
    for i := 0; i < Enanos; i++ {
        <-done
    }
}