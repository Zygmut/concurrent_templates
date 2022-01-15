import threading  # Generar un int aleatorio
from random import randint
from time import sleep  # Esperar
import random  # Generación de números aleatorios

MAX_TRAIN = 4
MAX_PERSONS = 7
MIN_PERSONS = 4

# semaforos:
puertasInTren = threading.Lock()
puertasOutTren = threading.Lock()
waitPuertas = threading.Semaphore(0)
mutexCapacity = threading.Lock()

capatity = 0 #Capacidad actual en el vagon


class Train(threading.Thread):
    def __init__(self):
        super().__init__()
        # Bloqueos Iniciales
        # Bloqueo inicial para que las personas esperen a que el tren llegue
        puertasInTren.acquire()  # Al principio las puertas del tren estan cerradas
        puertasOutTren.acquire()  # Al principio las puertas del tren estan cerradas

    def run(self):
        global nPersonas

        print(f"El tren acaba de llegar. Capacidad Maxima: {MAX_TRAIN}")

        nTravels = 0
        while True:
            puertasInTren.release()  # Abrir Puertas
            print(f"Tren abre las puertas subir")
            waitPuertas.acquire()  # Espera a cerrar puertas
            # Le hacen el release
            puertasInTren.acquire()  # Cierra puertas

            print(f"El tren se va. Vuelta: {nTravels}")
            nTravels = 1 + nTravels
            sleep(randint(1, 2))  # Se va

            # Llega
            puertasOutTren.release()  # Abrir Puertas
            print(f"Tren abre las puertas para bajar")
            waitPuertas.acquire()  # Espera a cerrar puertas
            # Le hacen el release
            puertasOutTren.acquire()  # Cierra puertas


class Persons(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        global capatity, nPersonas
        threading.currentThread().name = "Persona" + " " + \
            threading.currentThread().name.split("-")[1]

        while True:
            with puertasInTren:
                with mutexCapacity:
                    capatity = capatity + 1
                    print(f"{threading.currentThread().name} sube al tren")
                    if (capatity == MAX_TRAIN):
                        print(f"{threading.currentThread().name}: capatity: {capatity} == MAX_TRAIN: {MAX_TRAIN}")
                        waitPuertas.release()  # Desbloqueo al tren
                    elif ((capatity == nPersonas) and (nPersonas < MAX_TRAIN)):
                        print(f"** {threading.currentThread().name}: capatity {capatity} == nPersonas {nPersonas}")
                        waitPuertas.release()  # Desbloqueo al tren

            with puertasOutTren:
                sleep(randint(1, 2))  #Aleatorio?
                with mutexCapacity:
                    capatity = capatity - 1
                    print(f"{threading.currentThread().name} baja del tren")
                    if (capatity == 0):
                        waitPuertas.release()  # Desbloqueo al tren


def main():

    global nPersonas, waitPuertas, puertasInTren, puertasOutTren

    threads = []

    print(f"Simulacion Tren")

    nPersonas = randint(MIN_PERSONS, MAX_PERSONS)

    # Cargamos todos los threads en un array
    print(f"Hay {nPersonas} personas:")
    for i in range(nPersonas):
        print(f"Persona {i+1}")
        threads.append(Persons())  # Personas
    threads.append(Train())  # Tren

    # Asi evitamos un posible orden en caso que nuestros threads tengan caracteristicas diferentes
    random.shuffle(threads)

    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
