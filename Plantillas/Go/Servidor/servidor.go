package main

import (
	"fmt"       // o log para printear
	"math/rand" // Para generación de numeros aleatorios
	"time"      // sleep
)

//Constantes
const (
	Clientes     = 7 //Clientes que piden al servidor
	Repeticiones = 2 //Numero de veces de la accion

	// Control de velocidades
	cliente_max_time = 5
	cliente_min_time = 1

	//Posibles tipos de las peticiones:
	Estado1 = 1
	Estado2 = 2
	Estado3 = 3
)

//Estructuras
type Empty struct{}

type Peticion struct {
	id   int //Id del proceso
	tipo int //Estado de peticion

	// En algunos casos puede ser interesante pasarle un canal en la petición
}

//Variables
var (
	peticionServer  = make(chan Peticion)                                                      //Canal de peticiones al servidor que hacen los clientes
	okClientes      [Clientes]chan Empty                                                       // Respuestas del servidor a los clientes individualmente
	
	cliente_nombres = [Clientes]string{"cli1", "cli2", "cli3", "cli4", "cli5", "cli6", "cli7"} // En caso de que los clientes tengan nombres, se accede a este array
)

//Servidor
func servidor() {
	for {
		peticion := <-peticionServer

		switch peticion.tipo {
		case Estado1:
			fmt.Println("******* Servidor: Confirma Accion 1")
			//Mirar condicion a aceptar la peticion
			okClientes[peticion.id] <- Empty{} //Damos la confirmacion al cliente
		case Estado2:
			fmt.Println("******* Servidor: Confirma Accion 2")
			//Mirar condicion a aceptar la peticion
			okClientes[peticion.id] <- Empty{} //Damos la confirmacion al cliente
		case Estado3:
			fmt.Println("******* Servidor: Confirma Accion 3")
			//Mirar condicion a aceptar la peticion
			okClientes[peticion.id] <- Empty{} //Damos la confirmacion al cliente
		}
	}
}

func cliente(id int, done chan int) {
	//Inicilizacion del canal de espera personal de cada cliente
	okClientes[id] = make(chan Empty)

	//Variables
	velocidad := cliente_min_time + rand.Intn(cliente_max_time-cliente_min_time)

	//Funciones
	accion1 := func() {
		fmt.Printf("****** %s: Pide Accion 1\n", cliente_nombres[id])

		//Mandamos peticion
		peticionServer <- Peticion{id, Estado1}
		//Esperamos a que nos confirme
		<-okClientes[id]
	}

	accion2 := func() {
		fmt.Printf("****** %s: Pide Accion 2\n", cliente_nombres[id])

		//Mandamos peticion
		peticionServer <- Peticion{id, Estado2}
		//Esperamos a que nos confirme
		<-okClientes[id]
	}

	accion3 := func() {
		fmt.Printf("****** %s: Pide Accion 3\n", cliente_nombres[id])

		//Mandamos peticion
		peticionServer <- Peticion{id, Estado3}
		//Esperamos a que nos confirme
		<-okClientes[id]
	}

	//Metodo para esperar
	wait := func(wait_time int) {
		time.Sleep(time.Duration(wait_time) * time.Second)
	}

	//Acciones que hace el Cliente
	for i := 0; i < Repeticiones; i++ {
		accion1()
		wait(velocidad)

		accion2()
		wait(velocidad)

		accion3()
		wait(velocidad)
	}
	done <- id
}

func main() {
	rand.Seed(time.Now().UnixNano())

	done := make(chan int) //Sincrono
	//done := make(chan Vacio, 1) //Asincrono

	for i := 0; i < Clientes; i++ {
		go cliente(i, done)
	}
	go servidor()

	for i := 0; i < Clientes; i++ {
		nombre := cliente_nombres[<-done]
		fmt.Printf("*** %s:  Se va\n", nombre)
	}

	fmt.Printf("End\n")
}