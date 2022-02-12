#By: Ruben
import threading            # Generar threads
import random               # Generar valores aleatorios
from random import randint  
import logging              # Debug más elegante
from time import sleep      # Sleep/Delay

# Definir el entorno de log
logging.basicConfig(level=logging.DEBUG,
                        format='[%(threadName)-2s] %(message)s',
                        )

# Constantes 
MIN_TIME_REP = 5 
MAX_TIME_REP = 10

MIN_TIME_CLI = 1 
MAX_TIME_CLI = 1

MIN_CONSUMITIONS = 5
MAX_CONSUMITIONS = 15 

NUM_CONSUMERS = 8
NUM_PRODUCERS = 2

BUFFER_SIZE = 5

machine = object

class Machine(object):
    def __init__(self, size):
        self.maxSize = size
        self.curSize = 0
        self.consumitions = 0
        self.mutex = threading.Lock()
        self.notFull = threading.Condition(self.mutex)
        self.notEmpty = threading.Condition(self.mutex)

    def add_consumitions(self, consumition):
        with self.mutex:
            self.consumitions += int(consumition)
        

    def exist_client(self):
        return self.consumitions > 0
    
    # Servir
    def fill_up(self):
        with self.mutex:
            # If si no esta lleno x2
            while self.curSize == self.maxSize:
                self.notFull.wait()
            # Metemos "data"
            self.curSize = self.maxSize
            # Notificacion que ya hay "data"
            self.notEmpty.notify() 

    # Coger
    def take(self):
        with self.mutex:
            while self.curSize == 0:
                print(f"[{type(self).__name__}] Empty")
                self.notEmpty.wait()
            self.curSize -= 1 # Sacar el valor mas a la izquierda de la cola
            self.consumitions -= 1
            self.notFull.notify()
            return "tin can" 

class Client(threading.Thread):

    def __init__(self):
        super().__init__()
        self.consumitions = randint(MIN_CONSUMITIONS, MAX_CONSUMITIONS)
        self.velocity = randint(MIN_TIME_CLI, MAX_TIME_CLI)

    def run(self):
        global machine
        threading.currentThread().name = type(self).__name__ + "-" + threading.currentThread().name.split("-")[1] # Poner nombre al thread
        machine.add_consumitions(self.consumitions)
        logging.debug(f"Init with {self.consumitions} consumitions")
        if NUM_PRODUCERS != 0:
            curr_consumitions = 0
            while(curr_consumitions < self.consumitions):
                curr_consumitions += 1
                logging.debug(f"Takes a {machine.take()} from the machine [{curr_consumitions}/{self.consumitions}]") 
                sleep(self.velocity)

        logging.debug(f"Leaves")




class Replenisher(threading.Thread):

    def __init__(self):
        self.velocity = randint(MIN_TIME_REP, MAX_TIME_REP)
        super().__init__()

    def run(self):
        global machine 
        threading.currentThread().name = type(self).__name__ + "-" + str(int(threading.currentThread().name.split("-")[1]) - NUM_CONSUMERS) # Poner nombre al thread
        logging.debug(f"Init")
        sleep(self.velocity)
        while(machine.exist_client()):
            machine.fill_up()
            logging.debug(f"Replenishes the machine")
            sleep(self.velocity)

        logging.debug(f"Leaves")

def main():
    global machine 

    threads = []
    machine = Machine(BUFFER_SIZE)

    # Cargamos todos los threads en un array
    for i in range(NUM_CONSUMERS):
        threads.append(Client())

    for i in range(NUM_PRODUCERS):
        threads.append(Replenisher())

    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

    # Esperamos que acaben todos los threads
    for threads in threads:
        thread.join()

    print("End")


if __name__ == "__main__":
    main()