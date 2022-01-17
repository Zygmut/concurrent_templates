#Creado por: PlantanosVerdes

import threading # Generar un int aleatorio
from random import randint
from time import sleep # Esperar
import random # Generación de números aleatorios

#Constantes
MAX_TREN = 4                        #Capacidad Maxima del tren

MIN_PERSONAS = 5                    #Min personas que habran
MAX_PERSONAS = 6                    #Max personas que habran

MIN_TIME_TRAVEL = 1                 #Minimo de tiempo para el viaje
MAX_TIME_TRAVEL = 2                 #Maximo de tiempo para el viaje

#Semaforos
waitPasajeros = threading.Lock()    #Semaforo para que esperen los pasajeros
confirmPasajeros = threading.Lock() #Para que el tren se vaya de viaje
mutexPasajeros = threading.Lock()   #Mutex para proteger a la variable "pasajerosVagon"
viaje = threading.Lock()            #Semaforo para cuando se va el tren de viaje

#Variables
personas = 0                        #Personas que habra durante la ejecución
pasajerosVagon = 0                  #Pasajeros que habra en el vagon


class Tren(threading.Thread):
    def __init__(self):
        super().__init__()
        self.viajes = 0

    def run(self):
        print(f"El tren acaba de llegar. Capacidad Maxima: {MAX_TREN}")

        while True:
            #Llegada del tren
            waitPasajeros.release() #desbloquear a los pasajeros
            print(f"El tren abre las puertas para subir...")
            confirmPasajeros.acquire() #bloqueo tren hasta que los pasajeros hasta que suban

            print(f"El se marcha. Viaje: {self.viajes}")
            self.viajes += 1
            sleep(randint(MIN_TIME_TRAVEL, MAX_TIME_TRAVEL))
            
            viaje.release() #Desbloquear a los pasajeros subidos
            print(f"El tren abre las puertas para bajar...")

            confirmPasajeros.acquire() #bloqueo tren hasta que los pasajeros lo desbloquen

class Pasajero(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global pasajerosVagon
        threading.currentThread().name = "Persona" + " " + \
            threading.currentThread().name.split("-")[1]
        
        while True:
            waitPasajeros.acquire() #Esperamos a que llegue el tren
            #Subir al tren
            with mutexPasajeros:
                pasajerosVagon += 1
                print(f"    {threading.currentThread().name} sube al tren")
                if (pasajerosVagon < MAX_TREN) and (pasajerosVagon < personas):
                    waitPasajeros.release() #Pueden pasar mas personas al vagon
                else:
                    confirmPasajeros.release() #Desbloqueamos al tren para que haga el viaje

            viaje.acquire() #Esperamos al que el tren llegue

            #Bajar del tren
            with mutexPasajeros:
                pasajerosVagon -= 1
                print(f"    {threading.currentThread().name} baja del tren")
                if (pasajerosVagon == 0):
                    confirmPasajeros.release() #Si es el ultimo pasajero, avisar al tren
                else:
                    #Libreamos a todos los pasajeros bloqueados por el viaje
                    viaje.release() #Desbloqueamos a los siguientes pasajeros para bajar. Evitamos un "for"

def main():

    global personas
    threads = []
    print(f"Simulacion Tren")
    personas = randint(MIN_PERSONAS, MAX_PERSONAS)

    #Semaforos bloqueados inicialmente
    #Bloquean a los pasajeros:
    waitPasajeros.acquire() #Bloqueamos a los pasajeros hasta que llegue el tren
    viaje.acquire() #Bloqueamos durante el viaje a los pasajeros
    #Bloquean al tren:
    confirmPasajeros.acquire() #Confirmacion de pasajeros, bloqueado inicialmente


    print(f"Hay {personas} personas:")
    # Personas
    for i in range(personas):
        print(f"Persona {i+1}")
        threads.append(Pasajero())  
    
    # Tren
    threads.append(Tren())  

    # Asi evitamos un posible orden en caso que nuestros threads tengan caracteristicas diferentes
    #random.shuffle(threads)

    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
