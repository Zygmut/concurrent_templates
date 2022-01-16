package main

import (
	"log"       // o log para printear
	"math/rand" // Para generación de numeros aleatorios
	"time"      // sleep
)

//Constantes
const (
	CLIENT_COUNT     = 7 
	CLIENT_TIMES 	 = 2 

	// Control de velocidades
	CLIENT_MAX_TIME = 5
	CLIENT_MIN_TIME = 1

	//Posibles tipos de las peticiones:
	STATE_1 = 1
	STATE_2 = 2
	STATE_3 = 3

	SERVER_NAME = "Server"
)

//Estructuras
type Empty struct{}

type Request struct {
	id   int //Id del proceso
	state int //Estado de peticion

	// En algunos casos puede ser interesante pasarle un canal en la petición
}

//Variables
var (
	request_chan  = make(chan Request)                                                      //Canal de peticiones al servidor que hacen los clientes
	ack_chans      [CLIENT_COUNT]chan Empty                                                       // Respuestas del servidor a los clientes individualmente
	client_names = [CLIENT_COUNT]string{"cli1", "cli2", "cli3", "cli4", "cli5", "cli6", "cli7"} // En caso de que los clientes tengan nombres, se accede a este array
)

//Servidor
func Servidor() {
	for {
		request := <-request_chan

		switch request.state {
		case STATE_1:
			log.Printf("[%s]: Confirma Accion 1", SERVER_NAME)
			//Mirar condicion a aceptar la request
			ack_chans[request.id] <- Empty{} //Damos la confirmacion al cliente
		case STATE_2:
			log.Printf("[%s]: Confirma Accion 2", SERVER_NAME)
			//Mirar condicion a aceptar la request
			ack_chans[request.id] <- Empty{} //Damos la confirmacion al cliente
		case STATE_3:
			log.Printf("[%s]: Confirma Accion 3", SERVER_NAME)
			//Mirar condicion a aceptar la request
			ack_chans[request.id] <- Empty{} //Damos la confirmacion al cliente
		}
	}
}

func Cliente(id int, done chan int) {
	//Inicilizacion del canal de espera personal de cada cliente
	ack_chans[id] = make(chan Empty)

	//Variables
	velocidad := CLIENT_MIN_TIME + rand.Intn(CLIENT_MAX_TIME-CLIENT_MIN_TIME)

	//Funciones
	accion1 := func() {
		log.Printf("[%s]: Pide Accion 1\n", client_names[id])

		//Mandamos peticion
		request_chan <- Request{id, STATE_1}
		//Esperamos a que nos confirme
		<-ack_chans[id]
	}

	accion2 := func() {
		log.Printf("[%s]: Pide Accion 2\n", client_names[id])

		//Mandamos peticion
		request_chan <- Request{id, STATE_2}
		//Esperamos a que nos confirme
		<-ack_chans[id]
	}

	accion3 := func() {
		log.Printf("[%s]: Pide Accion 3\n", client_names[id])

		//Mandamos peticion
		request_chan <- Request{id, STATE_3}
		//Esperamos a que nos confirme
		<-ack_chans[id]
	}

	//Metodo para esperar
	wait := func(wait_time int) {
		time.Sleep(time.Duration(wait_time) * time.Second)
	}

	//Acciones que hace el Cliente
	for i := 0; i < CLIENT_TIMES; i++ {
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

	for i := 0; i < CLIENT_COUNT; i++ {
		go Cliente(i, done)
	}
	go Servidor()

	for i := 0; i < CLIENT_COUNT; i++ {
		nombre := client_names[<-done]
		log.Printf("[%s]: Se va\n", nombre)
	}

	log.Printf("End\n")
}