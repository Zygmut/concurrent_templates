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
NUM_THREADS = 5

class Process(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        logging.debug(f"Init")


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