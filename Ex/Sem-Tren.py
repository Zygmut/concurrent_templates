import threading            # Generar threads
import random               # Generar valores aleatorios
from random import randint 
import logging              # Debug más elegante
from time import sleep


# Definir el entorno de log
logging.basicConfig(level=logging.DEBUG,
                        format='[%(threadName)-2s] %(message)s',
                        )

# Constantes 
TRAIN_CAPACITY = 4              # Capacidad del tren 
MIN_TRAIN_TIME = 2              # Tiempo minimo del "tour" 
MAX_TRAIN_TIME = 5              # Tiempo maximo del "tour"
NUM_PASSENGERS = 10             # Numero de pasajeros

# Variables
passengers = []                 # Array de pasajeros 

# Semaforos
mutex_print = threading.Lock()  # Evitar errores de display

class Passenger(threading.Thread):
    def __init__(self):
        super().__init__()
        self.waiting = True                 # Determinar si un pasajero esta esperando al tren o dentro del tren 
        self.await_train = threading.Lock() # Semaforo binario para esperar el acceso al tren
        self.leave_train = threading.Lock() # Semaforo binario para esperar la remision del tren

        self.leave_train.acquire()          # Los semaforos binarios se inicializan con 0 permisos 
        self.await_train.acquire()

    def run(self):
        threading.currentThread().name = type(self).__name__ + "-" + threading.currentThread().name.split("-")[1] # Poner nombre al thread
        logging.debug("Init")
        while True:
            self.await_train.acquire()          # Esperamos que el tren nos de permiso para entrar 
            logging.debug("Enters the train")
            mutex_print.release()               # Evitar posibles problemas de prints
            self.waiting = False                # Ya no estoy esperando 

            self.leave_train.acquire()          # Esperamos que el tren nos de permiso para salir
            logging.debug("Leaves the train")
            mutex_print.release()               # Evitar posibles problemas de prints
            self.waiting = True                 # Me pongo a esperar

class Train(threading.Thread): 
    def __init__(self):
        super().__init__()
        self.loops = 0
        
    def take_passengers(self):
        global mutex_print, passengers
        logging.debug("Take passengers")
        avaliable_pass =  [passenger for passenger in passengers if passenger.waiting == True] # Cogemos todos los pasajeros que esten esperando
        random.shuffle(avaliable_pass)                      # Los reorganizamos para una entrada aleatoria

        if len(avaliable_pass) < TRAIN_CAPACITY:            # Revisamos si tenemos suficientes pasajeros para llenar el tren
            for i in range(len(avaliable_pass)):
                avaliable_pass[i].await_train.release()     # Vamos dando permiso a los pasajeros para entrar al tren
                mutex_print.acquire()                       # Evitar problemas de prints
                
        else:                   # Podemos llenar el tren entero 
            for i in range(TRAIN_CAPACITY):
                avaliable_pass[i].await_train.release()     # Vamos dando permiso a los pasajeros para entrar al tren
                mutex_print.acquire()                       # Evitar problemas de prints

    def leave_passengers(self):
        global mutex_print, passengers
        logging.debug("Leave passengers")
        avaliable_pass =  [passenger for passenger in passengers if passenger.waiting == False] # Cogemos todos los pasajeros que esten en el tren
        random.shuffle(avaliable_pass)                      # Los reorganizamos para una entrada aleatoria
        for i in range(len(avaliable_pass)):                         
            avaliable_pass[i].leave_train.release()         # Vamos dando permiso a los pasajeros para salir del tren
            mutex_print.acquire()                           # Evitar problemas de prints 

    def run(self):
        threading.currentThread().name = type(self).__name__  # Poner nombre al thread
        logging.debug(f"Arrives with seats for {TRAIN_CAPACITY} passengers")
        while True:
            self.take_passengers()                            # Cogemos pasajeros

            logging.debug(f"Starts the loop: {self.loops}")
            self.loops += 1
            sleep(randint(MIN_TRAIN_TIME, MAX_TRAIN_TIME))

            self.leave_passengers()                           # Dejamos pasajeros


def main():
    global passengers, mutex_print

    # Cargamos todos los threads en un array
    print(f"There are {NUM_PASSENGERS} passengers")
    for i in range(NUM_PASSENGERS):
        passengers.append(Passenger())

    mutex_print.acquire()
    # Ejecutamos todos los threads
    for passenger in passengers:
        passenger.start()

    Train().start()
if __name__ == "__main__":
    main()