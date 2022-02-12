import threading            # Generar threads
import random               # Generar valores aleatorios
from random import randint  # Uso del random
from time import sleep

# Variables:
# Numero de lobos
MIN_LOBOS = 2
MAX_LOBOS = 2

# Numero de abejas
MIN_OBEJAS = 3
MAX_OBEJAS = 3

# Numero de veces que iran a beber
MIN_SED = 1
MAX_SED = 1
# Velocidades
MIN_BEBER = 3  # Tipo minimo para beber
MAX_BEBER = 4  # Tipo maximo para beber

#Minimo de obejas que debe de haber para no morir
MIN_TO_NOTDIE = 2

# Objeto Monitor
monitor = object()

class Rio(object):
    def __init__(self):
        super().__init__()

        # Mutex
        self.mutex = threading.Lock()
        # Condicion de bloqueo
        self.esperandoEntrar = threading.Condition(self.mutex)
        self.esperandoSalir = threading.Condition(self.mutex)

        # Contador Lobo en el rio
        self.lobos = 0 
        # Contador Obejas en el rio
        self.obejas = 0
        self.obejas_esperando_entrar = 0
        self.obejas_esperando_salir = 0

    # Un oso entra al rio
    def entry_lobo(self):
        with self.mutex:
            self.lobos += 1
            print(f"{threading.currentThread().name}: Entro al rio, hay {self.lobos} lobos")
            if self.obejas < MIN_TO_NOTDIE and self.obejas > 0:
                print(f"{threading.currentThread().name}: Ñam Obeja")

    # Un oso sale del rio
    def exit_lobo(self):
        with self.mutex:
            self.lobos -= 1
            print(f"{threading.currentThread().name}: Salgo del rio, hay {self.lobos} lobos")

    #No se puede dejar entrar a una obeja sola
    def entry_obeja(self):
        with self.mutex:
            self.obejas_esperando_entrar += 1

            #Si hay mas obejas esperando para no morir, pueden pasar y avisan a todas
            if self.obejas_esperando_entrar >= MIN_TO_NOTDIE:
                self.esperandoEntrar.notify()
            else:
                #Si no pueden pasar esperan
                while (self.obejas_esperando_entrar < MIN_TO_NOTDIE and self.obejas == 0):
                    print(f"***{self.obejas_esperando_entrar} obejas esperando a entrar....")
                    self.esperandoEntrar.wait()
            
            #Pasan al rio:
            self.obejas += 1
            print(f"{threading.currentThread().name}: Entro al rio, hay {self.obejas} obejas")
            self.obejas_esperando_entrar -= 1 #Ya no esperan
    
    #No se puede dejar a una obeja sola al salir
    def exit_obeja(self):
        with self.mutex:
            self.obejas_esperando_salir += 1
            #Si no deja a 1 obeja sola y hay peticiones para salir avisa
            if self.obejas >= MIN_TO_NOTDIE and self.obejas_esperando_salir >= MIN_TO_NOTDIE:
                self.esperandoSalir.notify()
            else:
                #Mintras deje a la obeja sola se quedara bloqueada
                while self.obejas == MIN_TO_NOTDIE:
                    print(f"***{self.obejas_esperando_salir} obejas esperando a salir....")
                    self.esperandoSalir.wait()
                    #sleep(0.1)
            
            #Sale:
            self.obejas -= 1
            print(f"{threading.currentThread().name}: Salgo del rio, hay {self.obejas} obejas")
            self.obejas_esperando_salir -= 1 #Ya no espera

# Clase thread de un LOBO
class Lobo(threading.Thread):
    def __init__(self, npass):
        super().__init__()
        self.repeteats = npass  # Veces que tiene sed

    def run(self):
        global monitor
        threading.currentThread().name = "Lobo" + "-" + \
            threading.currentThread().name.split("-")[1]
        print(f"Hola soy el {threading.currentThread().name}. Ire a beber {self.repeteats} veces")

        for i in range(self.repeteats):
            #Va al rio
            monitor.entry_lobo()
            #Bebe
            sleep(randint(MIN_BEBER,MAX_BEBER))
            #Seva del rio
            monitor.exit_lobo()

# Clase thread de una OBEJA
class Obeja(threading.Thread):
    def __init__(self, npass):
        super().__init__()
        self.repeteats = npass  # Veces que tiene sed

    def run(self):
        global monitor

        threading.currentThread().name = "Obeja" + "-" + \
            threading.currentThread().name.split("-")[1]
        print(f"Hola soy la {threading.currentThread().name}. Ire a beber {self.repeteats} veces")

        for i in range(self.repeteats):
            #Va al rio
            monitor.entry_obeja()
            #Bebe
            sleep(randint(MIN_BEBER,MAX_BEBER))
            #Seva del rio
            monitor.exit_obeja()


def main():
    global monitor

    # Monitor
    monitor = Rio()

    print(f"-- SIMULACION LOBOS & OBEJAS --")
    # Variables
    Lobos = randint(MIN_LOBOS, MAX_LOBOS)
    Obejas = randint(MIN_OBEJAS, MAX_OBEJAS)
    print(f"Lobos: {Lobos} & Obejas: {Obejas}")

    # Declaracion de procesos
    threads = []

    for n in range(Lobos):
        threads.append(Lobo(randint(MIN_SED, MAX_SED)))
    for n in range(Obejas):
        threads.append(Obeja(randint(MIN_SED, MAX_SED)))

    # Start all threads
    for t in threads:
        t.start()
    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("FIN DE LA SIMULACION")


if __name__ == "__main__":
    main()
