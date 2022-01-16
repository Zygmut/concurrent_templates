// Barrera binaria con canales asincronos
//2 Procesos
/*  
Comunicacion asincrona: el Remitente envia el
mensaje i continua sin bloquearse i el Receptor
puede ejecutar cualquier sentencia cuando envia
el mensaje y despues comprueba el canal para los 
mensajes. Necesita un BUFFER
*/
package main

import (
    "fmt"
)

const (
    Phases = 20
)

func A(done, a, b chan bool) {
    for i := 0; i < Phases; i++ {
        a <- true
        fmt.Println("A finished phase", i)
        <-b
    }
    fmt.Println("Finished thread A")
    done <- true
}

func B(done, a, b chan bool) {
    for i := 0; i < Phases; i++ {
        b <- true
        fmt.Println("B finished phase", i)
        <-a
    }
    fmt.Println("Finished thread B")
    done <- true
}

func main() {
    done := make(chan bool)
    a := make(chan bool, 1)
    b := make(chan bool, 1)
    go A(done, a, b)
    go B(done, a, b)
    
    //Esperar a que acaben
    <-done
    <-done
    
    fmt.Printf("End\n")
}
