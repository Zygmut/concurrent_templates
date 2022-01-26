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
var demanaCadira = make(chan int)
var permisCadira [Nans]chan Empty
var tornaCadira = make(chan int)
var permisAixecarse = make(chan Empty)
var demanaMenjar = make(chan int)
var permisMenjar = make(chan Empty)

func nan(nom string, id int, done chan Empty) {
	fmt.Println("Hola el meu nom és: " + nom)
	for i := 1; i <= Quantitat; i++ {
		fmt.Println(nom + " treballa a la mina")
		time.Sleep(time.Duration(rand.Intn(2000)) * time.Millisecond)
		fmt.Println(nom + " ha arribat de la mina i espera una cadira")
		demanaCadira <- id
		<-permisCadira[id]
		fmt.Println(nom + " ja seu i demana ser servit")
		demanaMenjar <- id
		<-permisMenjar
		fmt.Println(nom + " ja menja!!!!!")
		time.Sleep(time.Duration(rand.Intn(20000)) * time.Millisecond)
		fmt.Println(nom + " ha acabat de menjar i demana permís per aixecar-se")
		tornaCadira <- id
		<-permisAixecarse
	}
	fmt.Println(nom + " se'n va a dormir")
	done <- Empty{}
}

func majordom() {
	cadires := 4
	esperen := [Nans]int{0, 0, 0, 0, 0, 0, 0}
	numEsperen := 0
	for {
		select {
		case id := <-demanaCadira:
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
			cadires++
			fmt.Println("******* El majordom dona permís per anar-se'n a " + nom[id])
			permisAixecarse <- Empty{}
			if numEsperen > 0 {
				i := 0
				for i = 0; i < Nans; i++ {
					if esperen[i] == 1 {
						break
					}
				}
				cadires--
				fmt.Println("******* El majordom fa seure a " + nom[i] + " a la cadira de " + nom[id])
				permisCadira[i] <- Empty{}
				esperen[i] = 0
				numEsperen--
			}
		}

	}
}

func main() {
	done := make(chan Empty, 1)
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
