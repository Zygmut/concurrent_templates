# Rubén

from random import randrange, randint
from time import sleep      # Sleep/Delay
import logging              # Debug más elegante
import random               # Generar valores aleatorios
import threading            # Generar threads


# Definir el entorno de log
logging.basicConfig(level=logging.DEBUG,
                    format='[%(threadName)-2s] %(message)s',
                    )

# Constantes
NUM_ELFS = 9
MAX_ELF_VEL = 1
MIN_ELF_VEL = 5
NUM_QUESTIONS = 2
WAITING_ROOM_SIZE = 3

NUM_DEERS = 9
MAX_DEER_VEL = 10
MIN_DEER_VEL = 30

MAX_SANTA_VEL = 1
MIN_SANTA_VEL = 3

# Variables
deers_ready = False
ready = 0
question_turns = 0
elfs_waiting = 0
deers_waiting = 0

# Semaforos
wake_up_santa = threading.Lock()
resolve_question = threading.Lock()
elf_mutex = threading.Lock()
deer_mutex = threading.Lock()
deer_hitch = threading.Lock()
waiting_room = threading.Lock()


class Santa(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        global wake_up_santa, deers_ready, ready, question_turns, resolve_question, deer_hitch
        threading.currentThread().name = type(self).__name__  # Poner nombre al thread
        while not (ready == 2):
            logging.debug(f"I'm tired, I'll go hit the sack")

            wake_up_santa.acquire()  # Espero hasta que me levanten
            logging.debug(f"I'm awake HO HO HO !")
            if deers_ready:
                # Deers
                deers_ready = False
                ready += 1
                logging.debug(f"Toys are ready!")
                logging.debug(f"Loads the toys")
                logging.debug(f"Until next Christmas!")
                deer_hitch.release()
            else:
                # Elfs
                question_turns += 1
                logging.debug(f"What is the problem?")
                for question in range(WAITING_ROOM_SIZE):
                    logging.debug(
                        f"Helps the elf {question+1}/{WAITING_ROOM_SIZE}")
                    sleep(randint(MAX_SANTA_VEL, MIN_SANTA_VEL))
                    resolve_question.release()

                if question_turns == ((NUM_ELFS*NUM_QUESTIONS)/WAITING_ROOM_SIZE):
                    logging.debug(f"No more questions!")
                    ready += 1

        logging.debug(f"Ends")


class Elf(threading.Thread):

    def __init__(self):
        super().__init__()
        self.velocity = randrange(MAX_ELF_VEL, MIN_ELF_VEL)

    def run(self):
        global elf_mutex, waiting_room, elfs_waiting, resolve_question
        threading.currentThread().name = type(self).__name__ + "-" + \
            threading.currentThread().name.split(
                "-")[1]  # Poner nombre al thread
        logging.debug(f"Init with vel: {self.velocity}")

        for question in range(NUM_QUESTIONS):
            sleep(self.velocity)
            waiting_room.acquire()
            with elf_mutex:
                elfs_waiting += 1

            if elfs_waiting == 3:
                logging.debug(
                    f"I have a question and I'm {elfs_waiting}, SANTAAA !!!! ")
                wake_up_santa.release()
            else:
                logging.debug(f"I have a question and I'm {elfs_waiting}")
                waiting_room.release()

            resolve_question.acquire()
            with elf_mutex:
                elfs_waiting -= 1
                if elfs_waiting == 0:
                    waiting_room.release()

        logging.debug(f"I'm done with questions")


class Deer(threading.Thread):

    def __init__(self):
        super().__init__()
        self.velocity = randrange(MAX_DEER_VEL, MIN_DEER_VEL)

    def run(self):
        global deer_mutex, deers_waiting, wake_up_santa, deers_ready
        threading.currentThread().name = type(self).__name__ + "-" + \
            str(int(threading.currentThread().name.split(
                "-")[1])-NUM_ELFS)  # Poner nombre al thread

        logging.debug(f"Init with vel: {self.velocity}")
        sleep(self.velocity)
        with deer_mutex:
            deers_waiting += 1
            if deers_waiting == 9:
                logging.debug(f"Arrives and is the last one !")
                deers_ready = True
                wake_up_santa.release()
            else:
                logging.debug(f"Arrives")

        deer_hitch.acquire()
        with deer_mutex:
            deers_waiting -= 1
            if not deers_waiting == 0:
                deer_hitch.release()

        logging.debug(f"Ready and hitched")
        logging.debug(f"Ends")


def main():
    global wake_up_santa
    threads = []

    # Cargamos todos los threads en un array
    for i in range(NUM_ELFS):
        threads.append(Elf())

    for i in range(NUM_DEERS):
        threads.append(Deer())
    threads.append(Santa())

    # Asi evitamos un posible orden en caso que nuestros threads tengan caracteristicas diferentes
    random.shuffle(threads)

    resolve_question.acquire()
    wake_up_santa.acquire()
    deer_hitch.acquire()

    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

    # Esperamos que acaben todos los threads
    for threads in threads:
        thread.join()

    print("End")


if __name__ == "__main__":
    main()