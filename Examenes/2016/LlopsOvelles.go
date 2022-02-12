package main

import (
	"fmt"
	"math/rand"
	"time"
)

const (
	ovelles    = 4 // Nombre de processos ovella (ovelles)
	llops      = 5 // Nombre de processos llop
	iteracions = 1 // nombre d'iteracions de cada procés
)

type Empty struct{}

type RequestLlop struct {
	id      int
	my_chan chan Empty
}

// Random sleep between 0 til max
func sleep(max int) {
	time.Sleep(time.Duration(rand.Intn(max)) * time.Millisecond)
}

// Proveïdor
func proveidor(done chan Empty) {
	var esperantEntrada int // guarda l'identificador de l'ovella que està esperant per entrar
	var esperantSortida int // guarda l'identificador de l'ovella que està esperant per sotir
	llops := 0
	ovellesEnt := 0
	ovellesRiu := 0
	ovellesSor := 0

	for {
		time.Sleep(100 * time.Millisecond)
		select {

		case id := <-ovellaPermisEntrar: // ovelles que volen entrar
			fmt.Printf("L'ovella %d vol entrar al riu\n", id)
			ovellesEnt++

			if ovellesEnt == 1 { // si hi una ovella que vol entrar
				if ovellesRiu == 0 { // i encara no hi ha ningú dins el riu
					fmt.Printf("L'ovella %d ha d'esperar a una altra ovella per entrar!!\n", id)
					esperantEntrada = id // ha d'esperar

				} else { // si hi ha una ovella o més dins el riu, la deixam passar
					ovellesEnt--
					ovellesRiu++
					fmt.Printf("++ L'ovella %d pot entrar. Hi ha %d ovelles\n", id, ovellesRiu)
					ovellaEntra[id] <- Empty{} // y también a la que quiere entrar ahora

					if ovellesRiu == 3 && ovellesSor == 1 { // si ara tenim 3 ovelles dins el riu i una d'elles estava esperant per sortir
						ovellesRiu--
						ovellesSor--
						fmt.Printf("++ L'ovella %d que estava esperant ja pot sortir. Queden %d ovelles\n", esperantSortida, ovellesRiu)
						ovellaSurt[esperantSortida] <- Empty{} // dejamos entrar a la que estaba esperando
						esperantSortida = -1                   // la deixam sortir
					}
				}

			} else { // si hi ha dues ovelles que volen passar, les deixam passar a totes dues
				ovellesEnt = ovellesEnt - 2
				ovellesRiu++
				fmt.Printf("++ L'ovella %d pot entrar. Hi ha %d ovelles\n", id, ovellesRiu)
				ovellaEntra[id] <- Empty{} // y también a la que quiere entrar ahora
				ovellesRiu++
				fmt.Printf("++ L'ovella %d que estava esperant ja pot entrar. Hi ha %d ovelles\n", esperantEntrada, ovellesRiu)
				ovellaEntra[esperantEntrada] <- Empty{} // dejamos entrar a la que estaba esperando
				esperantEntrada = -1
			}

		case msg := <-llopEntra:
			llops++
			fmt.Printf("El llop %d entra al riu. Hi ha %d llops\n", msg.id, llops)
			msg.my_chan <- Empty{}

		case id := <-ovellaPermisSortir: // ovelles que volen sortir
			fmt.Printf("L'ovella %d vol SORTIR del riu\n", id)
			ovellesSor++

			if ovellesSor == 1 { // si una ovella vol sortir,
				if ovellesRiu <= 2 { // i nomes queda ella i una altra al riu
					fmt.Printf("L'ovella %d ha d'esperar a una altra ovella per sortir!!\n", id)
					esperantSortida = id // li feim esperar a la segona per sortir

				} else { // i hi ha més de dues ovelles dins el riu, la deixam sortir
					ovellesSor--
					ovellesRiu--
					fmt.Printf("++ L'ovella %d pot sortir. Queden %d ovelles\n", id, ovellesRiu)
					ovellaSurt[id] <- Empty{} // y también a la que quiere entrar ahora
				}

			} else { // hi ha dues ovelles que volen sortir, les deixam sortir a totes dues
				ovellesSor = ovellesSor - 2
				ovellesRiu--
				fmt.Printf("++ L'ovella %d pot sortir. Queden %d ovelles\n", id, ovellesRiu)
				ovellaSurt[id] <- Empty{} // y también a la que quiere entrar ahora
				ovellesRiu--
				fmt.Printf("++ L'ovella %d que estava esperant ja pot sortir. Queden %d ovelles\n", esperantSortida, ovellesRiu)
				ovellaSurt[esperantSortida] <- Empty{} // dejamos entrar a la que estaba esperando
				esperantSortida = -1
			}

		case msg := <-llopSurt:
			llops--
			fmt.Printf("El llop %d surt del riu. Queden %d llops\n", msg.id, llops)
			msg.my_chan <- Empty{}
		}
	}
}

// procés ovella
func ovella(id int, done chan Empty) {
	fmt.Printf("Hola sóc l'ovella %d\n", id)
	time.Sleep(100 * time.Millisecond)

	for i := 0; i < iteracions; i++ {
		// entra
		ovellaPermisEntrar <- id
		<-ovellaEntra[id]

		// beure
		fmt.Printf("L'ovella %d beu\n", id)
		sleep(700)

		// sortir
		ovellaPermisSortir <- id
		<-ovellaSurt[id]
	}

	time.Sleep(100 * time.Millisecond)
	fmt.Printf("Adéu ovella %d\n", id)
	done <- Empty{}
}

// procés llop
func llop(id int, done chan Empty) {
	var my_chan = make(chan Empty)
	fmt.Printf("Hola sóc el llop %d\n", id)
	time.Sleep(100 * time.Millisecond)

	for i := 0; i < iteracions; i++ {
		// entra
		llopEntra <- RequestLlop{id: id, my_chan: my_chan}
		<-my_chan

		// beure
		fmt.Printf("El llop %d beu\n", id)
		sleep(700)

		// sortir
		llopSurt <- RequestLlop{id: id, my_chan: my_chan}
		<-my_chan
	}

	time.Sleep(100 * time.Millisecond)
	fmt.Printf("Adéu llop %d\n", id)
	done <- Empty{}
}

var ovellaPermisEntrar = make(chan int)
var ovellaEntra [ovelles]chan Empty
var ovellaPermisSortir = make(chan int)
var ovellaSurt [ovelles]chan Empty

var llopEntra = make(chan RequestLlop)
var llopSurt = make(chan RequestLlop)

func main() {
	// Inicialitzam l'array de canals
	for i := range ovellaEntra {
		ovellaEntra[i] = make(chan Empty)
		ovellaSurt[i] = make(chan Empty)
	}

	done := make(chan Empty)

	go proveidor(done)

	//time.Sleep(100 * time.Millisecond)

	// inicialitzam tots els processos ovella
	for i := 0; i < ovelles; i++ {
		go ovella(i, done)
	}

	// inicialitzam tots els processos ovella
	for i := 0; i < llops; i++ {
		go llop(i, done)
	}

	// esperam a que acabin els processos ovella
	for i := 0; i < ovelles; i++ {
		<-done
	}

	// esperam a que acabin els processos ovella
	for i := 0; i < llops; i++ {
		<-done
	}

	fmt.Printf("\nEnd")
}
