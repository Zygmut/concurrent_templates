package main

import (
	"fmt"       // o log para printear
	"math/rand" // Para generación de numeros aleatorios
	"time"      // sleep
)

//CONSTANTES
const (
	Fumadores   = 6 //Clientes fumadores
	NoFumadores = 6 //Clientes nofumadores

	// Control de velocidades para comer
	MAX_time_eat = 5
	MIN_time_eat = 1

	//Posibles tipos de las peticiones:
	PedirSitio = 1
	Despedida  = 2

	//Numero maximo de espacios en el restaurante
	Salones = 3
	Mesas   = 3

	//Tipos de clientes/mesas
	NONE        = ""
	T_Fumador   = "FUMADOR"
	T_NoFumador = "NOFUMADOR"
)

//ESTRUCTURAS
//Estructura salon
type Salon struct {
	tipo  string
	mesas int
}

//Esctuctura de la peticion que hara el proceso
type Peticion_Salon struct {
	id   int    //Id del proceso
	tipo string //Estado de peticion
}

//Esctuctura de la peticion que hara el proceso
type Devolucion_Salon struct {
	id    int //Id del proceso
	salon int //Estado de peticion
}

//Estructura vacia
type Empty struct{}

//VARIABLES
var (
	//Canales para pedir sentarse
	//Peticiones de los clientes al servidor
	chan_pedir_sito = make(chan Peticion_Salon)
	//Confirmacion del sitio donde sentarse
	chan_sitio_salon [Fumadores + NoFumadores]chan int

	//Canales para lenvantarse
	chan_devolver_sito = make(chan Devolucion_Salon)
	chan_byebye        = make(chan Empty)

	//Salones del restaurante
	salones [Salones]Salon

	//Nombres
	nombres = []string{"RUBEN", "MARIO", "JORGE", "MARIA", "PAULA", "IRENE",
		"PABLO", "CATALINA", "IVAN", "RAMONA", "CRIS", "TOMEU"}
)

//Metodo para esperar
func wait(wait_time int) {
	time.Sleep(time.Duration(wait_time) * time.Second)
}

//Funcion Cliente que va al restaurante
func cliente(id int, nombre string, tipo string, done chan Empty) {
	//Inicilizacion del canal de espera personal de cada cliente
	chan_sitio_salon[id] = make(chan int)
	fmt.Printf("Cliente %d Hola soy %s - %s\n", id, nombre, tipo)

	//Sentarse:
	//Mandamos peticion
	chan_pedir_sito <- Peticion_Salon{id, tipo}
	fmt.Printf("%s: estoy esperando\n", nombre)
	//Esperamos a que nos confirme y recogemos el salon
	salon := <-chan_sitio_salon[id]
	fmt.Printf("%s: me he sentado en el Salon %d - %s (%d/%d)\n", nombre, salon, tipo, salones[salon].mesas, Mesas)

	//Comer:
	//Espear un tiempo random
	wait(MIN_time_eat + rand.Intn(MAX_time_eat-MIN_time_eat))

	//Irse:
	//Pedimos la cuenta y nos vamos del salon
	fmt.Printf("%s - %s: ya he comido, me quiero ir\n", nombre, tipo)
	chan_devolver_sito <- Devolucion_Salon{id, salon}
	<-chan_byebye

	fmt.Printf("%s - %s: Adios\n", nombre, tipo)

	//Fin del proceso
	done <- Empty{}
}

