import threading            # Generar threads
import random               # Generar valores aleatorios
from random import randrange  
import logging              # Debug más elegante
from time import sleep      # Sleep/Delay


# Definir el entorno de log
logging.basicConfig(level=logging.DEBUG,
                        format='[%(threadName)-2s] %(message)s',
                        )

# Constantes 
NUM_THREADS = 5
MAX_VEL = 1
MIN_VEL = 5

class Process(threading.Thread):

    def __init__(self):
        super().__init__()
        self.velocity = randrange(MAX_VEL, MIN_VEL) 

    def run(self):
        threading.currentThread().name = type(self).__name__ + "-" + threading.currentThread().name.split("-")[1] # Poner nombre al thread
        
        logging.debug(f"Init with vel: {self.velocity}")


def main():
    threads = []

    # Cargamos todos los threads en un array
    for i in range(NUM_THREADS):
        threads.append(Process())

    random.shuffle(threads) # Asi evitamos un posible orden en caso que nuestros threads tengan caracteristicas diferentes

    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

    # Esperamos que acaben todos los threads
    for threads in threads:
        thread.join()

    print("End")


if __name__ == "__main__":
    main()