package main

import (
	"log"       // o log para printear
	"math/rand" // Para generación de numeros aleatorios
	"time"      // sleep
)

//Constantes
const (
	BEE_COUNT    = 5 // IF THIS CHANGE; CHANGE BEE_NAMES VALUES TO ADD NEW NAMES 

	BEAR_TIMES 	= 3 

	// Control de velocidades
	BEE_MAX_TIME = 5
	BEE_MIN_TIME = 1

	BEAR_MIN_TIME = 1
	BEAR_MAX_TIME = 2

	POT_SIZE = 10

	//Posibles tipos de las peticiones:
	GIVE_HONEY = 1 // Bee request
	AWAIT_POT = 2 // bear request
	BEAR_SLEEP = 3
	WAKE_BEAR = 4

	BEAR_NAME = "Gilgamesh"
	SERVER_NAME = "Konyaskaya"
)

//Estructuras
type Empty struct{}

type Request struct {
	id   		int 			// Id del proceso
	state 		int			    // Estado de peticion
}

//Variables
var (
	request_chan  = make(chan Request)    
	bear_chan     = make(chan int)                                                  //Canal de peticiones al servidor que hacen los clientes
	client_names  = []string{"Arjuna", "Ganesha", "Orion", "Karna", "Olimpus"}
	pot           = 0
	bees_perm       [BEE_COUNT]chan Empty
)


func wait(wait_time int){
	time.Sleep(time.Duration(wait_time) * time.Second)
}

func Pot(){
	bees_waiting :=[]int{0,0,0,0,0,0,0}	
	bear_eating := false 
	local_pot := 0
	last_bee := 0
	wake_bees := func(){
		for i := 0; i <BEE_COUNT;i++{
			if bees_waiting[i] != 0{
				bees_waiting[i] = 0
				log.Printf("[%s]: Wakes %s", SERVER_NAME, client_names[i])
				local_pot += 1
				bees_perm[i] <- Empty{}
			}
		}
	}

	for{
		request := <- request_chan
		switch request.state{
			case GIVE_HONEY: // Bee request
				if !bear_eating{
					if local_pot == POT_SIZE{
						log.Printf("[%s]: The pot is full, wait",SERVER_NAME)
						bees_waiting[request.id] = 1
					}else{
						local_pot += 1
						bees_perm[request.id] <- Empty{}
					} 
				}else{
					bees_waiting[request.id] = 1
					log.Printf("[%s]: %s is eating, fuck off %s", SERVER_NAME, BEAR_NAME, client_names[request.id])
				}

			case AWAIT_POT: // Bear request
				if pot == POT_SIZE{
					log.Printf("[%s]: The pot is ready", SERVER_NAME)
					bear_chan <- last_bee
					bear_eating = true
				}else{
					log.Printf("[%s]: The pot is not ready yet, fuck off", SERVER_NAME)
				}
			
			case BEAR_SLEEP: // Bear request
				log.Printf("[%s]: Rest tight %s", SERVER_NAME, BEAR_NAME)
				local_pot = 0
				bear_eating = false
				wake_bees()	
			

			case WAKE_BEAR: // Bee request
				if pot == POT_SIZE && !bear_eating {
					log.Printf("[%s]: %s can wake %s", SERVER_NAME, client_names[request.id], BEAR_NAME)
					bear_chan <- request.id 
					last_bee = request.id
					bear_eating = true
				}

				bees_perm[request.id] <- Empty{}
		}
	}
}

func Bear (done chan Empty) {

	bear_vel := BEAR_MIN_TIME + rand.Intn(BEAR_MAX_TIME - BEAR_MIN_TIME)


	eat_pot := func(){
		for i := 0; i <POT_SIZE; i++{
			pot -= 1
			wait(bear_vel)
		}
	}

	log.Printf("[%s]: Wants the pot filled", BEAR_NAME)

	for i:=0; i<BEAR_TIMES; i++{
		request_chan <- Request{-1,AWAIT_POT}
		bee_id := <- bear_chan // Si y solo si el bote esta lleno
		log.Printf("[%s]: Is woken up by %s & consumes the pot", BEAR_NAME, client_names[bee_id])

		eat_pot()
		if i != BEAR_TIMES-1 {
			request_chan <- Request{-1, BEAR_SLEEP}
			<- bear_chan // si o si se lo da
			log.Printf("[%s]: Goes to sleep", BEAR_NAME)	
		}
	}
	log.Printf("[%s]: Breaks the pot & leaves", BEAR_NAME)
	done <- Empty{}
}

func Bee(id int) {

	//Variables
	velocidad := BEE_MIN_TIME + rand.Intn(BEE_MAX_TIME-BEE_MIN_TIME)
	bees_perm[id] = make(chan Empty)
	
	//Funciones
	give_honey := func() {
		log.Printf("[%s]: Creates honey", client_names[id])
		wait(velocidad)

		//Mandamos peticion
		request_chan <- Request{id, GIVE_HONEY} 
		//Esperamos a que nos confirme
		<- bees_perm[id] // Si y solo si el bote no esta lleno y el oso no esta comiendo, sino espera
		pot += 1
		log.Printf("[%s]: Puts honey in the pot [%d/%d]", client_names[id], pot, POT_SIZE)

		request_chan <- Request{id, WAKE_BEAR}
		<- bees_perm[id]
	}


	//Acciones que hace el Cliente
	log.Printf("[%s]: Init", client_names[id])
	for {

		give_honey()

	}
}

func main() {
	rand.Seed(time.Now().UnixNano())

	done := make(chan Empty) //Sincrono

	go Pot()

	for i := 0; i < BEE_COUNT; i++ {
		go Bee(i)
	}
	go Bear(done)

	<- done 
	log.Printf("End\n")
}