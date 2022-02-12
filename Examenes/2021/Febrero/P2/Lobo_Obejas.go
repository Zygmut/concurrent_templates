//Jorge González Pascual
package main

import (
	"fmt"
	"math/rand"
	"time"
)

//Constantes
const (
	//Rango de numero de obejas
	MIN_Obejas = 2
	MAX_Obejas = 5
	//Rango de numero de lobos
	MIN_Lobos = 1
	MAX_Lobos = 10

	//Rango de tiempos beber obejas
	MIN_TIME = 1
	MAX_TIME = 5
	//Rango de tiempos lobo
	MIN_TIME_LOBO = 3
	MAX_TIME_LOBO = 5
)

//Estructura vacia
type Empty struct{}

//Canales
var permisoBeber = make(chan int)
var okPermisoBeber [MAX_Obejas]chan Empty

var permisoIrse = make(chan int)
var okPermisoIrse [MAX_Obejas]chan Empty

var loboBeber = make(chan int)
var okLoboBeber = make(chan Empty)

var loboExit = make(chan int)
var okLoboExit = make(chan Empty)

//Metodo para que los procesos esperen
func wait(wait_time int) {
	time.Sleep(time.Duration(wait_time) * time.Second)
}

//Servidor: hace el papel de Pastor
func servidor(obejas int) {
	waitDrinkObejas := 0 //Contador de obejas esperando para beber
	inObejas := 0        //Obejas que hay en el rio
	inLobos := 0         //Lobos que hay en el rio
	waitExitObejas := 0  //Contador de obejas esperando para irse

	//Array de obejas esperando para beber
	var obejasPendientesBeber [MAX_Obejas]int
	for i := 0; i < obejas; i++ {
		obejasPendientesBeber[i] = 0
	}
	//Array de obejas esperando para irse
	var obejasPendientesExit [MAX_Obejas]int
	for i := 0; i < obejas; i++ {
		obejasPendientesExit[i] = 0
	}

	//Metodo que busca la primera obeja esperando segun el id. Segun la direccion
	//0: Ir a beber
	//1: Irse del rio
	get_first_waiting := func(direccion int) (id int) {
		//Ir a beber
		if direccion == 0 {
			for i := 0; i < obejas; i++ {
				if obejasPendientesBeber[i] == 1 {
					return i
				}
			}
		} else {
			//Irse del rio
			for i := 0; i < obejas; i++ {
				if obejasPendientesExit[i] == 1 {
					return i
				}
			}
		}
		return -1
	}

	//Bucle infinito del SERVIDOR
	for {
		select {
		//Obeja pide beber
		case id := <-permisoBeber:
			//Si hay mas de una obeja en el rio o una esperando puede/n pasar
			if inObejas > 1 || waitDrinkObejas > 0 {
				//Si hay una obeja esperando pasa con ella
				if waitDrinkObejas > 0 {
					//Se van la que espera y la que solicita irse
					//Cogemos el id de una obeja esperando
					idWaiting := get_first_waiting(0)
					//Esa obeja ya no espera por lo tanto:
					obejasPendientesBeber[idWaiting] = 0
					waitDrinkObejas--

					inObejas++
					fmt.Printf("**** El pastor hace pasar a la obeja %d para bajar al rio a beber.      Lobos = %d - Obejas = %d RAPIDO!!\n", idWaiting, inLobos, inObejas)
					inObejas++
					fmt.Printf("**** El pastor hace pasar a la obeja %d para bajar al rio a beber.      Lobos = %d - Obejas = %d RAPIDO!!\n", id, inLobos, inObejas)
					okPermisoBeber[idWaiting] <- Empty{}
					okPermisoBeber[id] <- Empty{}

				} else {
					//Si no hay obejas esperando pasa ella sola
					inObejas++
					fmt.Printf("**** El pastor da permiso a la obeja %d para bajar al rio a beber.      Lobos = %d - Obejas = %d\n", id, inLobos, inObejas)
					okPermisoBeber[id] <- Empty{}
				}
			} else {
				//Ponemos la obeja en espera
				waitDrinkObejas++
				obejasPendientesBeber[id] = 1
				fmt.Printf("---- El pastor hace esperar a la obeja %d para bajar ira a beber.\n", id)
			}
		//Obeja pide irse
		case id := <-permisoIrse:
			//Si hay mas de dos obejas o minimo 1, se pueden ir tranquilamente
			if inObejas > 2 || waitExitObejas > 0 {
				//Si hay obejas esperando
				if waitExitObejas > 0 {
					//Se van la que espera y la que solicita irse
					//Cogemos el id de una obeja esperando
					idWaiting := get_first_waiting(1)

					//Esa obeja ya no espera por lo tanto:
					obejasPendientesExit[idWaiting] = 0
					waitExitObejas--

					inObejas--
					fmt.Printf("**** El pastor hace salir a la obeja %d para irse del rio.      		Lobos = %d - Obejas = %d RAPIDO!!\n", idWaiting, inLobos, inObejas)
					inObejas--
					fmt.Printf("**** El pastor hace salir a la obeja %d para irse del rio.      		Lobos = %d - Obejas = %d RAPIDO!!\n", id, inLobos, inObejas)

					okPermisoIrse[idWaiting] <- Empty{}
					okPermisoIrse[id] <- Empty{}

				} else {
					//Se puede ir tranquilamente
					inObejas--
					okPermisoIrse[id] <- Empty{}
					fmt.Printf("**** El pastor da permiso a la obeja %d para irse.    					Lobos = %d - Obejas = %d\n", id, inLobos, inObejas)
				}

			} else {
				//Ponemos la obeja en espera
				waitExitObejas++
				obejasPendientesExit[id] = 1
				fmt.Printf("---- El pastor hace esperar a la obeja %d para irse del rio.\n", id)
			}

		//Lobo pide beber
		case id := <-loboBeber:
			inLobos++
			fmt.Printf("	El lobo %d baja al rio a beber                        				Lobos = %d - Obejas = %d\n", id, inLobos, inObejas)
			okLoboBeber <- Empty{}

		//Lobo pide irse
		case id := <-loboExit:
			inLobos--
			fmt.Printf("	El lobo %d se va                       								Lobos = %d - Obejas = %d\n", id, inLobos, inObejas)
			okLoboExit <- Empty{}
		}
	}
}

