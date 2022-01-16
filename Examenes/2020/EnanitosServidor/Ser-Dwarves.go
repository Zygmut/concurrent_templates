// Rubén 

package main

import (
	"log"
	"time"
	"math/rand"
)

const(
	DWARF_COUNT = 7
	DWARF_SHIFT_COUNT = 2
	DWARF_MIN_TIME = 1
	DWARF_MAX_TIME = 5
	CHAIR_COUNT = 4

	SIT = 0
	EAT = 1
	GET_UP = 2
	BUTLER_NAME = "ALFREDO"

)

type Empty struct{}

type Request struct{
	id		  int 
	status	  int
}

var (
	DWARF_NAMES = []string{"Bashful", "Doc", "Dopey", "Grumpy", "Happy", "Sleepy", "Sneezy"}
	DWARF_EARS [DWARF_COUNT] chan Empty 
)


func butler(butler_ear chan Request){

	avaliable_chairs := CHAIR_COUNT
	dwarf_waiting := [] int {0,0,0,0,0,0,0}

	can_sit := func() bool{
		return avaliable_chairs > 0 
	}

	check_waiting := func() int{
		for i := 0; i <DWARF_COUNT; i++{
			if dwarf_waiting[i] != 0{
				return i
			}
		}
		return -1
	}

	for{
		rq := <- butler_ear
		switch rq.status{
			case SIT:
				if can_sit(){
					avaliable_chairs --
					log.Printf("%s: Hace sentar a %s", BUTLER_NAME, DWARF_NAMES[rq.id])
					DWARF_EARS[rq.id] <- Empty{}
				}else{
					log.Printf("%s: Hace esperar a %s, todas las sillas estan ocupadas", BUTLER_NAME, DWARF_NAMES[rq.id])
					dwarf_waiting[rq.id] = 1
				}

			case EAT:
				log.Printf("%s: Sirve a %s", BUTLER_NAME, DWARF_NAMES[rq.id])
				DWARF_EARS[rq.id] <- Empty{}

			case GET_UP:
				log.Printf("%s: Le da permiso para levantarse a %s", BUTLER_NAME, DWARF_NAMES[rq.id])
				DWARF_EARS[rq.id] <- Empty{}

				if !can_sit(){ // Si alguien no se pudiese sentar actualmente
					
					// Nadie se puede sentar
					waiting_dwarf := check_waiting()
					if waiting_dwarf != -1{ // Mirar si hay alguien esperando 
						log.Printf("%s: Hace sentar a %s en la silla de %s", BUTLER_NAME, DWARF_NAMES[waiting_dwarf], DWARF_NAMES[rq.id] )
						dwarf_waiting[waiting_dwarf] = 0
						DWARF_EARS[waiting_dwarf] <- Empty{}
					}else{
						avaliable_chairs ++ 
					}
				}
		}

	}

}

func dwarf(id int, done chan int, butler chan Request){
	DWARF_VEL := DWARF_MIN_TIME + rand.Intn(DWARF_MAX_TIME - DWARF_MIN_TIME) 

	DWARF_EARS[id] = make(chan Empty)


	wait := func (wait_time int){
		time.Sleep(time.Duration(wait_time) * time.Second)
	}

	goto_mine := func(){
		log.Printf("%s: Trabaja en la mina", DWARF_NAMES[id])
		wait(DWARF_VEL)
	}

	sit := func(){
		log.Printf("%s: Llega de la mina y espera una silla", DWARF_NAMES[id])
		butler <- Request{id, SIT}
		<- DWARF_EARS[id]
	}

	eat := func(){
		log.Printf("%s: Se sienta y pide ser servido", DWARF_NAMES[id])
		butler <- Request{id, EAT}
		<- DWARF_EARS[id]
		log.Printf("%s: Come", DWARF_NAMES[id])
		wait(DWARF_VEL)
	}

	get_up := func(){
		log.Printf("%s: Ha acabado de comer y pide permiso para levantarse", DWARF_NAMES[id])
		butler <- Request{id, GET_UP}
		<- DWARF_EARS[id]
	}

	log.Printf("%s: Init", DWARF_NAMES[id])
	for i:=0; i <DWARF_SHIFT_COUNT; i++{
		// Va a la mina 
		goto_mine()

		// Piden permiso para sentarse
		sit()

		// Piden permiso para comer
		eat()

		// Piden permiso para levantarse
		get_up()
	}

	done <- id 
}

func main() {
	// Random Seed
	rand.Seed(time.Now().UnixNano())

	// Canales
	done := make(chan int) 		// Canal de salida

	butler_ear := make(chan Request)


	// Lanzar enanos y el mayordomo	
	for i:=0; i <DWARF_COUNT; i++{
		go dwarf(i, done, butler_ear)
	}	
	
	go butler(butler_ear)


	for i:=0; i<DWARF_COUNT; i++{
		log.Printf("%s: Se va", DWARF_NAMES[<-done]) 
	}
}