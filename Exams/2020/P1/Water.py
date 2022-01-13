import threading
# Generar un int aleatorio
from random import randint
from time import sleep                                  # Esperar
# Generación de números aleatorios
import random

NUM_HYDROGEN = 4  # Numero de hidrogenos
NUM_OXYGEN = 2  # Numero de oxigeno
SYN_WATER = 4  # Numero de sintetizaciones
CHARACTERS = 4  # Numero de caracteres a imprimir

# 5 canales
hydrogen_union = threading.Lock()  # Semaforo de hidrogenos
hydrogen_wait = threading.Lock()  # Semaforo que bloquea al primer hidrogeno
hydrogens_block = threading.Lock() # Semaforo que bloquea a los hydrogenos miendras se sintetiza el Agua
oxygen_wait = threading.Semaphore(0) # Semaforo contador que espera al segundo hidrogeno
mutex_sim = threading.Lock() # Mutex para realizar la segunda simulacion

second_hydrogen_wait = False #Variable para saber si ya ha entrado un hidrogeno o no

SECOND_ALTERNATIVE = True #VARIABLE PARA REALIZAR LA SEGUNDA MONITORIZACION

# Clase HYDROGENO
class hydrogen(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global second_hydrogen_wait, hydrogen_union, hydrogen_wait, hydrogens_block, oxygen_wait
        threading.currentThread().name = "Hy" + "-" + threading.currentThread().name.split("-")[1]
        print(f"Hola soy el {threading.currentThread().name}")

        for i in range(SYN_WATER):
            hydrogen_union.acquire()

            if not second_hydrogen_wait:
                # Primer hidrogeno
                print(f"{threading.currentThread().name} es el primero: espera a otro hidrogeno")
                second_hydrogen_wait = True

                hydrogen_union.release()  # Via libre a otros Hidrogenos

                hydrogen_wait.acquire()  # Bloqueo al primer hidrogeno

            else:
                # Segundo hidrogeno
                print(f"{threading.currentThread().name} es el segundo: libera un oxigeno para hacer H2O")
                second_hydrogen_wait = False

                hydrogen_union.release()  # Via libre a otros Hydrogenos

                oxygen_wait.release()  # Desbloqueo del Oxigeno
                hydrogens_block.acquire()  # Bloqueo hasta que el Oxigeno acaben
                hydrogen_wait.release()  # Desbloqueo al primer Hidrogeno


# Clase OXIGENO
class oxygen(threading.Thread):

    def __init__(self, type):
        super().__init__()
        self.type = (type % 2)

    #Sintetizacion
    def syn(self):
        for i in range(SYN_WATER):
            if self.type == 0:
                print(f"*", end="")
            else:
                print(f"+", end="")
            sleep(randint(1,2))
        print("")

    def run(self):
        global hydrogens_block, oxygen_wait, mutex_sim
        threading.currentThread().name = "Ox" + str(self.type) + "-" + threading.currentThread().name.split("-")[1]
        print(f"Hola soy el {threading.currentThread().name}")

        for i in range(SYN_WATER):
            oxygen_wait.acquire()  # Esperar hasta que lo desbloquee alguien
            
            if SECOND_ALTERNATIVE: mutex_sim.acquire() #Mutex en en el caso de la segunda simulacion
            print(f"-------> {threading.currentThread().name} sintetizando H2O")
            self.syn() #Sintetizacion
            if SECOND_ALTERNATIVE: mutex_sim.release()

            hydrogens_block.release() #Liberamos a los hidrogenos


def main():
    global hydrogen_union, hydrogen_wait, hydrogens_block, oxygen_wait, mutex_sim
    
    threads = []

    print(f"Simulacion sintetizacion de H2O")
    # Bloqueamos de semaforos para que empiecen bloqueados
    hydrogen_wait.acquire()  # Bloqueo del oxigeno
    hydrogens_block.acquire()  # Bloqueo de los hydrogenos que esperan a Oxigeno

    # Cargamos todos los threads en un array
    for i in range(NUM_HYDROGEN):
        threads.append(hydrogen())
    for i in range(NUM_OXYGEN):
        threads.append(oxygen(i))

    # Asi evitamos un posible orden en caso que nuestros threads tengan caracteristicas diferentes
    random.shuffle(threads)

    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

    # Esperamos que acaben todos los threads
    for threads in threads:
        thread.join()

    print("FINISH")


if __name__ == "__main__":
    main()
