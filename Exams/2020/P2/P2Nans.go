package main

import (
	"fmt"
	"time"
)

// Constantes:
// 4 Sillas
// 2 veces comen
// 1 majordomo
// 7 enanos

//Canales:
// Venir de la mina/Sentarse
// Servir/comer
// Levantarse

const (
	ChairSites    = 4 // Sillas
	TimesToEat    = 2 // Veces que comen
	NumberTitchys = 7 // Enanos

	MinRandom = 1  // Numero minimo random
	MaxRandom = 10 // Numero minimo random
)

type Empty struct{}

//Mayordomo
func butler(name string, site chan string, eat chan string, standUp chan string) {

	var chairs int = 0
	var nowTitchy string
	var lastTitchy string
	var empty bool = true

	fmt.Println("******* Hola som el majordom:", name)

	for {
		//Si los sitios se han ocupado
		if chairs < ChairSites {
			//Se usarane estos cases
			select {
			//Si un enanito quiere sientarse
			case nowTitchy = <-site:
				if empty {
					fmt.Println("******* El majordom fa seure a:", nowTitchy)
				} else {
					fmt.Println("******* El majordom fa seure a", nowTitchy, "a la cadira de", lastTitchy)
					lastTitchy = ""
					empty = true
				}
				chairs = chairs + 1

			//Si un enanito quiere comer
			case nowTitchy = <-eat:
				fmt.Println("******* El majordom serveix a:", nowTitchy)

			//Si un enanito se quiere levantar
			case nowTitchy = <-standUp:
				fmt.Println("******* El majordom dona permís per anar-se'n a:", nowTitchy)
				chairs = chairs - 1
				lastTitchy = nowTitchy //El enanito pasara a ser el ultimo enanito en ser despachado
				empty = false
			}
		} else { //Si en la sala NO hay sitio para sentase
			//Solo se utilizaran estos cases:
			select {
			//Si un enanito quiere comer
			case nowTitchy = <-eat:
				fmt.Println("+++++++ El majordom serveix a:", nowTitchy)

			//Si un enanito se quiere levantar
			case nowTitchy = <-standUp:
				fmt.Println("+++++++ El majordom dona permís per anar-se'n a:", nowTitchy)
				chairs = chairs - 1
				lastTitchy = nowTitchy //El enanito pasara a ser el ultimo enanito en ser despachado
				empty = false
			}

		}
	}
}

func work(name string) {
	fmt.Println(name, "treballa a la mina")
	time.Sleep(2 * time.Second)
}

func eats(name string) {
	fmt.Println(name, "ja menja!!!!!")
	//time.Sleep(500 * time.Millisecond)
	time.Sleep(1 * time.Second)
}

//Enanito
func titchy(name string, site chan string, eat chan string, standUp chan string, done chan Empty) {
	fmt.Println("Hola el meu nom és: ", name)

	for i := 0; i < TimesToEat; i++ {
		work(name)

		//Pide permiso para sentarse
		site <- name
		fmt.Println(name, "ja seu i demana ser servit")

		//Pide permiso para comer
		eat <- name
		eats(name)
		fmt.Println(name, "ha acabat de menjar i demana permís per aixecar-se")

		//Pide permiso para levantarse
		standUp <- name
	}

	fmt.Println(name, "se'n va a dormir")
	done <- Empty{} //Exit
}

func main() {

	var titchys = [NumberTitchys]string{"Savi", "Rondinaire", "Mudet", "Vergonyós", "Esternuts", "Feliç", "Dormilega"}

	site := make(chan string)
	eat := make(chan string)
	standUp := make(chan string)

	done := make(chan Empty, 1)

	//Mayordomo
	go butler("Alfred", site, eat, standUp)
	// Enanitos
	for i := 0; i < len(titchys); i++ {
		go titchy(titchys[i], site, eat, standUp, done)
	}

	for i := 0; i < len(titchys); i++ {
		<-done //Esperar que acaben
	}

}
