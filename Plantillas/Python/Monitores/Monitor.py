from sre_parse import REPEAT_CHARS
import threading            # Generar threads
import random               # Generar valores aleatorios
from random import randint
import logging              # Debug más elegante
from time import sleep      # Sleep/Delay

# Definir el entorno de log
logging.basicConfig(level=logging.DEBUG,
                    format='[%(threadName)-2s] %(message)s',
                    )

REPEATS_INCREASES = 5
REPEATS_DECREMENTS = 5

INCREASER_COUNT = 3
DECREASER_COUNT = 1

# Objeto Monitor
monitor = object()


class Monitor(object):
    def __init__(self):  # o def __init__(self,size):
        #Contador: Ejemplo
        self.contador = 0  # Contador que se modificara en el monitor
        self.Max_cont = 5  # Maximo valor del contador

        self.mutex = threading.Lock()
        # Condiciones que afectan al mutex
        self.notMax = threading.Condition(self.mutex)
        # Condiciones que afectan al mutex
        self.notZero = threading.Condition(self.mutex)

    # Metodos del Monitor:
    def increase_counter(self):
        with self.mutex:
            # Conidicion para dejarlo bloqueado
            while (self.contador == self.Max_cont):
                self.notMax.wait()

            self.contador += 1  # Incremento de cavor
            print(f"[Monitor]: Counter : {self.contador}")
            self.notZero.notify()
            self.notMax.notify()

    def decrement_counter(self):
        with self.mutex:
            # Conidicion para dejarlo bloqueado
            while (self.contador == 0):
                self.notZero.wait()

            self.contador -= 1  # Incremento de cavor
            print(f"[Monitor]: Counter : {self.contador}")
            self.notMax.notify()
            self.notZero.notify()


class Increaser(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        # Monitor Global
        global monitor

        threading.currentThread().name = type(self).__name__ + "-" + \
            threading.currentThread().name.split("-")[1]
        logging.debug("Init")

        for i in range(REPEATS_INCREASES):
            monitor.increase_counter()
            logging.debug("Increase counter")

        logging.debug("Me voy")


class Decrementer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        # Monitor Global
        global monitor

        threading.currentThread().name = type(self).__name__ + "-" + \
            str(int(threading.currentThread().name.split(
                "-")[1]) - INCREASER_COUNT)
        logging.debug("Init")
        for i in range(REPEATS_DECREMENTS):
            monitor.decrement_counter()
            logging.debug("Decrement counter")

        logging.debug("Me voy")


def main():
    global monitor
    threads = []

    # Inicializacion del monitor
    monitor = Monitor()

    # Cargamos todos los threads en un array
    for i in range(INCREASER_COUNT):
        threads.append(Increaser())

    for i in range(DECREASER_COUNT):
        threads.append(Decrementer())

    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

    # Esperamos que acaben todos los threads
    for threads in threads:
        thread.join()

    print("End")


if __name__ == "__main__":
    main()