//Servidor: funcion que hace de "Metre"
func servidor() {
	var pendientesFumadores [Fumadores]int
	var pendientesNoFumadores [NoFumadores]int
	//Ponemos todos los id a 0
	for i := 0; i < Fumadores; i++ {
		pendientesFumadores[i] = 0
	}
	for i := 0; i < NoFumadores; i++ {
		pendientesNoFumadores[i] = 0
	}
	nPendientesFum := 0
	nPendientesNoFum := 0

	//FUNCIONES:
	//Funcion que retorna el primer salon vacio o del mismo tipo
	//Retorna -1 si no hay salon disponible
	get_salon_tipo := func(tipo string) (mesa int) {
		//Todos los salones vacios
		for i := 0; i < Salones; i++ {
			//Si el salon esta vacio el cliente puede entrar
			if salones[i].tipo == NONE {
				salones[i].tipo = tipo
				return i
			} else {
				if salones[i].tipo == tipo {
					//Si no hay el maximo de mesos
					if salones[i].mesas < Mesas {
						return i
					}
				}
			}
		}
		//No hay mesas disponibles
		return -1
	}

	//Segun el tipo retorna el primer id del cliente que esta esperando
	get_fist_pendiente := func(tipo string) (id int) {
		if tipo == T_Fumador {
			//Si es de tipo fumador
			for i := 0; i < Fumadores; i++ {
				if pendientesFumadores[i] == 1 {
					return i
				}
			}
		} else {
			//Si es de tipo no fumador
			for i := 0; i < NoFumadores; i++ {
				if pendientesNoFumadores[i] == 1 {
					return i + NoFumadores
				}
			}
		}
		return -1
	}

	//Otroga una mesa a alguien de la lista de espera segun su tipo
	set_mesa_pendiente := func(tipo string, salon int, id_pendiente int) {
		if tipo == T_Fumador {
			pendientesFumadores[id_pendiente] = 0
			nPendientesFum--
			salones[salon].mesas++
			fmt.Printf("***** %s Tiene mesa en el salon %d de tipo %s", nombres[id_pendiente], salon, tipo)
		} else {
			pendientesNoFumadores[id_pendiente] = 0
			nPendientesNoFum--
			salones[salon].mesas++
			fmt.Printf("***** %s Tiene mesa en el salon %d de tipo %s", nombres[id_pendiente], salon, tipo)
		}
	}

	//BUCLE:
	for {
		select {
		//Caso que pidan un sitio
		case peticion_sentarse := <-chan_pedir_sito:
			salon_disponible := get_salon_tipo(peticion_sentarse.tipo)
			//Si no hay salones disponibles se añade en pendiente
			if salon_disponible < 0 {
				//No hay sitios disponibles
				fmt.Printf("***%s - %s Tienes que esperar\n", nombres[peticion_sentarse.id], peticion_sentarse.tipo)
				if peticion_sentarse.tipo == T_Fumador {
					nPendientesFum++
					pendientesFumadores[peticion_sentarse.id] = 1
				} else {
					nPendientesNoFum++
					pendientesNoFumadores[peticion_sentarse.id-NoFumadores] = 1
				}

			} else {
				//Le damos la mesa
				salones[salon_disponible].mesas++
				chan_sitio_salon[peticion_sentarse.id] <- salon_disponible
			}

		//Caso que se vayan del sitio
		case peticion_levantarse := <-chan_devolver_sito:
			fmt.Printf("***%s Puedes irte del salon %d\n", nombres[peticion_levantarse.id], peticion_levantarse.salon)
			salones[peticion_levantarse.salon].mesas--
			//Damos la confirmacion al cliente para irse
			chan_byebye <- Empty{}

			//Si no se queda vacio
			if salones[peticion_levantarse.salon].mesas > 0 {
				//Si hay peticiones:
				id := -1
				if salones[peticion_levantarse.salon].tipo == T_Fumador && nPendientesFum > 0 {
					//Cogemos al primer pendiente fumador si son ellos los que esperan
					id = get_fist_pendiente(T_Fumador)
					set_mesa_pendiente(T_Fumador,peticion_levantarse.salon,id)
					chan_sitio_salon[id] <- peticion_levantarse.salon
				} else if salones[peticion_levantarse.salon].tipo == T_NoFumador && nPendientesNoFum > 0 {
					//Cogemos al primer pendiente no fumador
					id = get_fist_pendiente(T_NoFumador)
					set_mesa_pendiente(T_NoFumador,peticion_levantarse.salon,id)
					chan_sitio_salon[id] <- peticion_levantarse.salon
				}

			} else {
				//Si la mesa se queda vacia quitamos el tipo hal salon
				salones[peticion_levantarse.salon].tipo = NONE

				//Miramos si hay alguien pendiente:
				//(En este caso tendran prioridad nos fumadores a entrar a un salon)
				if nPendientesFum > 0 {
					id := get_fist_pendiente(T_Fumador)
					set_mesa_pendiente(T_Fumador,peticion_levantarse.salon,id)
					chan_sitio_salon[id] <- peticion_levantarse.salon

				} else if nPendientesNoFum > 0 {
					id := get_fist_pendiente(T_NoFumador)
					set_mesa_pendiente(T_NoFumador,peticion_levantarse.salon,id)
					chan_sitio_salon[id] <- peticion_levantarse.salon
				}
			}

		}
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())

	done := make(chan Empty) //Sincrono
	//done := make(chan Vacio, 1) //Asincrono

	//Todos los salones vacios
	for i := 0; i < Salones; i++ {
		salones[i].mesas = 0
		salones[i].tipo = NONE
	}

	//Servidor
	go servidor()

	//Clientes Fumadores
	n := 0
	for n = 0; n < Fumadores; n++ {
		go cliente(n, nombres[n], T_Fumador, done)
	}
	//Clientes NoFumadores
	for i := 0; i < NoFumadores; i++ {
		go cliente(n+i, nombres[n+i], T_NoFumador, done)
	}

	//Esperamos a que finalicen
	for i := 0; i < Fumadores+NoFumadores; i++ {
		<-done
	}

	fmt.Printf("End\n")
}