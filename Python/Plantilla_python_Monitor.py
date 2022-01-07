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
NUM_CONSUMERS = 5
NUM_PRODUCERS = 1


class Producer(threading.Thread):

    cond = threading.Condition()

    def __init__(self, cond):
        super().__init__()
        self.cond = cond

    def run(self):
        threading.currentThread().name = "Producer-" + threading.currentThread().name.split("-")[1]
        logging.debug(f"Init")
        with self.cond:
            logging.debug("Cedo permisos para acceder al recurso")
            self.cond.notifyAll()

class Consumer(threading.Thread):

    cond = threading.Condition()

    def __init__(self, cond):
        super().__init__()
        self.cond = cond

    def run(self):
        threading.currentThread().name = "Consumer-" + threading.currentThread().name.split("-")[1]
        logging.debug(f"Init")
        with self.cond:
            self.cond.wait()
            logging.debug("Puedo consumir")


def main():
    threads = []
    cond = threading.Condition() # Condición para el monitor

    # Cargamos todos los threads en un array
    for i in range(NUM_CONSUMERS):
        threads.append(Consumer(cond))

    for i in range(NUM_PRODUCERS):
        threads.append(Producer(cond))


    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

    # Esperamos que acaben todos los threads
    for threads in threads:
        thread.join()

    print("End")


if __name__ == "__main__":
    main()