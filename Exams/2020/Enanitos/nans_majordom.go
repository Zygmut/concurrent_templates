package main

import (
	"fmt"
	"math/rand"
	"time"
)

const (
	Nans      = 7
	Quantitat = 2
)

type Empty struct{}

var nom = []string{"Mudet", "Esternuts", "Vergonyós", "Dormilega",
	"Feliç", "Rondinaire", "Savi"}

//Problema basado en Servidor:
//Para cada accion: Peticion - Confirmacion

//Sentarse
var demanaCadira = make(chan int)
var permisCadira [Nans]chan Empty //El servidor tiene que saber a quien darle la silla
								 //La forma de indentificarlo es que cada uno tiene uno
//Comer
var tornaCadira = make(chan int)
var permisAixecarse = make(chan Empty)
//Irse
var demanaMenjar = make(chan int)
var permisMenjar = make(chan Empty)


//Clase ENANO
func nan(nom string, id int, done chan Empty) {
	fmt.Println("Hola el meu nom és: " + nom)

	for i := 1; i <= Quantitat; i++ {
		//Trabaja
		fmt.Println(nom + " treballa a la mina")
		time.Sleep(time.Duration(rand.Intn(2000)) * time.Millisecond)

		//Pide sentarse
		fmt.Println(nom + " ha arribat de la mina i espera una cadira")
		demanaCadira <- id
		<-permisCadira[id]	//Espera SU confirmacion
		
		//Pide comer
		fmt.Println(nom + " ja seu i demana ser servit")
		demanaMenjar <- id
		<-permisMenjar
		fmt.Println(nom + " ja menja!!!!!")
		time.Sleep(time.Duration(rand.Intn(20000)) * time.Millisecond)
		
		//Pide irse
		fmt.Println(nom + " ha acabat de menjar i demana permís per aixecar-se")
		tornaCadira <- id
		<-permisAixecarse
	}

	fmt.Println(nom + " se'n va a dormir")
	done <- Empty{}
}

//Clase MAJORDOMO
func majordom() {

	cadires := 4
	esperen := [Nans]int{0, 0, 0, 0, 0, 0, 0}
	numEsperen := 0

	for {
		select {

		case id := <-demanaCadira:
			//Si hay sitio disponible
			if cadires > 0 {
				cadires--
				fmt.Println("******* El majordom fa seure a " + nom[id])
				permisCadira[id] <- Empty{}
			} else {
				fmt.Println("******* El majordom fa esperar a " + nom[id] + ", totes les cadires estan ocupades")
				esperen[id] = 1
				numEsperen++
			}

		case id := <-demanaMenjar:
			fmt.Println("******* El majordom serveix a " + nom[id])
			permisMenjar <- Empty{}

		case id := <-tornaCadira:

			//Silla libre:
			cadires++
			fmt.Println("******* El majordom dona permís per anar-se'n a " + nom[id])
			permisAixecarse <- Empty{}

			//Adjudicacion silla a quien espera:
			if numEsperen > 0 {
				//El primero que haya pedido le da una silla
				i := 0
				for i = 0; i < Nans; i++ {
					if esperen[i] == 1 {
						break
					}
				}
				cadires--
				fmt.Println("******* El majordom fa seure a " + nom[i] + " a la cadira de " + nom[id])
				
				permisCadira[i] <- Empty{}  //Permiso al que espera
				esperen[i] = 0 //Resetear el valor
				numEsperen--
			}
		}

	}
}

func main() {
	done := make(chan Empty, 1) //Canal para finalizar

	for i := range permisCadira {
		permisCadira[i] = make(chan Empty)
	}
	go majordom()
	for i := 0; i < Nans; i++ {
		go nan(nom[i], i, done)
	}
	for i := 0; i < Nans; i++ {
		<-done
	}

	fmt.Printf("Simulació acabada\n")
}
