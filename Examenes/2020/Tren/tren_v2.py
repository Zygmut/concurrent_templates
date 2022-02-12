#By: PlantanosVerdes
import threading            # Generar threads
from random import randint  # Generar valores aleatorios
from time import sleep      # Realizar sleeps
import random               # Generación de números aleatorios

CAPACIDAD_TREN = 4

# Personas en la ejecucion
MIN_PERSONAS = 5
MAX_PERSONAS = 10

# Tiempo del tren en hacer una vuelta
MIN_TIME = 1
MAX_TIME = 5

# Semaforos:
waitPasajeros = threading.Lock()   # Bloquea a los pasajeros en la "estacion"
mutexPasajeros = threading.Lock()  # Protege el contador de pasajeros
# Bloquea al tren mientras no se haya llenado de pasajeros
waitTren = threading.Lock()
# Bloquea al tren mientras no se haya llenado de pasajeros
waitViaje = threading.Lock()

# Semaforo mutex exclusivamente para print_ft_mutexear
mutex_print = threading.Lock()

# Variables
personas = 0
pasajeros = 0

# Clase Tren que hace viajes esperando a que se vaya llenando el vagon


class Tren(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global waitPasajeros, waitViaje, waitTren

        print(f"Tren: He llegado a la estacion")
        # Bucle infinito
        while True:
            waitPasajeros.release()  # El tren a llegado a la estacion
            print(f"Tren: Abre puertas para subir...")
            waitTren.acquire()  # Esperamos a que el tren se llene

            # Nos vamos de ruta de
            sleep(randint(MIN_TIME, MAX_TIME))

            # Desbloqueamos a los pasajeros del vagon
            print(f"Tren: Abre puertas para bajar...")
            waitViaje.release()
            waitTren.acquire()  # Esperamos a que se vacie

# Clase pasajero que va esperando al tren: a que llegue del viaje y/o a la estacion


class Pasajero(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global personas, waitViaje, waitTren, mutexPasajeros, waitPasajeros, pasajeros
        threading.currentThread().name = "Persona" + " " + \
            threading.currentThread().name.split("-")[1]

        while True:
            # Esperar a que llegue el tren
            waitPasajeros.acquire()

            # Subir:
            with mutexPasajeros:
                pasajeros += 1
                print(f"    {threading.currentThread().name}: Subo al tren")
                # Si no se ha llenado y no se ha llegado al numero de personas que hay
                # Las personas al ser un numero aleatorio puede que sea mas pequeño
                # que la capacidad maxima
                if pasajeros < CAPACIDAD_TREN and pasajeros < personas:
                    waitPasajeros.release()  # Pueden pasar mas personas
                else:
                    waitTren.release()  # Desbloqueamos al tren

            # El tren se va a hacer la ruta y le esperamos
            waitViaje.acquire()

            # Bajar:
            with mutexPasajeros:
                pasajeros -= 1
                print(f"    {threading.currentThread().name}: Bajo al tren")
                # Miramos si es el ultimo pasajero
                if pasajeros > 0:
                    waitViaje.release()  # Seguimos desbloqueando a los pasajeros del viaje
                else:
                    waitTren.release()  # Desbloqueamos al tren

# Metodo que realiza un buen print en la terminal


def print_ft_mutex(s):
    global mutex_print

    with mutex_print:
        print(s)

# MAIN


def main():
    global personas, mutex_print, waitPasajeros, waitTren

    waitPasajeros.acquire()  # Previamente el tren no esta y por eso debe de estar bloqueado
    waitTren.acquire()  # Previamente el tren no esta lleno
    # Previamente bloqueados ya que los pasajeros tienen que espera a que venga el tren
    waitViaje.acquire()

    # Pasajeros que habra
    personas = randint(MIN_PERSONAS, MAX_PERSONAS)
    print(f"Personas: {personas}")

    # Declaracion de procesos
    threads = []
    # Pasajeros
    for i in range(personas):
        threads.append(Pasajero())
    # Tren
    threads.append(Tren())

    # Start all threads
    for t in threads:
        t.start()
    # Wait for all threads to complete
    for t in threads:
        t.join()

    print_ft_mutex("FIN DE LA SIMULACION")


if __name__ == "__main__":
    main()
