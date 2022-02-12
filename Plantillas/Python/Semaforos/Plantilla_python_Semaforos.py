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
NUM_THREADS = 10
TOTAL_COUNT = 100

# Variables
count = 0

# Semaforos
counter_semaphore = threading.Lock()

class Process(threading.Thread):
    global NUM_THREADS, TOTAL_COUNT
    to_count = int(TOTAL_COUNT / NUM_THREADS)     
    
    def __init__(self):
        super().__init__()

    def run(self):
        global count
        logging.debug(f"Tengo que contar {self.to_count} veces")

        for i in range(self.to_count):
            counter_semaphore.acquire()
            count += 1
            counter_semaphore.release() 
        


def main():
    global count
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

    print(f"\nto_count: {count}")
    print("End")


if __name__ == "__main__":
    main()