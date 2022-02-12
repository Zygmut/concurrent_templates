//By: Jorge Gonzalez Pascual
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
	CLIENTES     = 4 //Numero de "amigos"
	TIPO_SHUSHIS = 5 //Numero de tipos de TIPO_SHUSHIS
)

//Tipos de nombres
var nombre = [CLIENTES]string{"Pepe", "Maria", "Lucia", "Pedro"}

//Tipos de shushi
var shushi = []string{"Nigiri salmon", "Sashimi Atun", "Makis de cangrejo", "Shasimi de anguila",
	"Nigiris de tortilla"}
var bandejaSushi = []PiezaSushi{}

//Canales
var pedirShusi = make(chan string)   //Canal para dar shushi
var darShusi = make(chan PiezaSushi) //Canal para dar la pieza de shushi

func servidor(done chan Empty) {
	for {
		nombreCliente := <-pedirShusi
		//Si quedan shushis
		if len(shushi) != 0 {
			//Eleguimos un shushi aleatorio de los que hay
			//NO SE HACER QUE NO DE POSICIONES ILEGALES, NO TENDIRA QUE PASAR
			i := rand.Intn(len(bandejaSushi))

			//Lo pasamos al cliente
			darShusi <- PiezaSushi{bandejaSushi[i].tipo, bandejaSushi[i].n}

			bandejaSushi[i].n-- //Quitamos un shushi de ese tipo

			fmt.Printf("---> Todavia quedan %d tipos de shushi\n", len(bandejaSushi))

			//Si no quedan mas
			if bandejaSushi[i].n == 0 {
				fmt.Printf("---> %s se ha acabado el ultimo %s\n", nombreCliente, bandejaSushi[i].tipo)
				//Lo quitamos
				bandejaSushi = append(bandejaSushi[:i], bandejaSushi[i+1:]...)
			}
			
			//Si era el ultimo de todos, terminamos
			if len(bandejaSushi) == 0 {
				done <- Empty{}
			}

		}

	}

}

func cliente(id int, cliente string) {

	//Mientras haya shushi
	for len(bandejaSushi) > 0 {

		pedirShusi <- cliente          //Pide un shushi
		nombreShushiDado := <-darShusi //Espera a que se lo de
		fmt.Printf("%s coge un %s, todavia quedan %d\n", cliente, nombreShushiDado.tipo, nombreShushiDado.n)

		time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)
	}

}

func main() {

	done := make(chan Empty) //Canal para finalizar

	rand.Seed(time.Now().UTC().UnixNano())

	//Llenado de bandeja de sushi
	for i := 0; i < len(shushi); i++ {
		nPiezas := 1 + rand.Intn(10)
		fmt.Printf("%d: piezas de %s\n", nPiezas, shushi[i])
		bandejaSushi = append(bandejaSushi, PiezaSushi{shushi[i], nPiezas})
	}

	fmt.Printf("Buen provecho\n")

	//Start go rutinas
	go servidor(done)

	for i := 0; i < len(nombre); i++ {
		fmt.Printf("Hola mi nombre es %s y vengo a comer shushi.\n", nombre[i])
		//exit [i] = make(chan Empty)
		go cliente(i, nombre[i])
	}

	<-done
	fmt.Printf("Simulació acabada\n")
}