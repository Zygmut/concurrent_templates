# Rubén 

import threading            # Generar threads
import random
from random import randrange  
import logging              # Debug más elegante
from time import sleep      # Sleep/Delay


# Definir el entorno de log
logging.basicConfig(level=logging.DEBUG,
                        format='[%(threadName)-2s] %(message)s',
                        )

# Constantes 
NUM_MOLECULES = 4           # Numero de moleculas de agua
NUM_OX = 2                  # Numero de moleculas de oxigeno
MAX_GENERATION_VEL = 1      # Max velocity
MIN_GENERATION_VEL = 2      # Min velocity
ALTERNATIVE_GEN = False      # Ejecución alternativa
WATER_LONGITUDE = 4         # Lo largo que es el "string" del agua

# Variables
hydrogen_is_waiting = False                 # Gestión de hidrogenos pares e impares 
hydrogen_waiting_count = 0                  # Autogestión de salida 

# Semaforos
parallel_generation = threading.Lock()      # Es posible hacer una generacion paralela?
hydrogen_waiting = threading.Lock()         # Espera a que el oxigeno acabe de generar  
hydrogen_generation = threading.Semaphore(0)      # Esperar hasta que las moleculas de hidrogeno esten 
hydrogen_classificator = threading.Lock()   # Clasificación de hidrogenos pares e impares
hydrogen_even = threading.Lock()            # Espera al hidrogeno par 

class Oxygen(threading.Thread):

    global NUM_MOLECULES, MIN_GENERATION_VEL, MAX_GENERATION_VEL, NUM_OX, WATER_LONGITUDE
    type = 0  # Puede ser 1 o 2
    velocity = randrange(MAX_GENERATION_VEL, MIN_GENERATION_VEL,1)

    def __init__(self, type):
        super().__init__()
        self.type = (type % 2) +1

    def generate_water(self):
        global ALTERNATIVE_GEN,  hydrogen_generation, parallel_generation

        hydrogen_generation.acquire()                       # Esperamos a tener dos moleculas de hidrogeno
        logging.debug("Genera oxigeno")
        if ALTERNATIVE_GEN: parallel_generation.acquire()   # Si estamos en la ejecución alternativa, exclusión mutua entre generación de agua
        for i in range(WATER_LONGITUDE):
            if self.type == 1:
                print(" * ", end="")
            else:
                print(" + ", end="")
            
            sleep(self.velocity)
        print("")   

        hydrogen_waiting.release()                          # Aviso a las moleculas de hidrogeno que ya he acabado

        if ALTERNATIVE_GEN: parallel_generation.release()

    def run(self):
        threading.currentThread().name = "Ox" + str(self.type) + "-" + threading.currentThread().name.split("-")[1]

        logging.debug(f"Entra en escena con velocidad de {self.velocity*WATER_LONGITUDE}s por molecula de agua")
        for molecule in range(NUM_MOLECULES):
            self.generate_water()       # Genero agua

        logging.debug("Acaba")

class Hydrogen(threading.Thread):
    global NUM_MOLECULES

    def __init__(self):
        super().__init__()

    def run(self):
        global hydrogen_generation, hydrogen_classificator, hydrogen_is_waiting, hydrogen_even, hydrogen_waiting_count, hydrogen_waiting, mutex
        threading.currentThread().name = "Hy" + "-" + threading.currentThread().name.split("-")[1]

        logging.debug("Entra en escena")
        for molecule in range(NUM_MOLECULES):

            hydrogen_classificator.acquire()        # Entra en la clasificación entre par e impar 
            if not hydrogen_is_waiting:             # Si no hay ningún hidrogeno esperando
                hydrogen_is_waiting = True          # Yo estoy esperando
                logging.debug("Impar espera a otro hidrogeno")
                hydrogen_classificator.release()    # Cedo el paso a otra molecula
                hydrogen_even.acquire()             # Espero a la molecula de hidrogeno Par  
            else:
                hydrogen_is_waiting = False         # Ya no hay nadie esperando porque voy yo  
                logging.debug("Par libera un oxigeno para hacer agua")
                hydrogen_classificator.release()    # Cedo el paso a otra molecula de hidrogeno
                hydrogen_generation.release()       # Aviso al oxigeno que puede generar agua       
                hydrogen_waiting.acquire()          # Espero a que acabe el oxigeno de hacer el agua 
                hydrogen_even.release()             # Doy la señal que hay una molecula par, usandolo para salir las dos moleculas a la vez 

        logging.debug("Acaba")


def main():
    threads = []
    global hydrogen_waiting, hydrogen_generation, hydrogen_even 
    # Cargamos todos los threads en un array
        
    for i in range(NUM_OX):
        threads.append(Oxygen(i))

    for i in range(NUM_OX*2):
        threads.append(Hydrogen())

    random.shuffle(threads)

    # Semaforos que estan bloqueados al principio de la ejecución
    hydrogen_even.acquire()        
    hydrogen_waiting.acquire() 

    
    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

    # Esperamos que acaben todos los threads
    for threads in threads:
        thread.join()

    print("End")


if __name__ == "__main__":
    main()