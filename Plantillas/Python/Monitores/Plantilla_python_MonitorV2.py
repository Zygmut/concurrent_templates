import threading            # Generar threads
import random               # Generar valores aleatorios
import collections
from random import randint  
import logging              # Debug más elegante
from time import sleep      # Sleep/Delay

# Definir el entorno de log
logging.basicConfig(level=logging.DEBUG,
                        format='[%(threadName)-2s] %(message)s',
                        )

# Constantes 
NUM_CONSUMERS = 2
NUM_PRODUCERS = 2

TO_PRODUCE = 1000
TO_CONSUME = TO_PRODUCE

BUFFER_SIZE = 10

monitor = object

class Monitor(object):
    def __init__(self, size):
        self.buffer = collections.deque([], size)
        self.mutex = threading.Lock()
        self.notFull = threading.Condition(self.mutex)
        self.notEmpty = threading.Condition(self.mutex)

    # Servir
    def append(self, data):
        with self.mutex:
            #if si no esta lleno x2
            while len(self.buffer) == self.buffer.maxlen:
                self.notFull.wait()
            #Metemos "data"
            self.buffer.append(data)
            #Notificacion que ya hay "data"
            self.notEmpty.notify() 

    # Coger
    def take(self):
        with self.mutex:
            while not self.buffer:
                self.notEmpty.wait()
            data = self.buffer.popleft() #Sacar el valor mas a la izquierda de la cola
            self.notFull.notify()
            return data

class Consumer(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        global monitor
        threading.currentThread().name = type(self).__name__ + "-" + threading.currentThread().name.split("-")[1] # Poner nombre al thread
        logging.debug(f"Init")
        for i in range(TO_PRODUCE):
            logging.debug(f"Produces")
            data = f"{threading.currentThread().name}'s thing"
            monitor.append(data) 



class Producer(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        global monitor
        threading.currentThread().name = type(self).__name__ + "-" + str(int(threading.currentThread().name.split("-")[1]) - NUM_CONSUMERS) # Poner nombre al thread
        logging.debug(f"Init")
        for i in range(TO_CONSUME):
            logging.debug(f"Consume {monitor.take()}")


def main():
    global monitor

    threads = []
    monitor = Monitor(BUFFER_SIZE)

    # Cargamos todos los threads en un array
    for i in range(NUM_CONSUMERS):
        threads.append(Consumer())

    for i in range(NUM_PRODUCERS):
        threads.append(Producer())

    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

    # Esperamos que acaben todos los threads
    for threads in threads:
        thread.join()

    print("End")


if __name__ == "__main__":
    main()