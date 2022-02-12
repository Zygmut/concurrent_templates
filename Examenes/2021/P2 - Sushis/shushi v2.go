//By: Jorge Gonzalez
package main

import (
	"fmt"
	"math/rand"
	"time"
)

//Estructura vacia
type Empty struct{}
type PiezaSushi struct {
	tipo string
	n    int
}

const (
	CLIENTES = 4 //Numero de "amigos"
)

//Tipos de nombres
var nombre = [CLIENTES]string{"Pepe", "Maria", "Lucia", "Pedro"}

//Tipos de sushi
var sushi = []string{"Nigiri salmon", "Sashimi Atun", "Makis de cangrejo", "Shasimi de anguila",
	"Nigiris de tortilla"}
//var sushi = []string{"Nigiri salmon"}
var bandejaSushi = []PiezaSushi{}

//Canales
var pedirShusi = make(chan int) //Canal para dar sushi
//var okSushi = make(chan Empty) 		//Canal para que el cliente pueda comer
var okSushi [CLIENTES]chan PiezaSushi //Canal para que los clientes puedan comer

var finComer = make(chan int)     //Canal para avisar que ya ha acabado de comer
var okfinComer = make(chan Empty) //Canal ack del finComer

func servidor(done chan Empty) {
	//VARIABLES: 
	//Array de personas esperando
	var esperando [CLIENTES]int
	//Inicializamos el array: 0 Clientes esperando
	for i := range esperando {
		esperando[i] = 0
	}
	cli_esperando := 0
	cli_comiendo := false

	//FUNCIONES:
	//Funcion que da un sushi aleatorio a una cliente
	giveRandomPiezaSushi := func(id int) {
		i := 0
		if len(bandejaSushi) > 1 { // Si queda mas de una pieza se la damos random, Si no sera: 0
			i = rand.Intn(len(bandejaSushi) - 1) 
		}
		//Le damos la pieza al cliente
		okSushi[id] <- bandejaSushi[i]

		//Quitamos un sushi de ese tipo
		bandejaSushi[i].n--

		fmt.Printf("---> Todavia quedan %d tipos de sushi\n", len(bandejaSushi))

		//Si no quedan mas
		if bandejaSushi[i].n == 0 {
			fmt.Printf("---> %s se ha acabado el ultimo %s\n", nombre[id], bandejaSushi[i].tipo)
			//Lo quitamos
			bandejaSushi = append(bandejaSushi[:i], bandejaSushi[i+1:]...)
		}
	}

	//BUCLE Servidor
	for {
		select {
		case id := <-pedirShusi:
			//Si hay alguien comiendo
			if cli_comiendo {
				cli_esperando++
				esperando[id] = 1
			} else {
				//Este cliente puede comer
				cli_comiendo = true

				//Le damos un sushi al cliente
				giveRandomPiezaSushi(id)
			}

		case <-finComer:
			//El cliente ya no come
			cli_comiendo = false
			okfinComer <- Empty{}

			//Si hay alguien que espera y quedan shushis
			if cli_esperando > 0 && len(bandejaSushi) > 0 {
				//El primero segun el id podra comer
				for i := range esperando {
					if esperando[i] == 1 {
						esperando[i] = 0
						cli_esperando--
						//Le damos un sushi al primer cliente que esperaba
						giveRandomPiezaSushi(i)
						break
					}
				}
			}
		}
	}
}


//Go rutina Cliente (Amigo)
func cliente(id int, cliente string, done chan Empty) {

	//Mientras haya sushi
	for len(bandejaSushi) > 0 {

		pedirShusi <- id          //Pide un sushi
		piezaShushi := <- okSushi[id] //Espera a que se lo de
		fmt.Printf("%s coge un %s, todavia quedan %d\n", cliente, piezaShushi.tipo, piezaShushi.n)

		time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)

		finComer <- id //Avisamos de que hemos acabado de comer
		<- okfinComer  //Ok fin
	}
	//Fin del proceso
	done <- Empty{}
}

func main() {

	done := make(chan Empty) //Canal para finalizar

	//Random seed
	rand.Seed(time.Now().UTC().UnixNano())

	//Llenado de bandeja de sushi
	for i := 0; i < len(sushi); i++ {
		nPiezas := 1 + rand.Intn(10)
		fmt.Printf("%d: piezas de %s\n", nPiezas, sushi[i])
		bandejaSushi = append(bandejaSushi, PiezaSushi{sushi[i], nPiezas})
	}

	//InIt canal piezas sushi
	for i:= range okSushi {
		okSushi[i] = make(chan PiezaSushi)
	}
	fmt.Printf("Buen provecho\n")

	//Start go rutinas:
	go servidor(done)

	//Clientes
	for i := 0; i < len(nombre); i++ {
		fmt.Printf("Hola mi nombre es %s y vengo a comer sushi.\n", nombre[i])
		//exit [i] = make(chan Empty)
		go cliente(i, nombre[i],done)
	}

	//Esperamos a que los clientes acaben
	for i := 0; i < len(nombre); i++ {
		<-done
	}
	fmt.Printf("Simulación acabada\n")
}
