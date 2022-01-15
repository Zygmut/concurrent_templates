
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
NUM_PASSENGERS = 2             # Numero de pasajeros

# Variables
passengers = []                 # Array de pasajeros 

# Semaforos
notify_train = threading.Lock() #asegurar print ordenado

class Passenger(threading.Thread):
    def __init__(self):
        global passengers
        super().__init__()
        passengers.append(self)
        self.waiting = True
        self.await_train = threading.Lock() # Semaforo binario para esperar el acceso al tren
        self.leave_train = threading.Lock() # Semaforo binario para esperar la remision del tren

        self.leave_train.acquire()          # Los semaforos binarios se inicializan con 0 permisos 
        self.await_train.acquire()

    def enter_train(self):
        global passengers, notify_train
        logging.debug("Enters the train")
        self.waiting= False

        running_passengers = [passenger for passenger in passengers if passenger.waiting == False]

        if len(running_passengers) < TRAIN_CAPACITY:
            waiting_passengers = [passenger for passenger in passengers if passenger.waiting == True]
            if len(waiting_passengers) != 0: 
                waiting_passengers[randint(0,len(waiting_passengers)-1)].await_train.release() # Cogemos un pasajero que este esperando aleatorio y le decimos que entre
            else:
                notify_train.release() # Notificamos que ya hemos acabado de llenar el Tren
        else:
            notify_train.release() # Notificamos que ya hemos acabado de llenar el Tren

    def exit_train(self):
        logging.debug("Leaves the train")
        self.waiting= True

        running_passengers = [passenger for passenger in passengers if passenger.waiting == False ]
        if len(running_passengers) != 0:
            running_passengers[randint(0, len(running_passengers)-1)].leave_train.release() # Vamos sacando pasajeros aleatorios
        else:
            notify_train.release()

    def run(self):
        threading.currentThread().name = type(self).__name__ + "-" + threading.currentThread().name.split("-")[1] # Poner nombre al thread
        logging.debug("Init")
        while True:
            self.await_train.acquire()          # Esperamos que el tren nos de permiso para entrar 
            self.enter_train()

            self.leave_train.acquire()          # Esperamos que el tren nos de permiso para salir
            self.exit_train()

class Train(threading.Thread): 
    def __init__(self):
        super().__init__()
        self.loops = 0
        
    def take_passengers(self):
        global passengers, notify_train
        logging.debug("Take passengers")
        passengers[randint(0, len(passengers)-1)].await_train.release() 
        notify_train.acquire()

    def leave_passengers(self):
        global passengers, notify_train
        logging.debug("Leave passengers")

        running_passengers = [passenger for passenger in passengers if passenger.waiting == False ]
        running_passengers[randint(0, len(running_passengers)-1)].leave_train.release()
        notify_train.acquire()

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
    global passengers, notify_train
    threads = []
    # Cargamos todos los threads en un array
    print(f"There are {NUM_PASSENGERS} passengers")
    for i in range(NUM_PASSENGERS):
        threads.append(Passenger())

    threads.append(Train())
    
    notify_train.acquire()
    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

if __name__ == "__main__":
    main()