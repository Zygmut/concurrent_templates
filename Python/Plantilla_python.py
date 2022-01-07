import threading            # Generar threads
from random import randint  # Generar valores aleatorios
from time import sleep      # Sleep/Delay

# Constantes 
NUM_THREADS = 5


class Process(threading.Thread):

    thread_id = 0
    
    def __init__(self, num_thread):
        super().__init__()
        self.thread_id = num_thread

    def run(self):
        print(f"Soy el Thread-{self.thread_id}")


def main():
    threads = []

    # Cargamos todos los threads en un array
    for i in range(NUM_THREADS):
        threads.append(Process(i))

    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

    # Esperamos que acaben todos los threads
    for threads in threads:
        thread.join()

print("End")


if __name__ == "__main__":
    main()