//Obeja:
func obeja(id int, done chan Empty) {
	fmt.Printf("Soy la obeja: %d\n", id)

	//Quiere ir a beber
	fmt.Printf("La obeja %d quiere al rio a beber\n", id)
	permisoBeber <- id
	<-okPermisoBeber[id]

	//Beber
	wait(MIN_TIME + rand.Intn(MAX_TIME-MIN_TIME))

	//Se quiere ir
	permisoIrse <- id
	<-okPermisoIrse[id]

	fmt.Printf("La obeja %d se va\n", id)
	//Fin del proceso
	done <- Empty{}
}

//Lobo:
func lobo(id int, done chan Empty) {
	fmt.Printf("	Soy el lobo: %d\n", id)

	//Quiere ir a beber
	loboBeber <- id
	<-okLoboBeber

	//Beber
	wait(MIN_TIME_LOBO + rand.Intn(MAX_TIME_LOBO-MIN_TIME_LOBO))

	//Se va
	loboExit <- id
	<-okLoboExit

	//Fin del proceso
	done <- Empty{}
}

func main() {
	fmt.Printf("EMPIEZA LA SIMULACION\n")
	done := make(chan Empty) //Canal para finalizar

	rand.Seed(time.Now().UnixNano())

	//Generamos los numeros aleatorios de los animales
	obejas := MIN_Obejas + rand.Intn(MAX_Obejas-MIN_Obejas)
	fmt.Printf("Obejas: %d\n", obejas)
	lobos := MIN_Lobos + rand.Intn(MAX_Lobos-MIN_Lobos)
	fmt.Printf("Lobos: %d\n", lobos)

	//Inicializamos los canales de respuesta
	for i := 0; i < obejas; i++ {
		okPermisoBeber[i] = make(chan Empty)
		okPermisoIrse[i] = make(chan Empty)
	}

	//Inicializamos las go rutinas
	go servidor(obejas)
	for i := 0; i < obejas; i++ {
		go obeja(i, done)
	}
	for i := 0; i < lobos; i++ {
		go lobo(i, done)
	}

	//Esperamos a que todos hayan finalizado
	for i := 0; i < obejas+lobos; i++ {
		<-done
	}

	fmt.Printf("SIMULACION ACABADA\n")
}
