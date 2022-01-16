// Barreras Generales para N procesos

package main

import (
    "fmt"
    "math/rand"
    //"runtime"
    "time"
)

const (
    //Procs      = 4
    Phases     = 20
    Goroutines = 10
)

type Barrier struct {
    arrival   chan int
    departure chan int
    n         int
}

func NewBarrier(value int) *Barrier {
    b := new(Barrier)
    b.arrival = make(chan int, 1)
    b.departure = make(chan int, 1)
    b.n = value
    b.arrival <- value
    return b
}

func (b *Barrier) Barrier() {
    var v int
    //ARRIBAR
    //Espera arrival (llegada) amb missatge
    v = <-b.arrival
    if v > 1 {//Queden processos per arribar
        v--
        b.arrival <- v //Un menys per arribar
    } else {
        b.departure <- b.n //Han arribat tots
    }
    //SORTIR
    //Espera departure (salida) amb missatge
    v = <-b.departure
    if v > 1 {//Queden processos per sortir
        v--
        b.departure <- v //Un menys per sortir
    } else {
        b.arrival <- b.n //Han sortit tots
    }
}

func run(id int, done chan bool, b *Barrier) {
    for i := 0; i < Phases; i++ {
        time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)
        b.Barrier()//Totes Goroutines han d'acabar la fase i
        fmt.Printf("%d finished phase %d\n", id, i)
    }
    b.Barrier() //Acaben Totes les Goroutines
    fmt.Printf("Finished thread %d\n", id)
    done <- true
}

func main() {
    //GOMAXPROCS per indicar el nombre de threads del sistema per defecte 1
    //runtime.NumCPU() //Per indicar el màxim del sistema
    //runtime.GOMAXPROCS(Procs) // Es pot virtualizar CPUs
    start := time.Now()
    done := make(chan bool, 1)
    barrier := NewBarrier(Goroutines)
    for i := 0; i < Goroutines; i++ {
        go run(i, done, barrier)
    }
    for i := 0; i < Goroutines; i++ {
        <-done
    }
    fmt.Printf("End\n")
    elapsed := time.Since(start)
    fmt.Printf("Temps emprat %s", elapsed)
}
