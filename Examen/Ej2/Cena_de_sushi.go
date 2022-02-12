// Rubén Palmer Pérez

package main

import (
	"log"       // o log para printear
	"math/rand" // Para generación de numeros aleatorios
	"time"      // sleep
)

//Constantes
const (
	CLIENT_COUNT     = 4

	// Control de velocidades
	CLIENT_MAX_TIME = 2
	CLIENT_MIN_TIME = 1

	WANT_SUSHI = 0
	EATING_SUSHI = 1

	SERVER_NAME = "Server"
)

//Estructuras
type Empty struct{} // Done

type Request struct{ // Requests al servidor
	id int
	state int
}

type sushi_piece struct{ // Elementos de nuestra tabla de sushis
	sushi_type  string 
	n 	 	    int
}

//Variables
var (
	wait 		= make(chan int) // Bloquear procesos
	request_chan  = make(chan Request)                                                      //Canal de peticiones al servidor que hacen los clientes
	ack_chans      [CLIENT_COUNT]chan Empty                                                       // Respuestas del servidor a los clientes individualmente
	client_names = [CLIENT_COUNT]string{"Alberto", "Jorge", "Pablo", "Pau"} 
	sushi_types  = [] string {"nigiri de salmon", "sashimi de atun", "maki de cangrejo", "sashimi de anguila", "nigiri de trucha"} 
	sushis		 = [] sushi_piece {}
)

//Servidor
func Servidor() { // SEQUENCIALIZAR EL ACCESO A LA TABLA DE SUSHI
	waiting_requests := [] Request{}
	current_grab := -1
	for {

		request := <- request_chan
		switch request.state{
			case WANT_SUSHI:
				if current_grab == -1 { // First request. accept
					current_grab = request.id
					ack_chans[request.id] <- Empty{}
				}else{
					if len(waiting_requests) == 0{ // Si no hay en la cola de
						current_grab = request.id
						ack_chans[request.id] <- Empty{}
					}else{
						waiting_requests = append(waiting_requests, request) // Lo añadimos a la cola 
					}
				}
			case EATING_SUSHI:
				// Le damos permiso para comer 
				ack_chans[request.id] <- Empty{}
				if len(waiting_requests) != 0{ // Si hay requests esperando
					ack_chans[waiting_requests[0].id] <- Empty{} // Le damos permiso para coger
					current_grab = waiting_requests[0].id
					waiting_requests = append(waiting_requests[:0], waiting_requests[1:]...) // Eliminamos el primero de la cola 

				}
		}	

	}
}


func Cliente(id int, done chan Empty) {
	//Inicilizacion del canal de espera personal de cada cliente
	ack_chans[id] = make(chan Empty)

	//Variables
	velocidad := CLIENT_MIN_TIME + rand.Intn(CLIENT_MAX_TIME-CLIENT_MIN_TIME)

	//Funciones
	coger_sushi := func() {

		// Como el servidor solo gestiona un estado (Poder coger sushi) no hace falta que hagamos un struct "Request"
		request_chan <- Request{id, WANT_SUSHI}  
		<- ack_chans[id]

		if len(sushis) != 0{
			random := rand.Intn(len(sushis))
			sushis[random].n-- // eliminamos 1 del sushis seleccionado
			log.Printf("[%s] Coge un %s, quedan %d", client_names[id], sushis[random].sushi_type, sushis[random].n)
			if sushis[random].n < 1{
				log.Printf("[%s] Ha cogido el ultimo %s", client_names[id], sushis[random].sushi_type)
				sushis = append(sushis[:random], sushis[random+1:]...) 
			}

			request_chan <- Request{id, EATING_SUSHI} // Hacemos request para decirle que ya hemos cogido y vamos a comer
			<- ack_chans[id]
		}
	}

	//Metodo para esperar
	wait := func(wait_time int) {
		time.Sleep(time.Duration(wait_time) * time.Second)
	}

	log.Printf("[%s] Vengo a comer sushi y mi velocidad es: %d", client_names[id], velocidad)
	// Mientras haya sushis
	for len(sushis) != 0{

		// Pedir la pieza de sushi al Servidor
		coger_sushi()
		// Comer
		wait(velocidad)
	}

	// Acabamos
	done <- Empty{} 
}

func main() {
	rand.Seed(time.Now().UnixNano())

	for i := 0; i < len(sushi_types); i++ {
		sushis = append(sushis, sushi_piece{sushi_types[i], 1 + rand.Intn(10)})
		log.Printf("%d de %s",sushis[i].n, sushis[i].sushi_type)
	}

	done := make(chan Empty) 

	for i := 0; i < CLIENT_COUNT; i++ {
		go Cliente(i, done)
	}
	go Servidor()

	for i:=0; i<CLIENT_COUNT; i++ {
		<- done 
	}
	log.Printf("Muy rico todo\n")
}