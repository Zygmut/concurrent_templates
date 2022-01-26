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
	ack_chans      [CLIENT_COUNT]chan int                                                       // Respuestas del servidor a los clientes individualmente
	client_names = [CLIENT_COUNT]string{"Alberto", "Jorge", "Pablo", "Pau"} 
	sushi_types  = [] string {"nigiri de salmon", "sashimi de atun", "maki de cangrejo", "sashimi de anguila", "nigiri de trucha"} 
	sushis		 = [] sushi_piece {}
)

//Servidor
func Servidor() { // SEQUENCIALIZAR EL ACCESO A LA TABLA DE SUSHI
	someone_picking := false
	clients_waiting := [] Request {}


	for {

		request := <- request_chan
		
		switch request.id{
			case WANT_SUSHI:
				if len(sushis) == 0{ // Si no hay sushis 
					ack_chans[request.id] <- -1  // No hay mas sushi
					for i := 0; i <len(clients_waiting); i++{
						ack_chans[clients_waiting[i].id] <- -1 // No hay mas  
					}
				}else{
					if someone_picking{ // Si alguien esta cogiendo sushi
						clients_waiting = append(clients_waiting, request) // Lo añadimos a la cola de gente 
					}else{
						someone_picking = true
						ack_chans[request.id] <- 0 // Le damos permiso
					}
					
				}
			case EATING_SUSHI:
				log.Printf("len clien: %d", len(clients_waiting)) 
				someone_picking = false
				if len(sushis)==0{ // SI no hay sushis avisamos a todos de que no hay
					for i := 0; i <len(clients_waiting); i++{
						ack_chans[clients_waiting[i].id] <- -1 // No hay mas  
					}
					ack_chans[request.id] <- -1
				}else{
					ack_chans[request.id] <- 0
					
					if len(clients_waiting) != 0{ // Si hay clientes esperando
						ack_chans[clients_waiting[0].id] <- 0 // Le damos permiso para coger
						someone_picking = true

						clients_waiting = append(clients_waiting[:0], clients_waiting[1:]...) // Eliminamos la posicion 0 del array
					}else{
					}
				}

		}

	}
}

func Cliente(id int, done chan Empty) {
	//Inicilizacion del canal de espera personal de cada cliente
	ack_chans[id] = make(chan int)

	//Variables
	velocidad := CLIENT_MIN_TIME + rand.Intn(CLIENT_MAX_TIME-CLIENT_MIN_TIME)

	//Funciones
	coger_sushi := func() {

		// Como el servidor solo gestiona un estado (Poder coger sushi) no hace falta que hagamos un struct "Request"
		request_chan <- Request{id, WANT_SUSHI}  
		// Esperamos a que nos confirme

		response := <-ack_chans[id] // El servidor puede decirnos que no hay mas 
		if response == -1{
			log.Printf("ME voy %s", client_names[id])
			done <- Empty{}
			<- wait  // nunca se mete nada dentro de este canal -> se queda bloqueado 
		}

		random := rand.Intn(len(sushis))
		own_sushi := sushis[random] // Cogemos el sushis que queramos
		own_sushi.n-- // eliminamos 1 del sushis seleccionado
		sushis[random].n = own_sushi.n
		log.Printf("[%s] Coge un %s, quedan %d", client_names[id], own_sushi.sushi_type, own_sushi.n)
		if own_sushi.n == 0{
			log.Printf("[%s] Ha cogido el ultimo %s", client_names[id], own_sushi.sushi_type)
			sushis = append(sushis[:random], sushis[random+1:]...) 
		}

		
		request_chan <- Request{id, EATING_SUSHI} // Hacemos request para decirle que ya hemos cogido y vamos a comer
		response = <-ack_chans[id] // El servidor puede decirnos que no hay mas 
		if response == -1{
			log.Printf("ME voy %s", client_names[id])
			done <- Empty{}
			<- wait  // nunca se mete nada dentro de este canal -> se queda bloqueado 
		}
	}

	//Metodo para esperar
	wait := func(wait_time int) {
		time.Sleep(time.Duration(wait_time) * time.Second)
	}

	log.Printf("[%s] Vengo a comer sushi y mi velocidad es: %d", client_names[id], velocidad)
	// Mientras haya sushis
	for len(sushis) > 0{

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
	log.Printf("End\n")
}