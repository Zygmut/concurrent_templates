import threading            # Generar threads
import random               # Generar valores aleatorios
from random import randint  # Uso del random
from time import sleep

CLIENTES = 4

NOMBRES = ["Paco", "Maria", "Ruben", "Paula", "Pablo", "Alberto",
           "Elena", "Kieran", "Irene", "Alicia", "Ramona", "Patricio"]
SUSHIS = ["Nigiri salmon", "Sashimi Atun", "Makis de cangrejo",
          "Shasimi de anguila", "Nigiris de tortilla"]
TIPOS_SUSHIS = 5

MAX_CANTIDAD = 10
MIN_CANTIDAD = 1

# Velocidades
MIN_COMER = 1  # Tipo minimo para comer
MAX_COMER = 3  # Tipo maximo para comer

# Objeto Monitor
monitor = object()

mutex_print = threading.Lock()          # Semaforo mutex exclusivamente para print_ft_mutexear
#Metodo que realiza un buen print_ft_mutex en la terminal
def print_ft_mutex(frase):
    global mutex_print
    with mutex_print:
        print(frase)

# Clase Pieza Sushi la bandeja tendra x piezas
class PiezaSushi():
    def __init__(self, tipo, n):
        self.tipo = tipo
        self.cantidad = n

class Monitor_bandeja(object):
    def __init__(self):
        super().__init__()
        # Mutex monitor
        self.mutex = threading.Lock()
        # Condiciones que afectan al mutex
        self.comer = threading.Condition(self.mutex)

        self.comiendo = False  # Variable que muestra si alguien esta comiendo
        self.bandejaSushi = []  # Bandeja con todas las piezas
        
        #Inicializar la bandeja
        for i in range(TIPOS_SUSHIS):
            numero = randint(MIN_CANTIDAD,MAX_CANTIDAD)
            self.bandejaSushi.append(PiezaSushi(SUSHIS[i],numero))
            print(f"{self.bandejaSushi[i].tipo} - {self.bandejaSushi[i].cantidad}")

    # Metodo que devuelve si hay sushis en la bandeja para poder comer
    def can_eat(self):
        can = False
        with self.mutex:
            if len(self.bandejaSushi) > 0:
                can = True
        return can

    # Metodo que mira y espera si puede comer
    def coger(self):
        with self.mutex:
            # Mientras haya alguien comiendo: esperar
            while (self.comiendo == True):
                self.comer.wait()
            # Podemos comer
            self.comiendo = True

    # Metodo que llamara un cliente para comer una pieza de la bandeja
    def comer_sushi(self,nombre):
        global mutex_print

        with self.mutex:
            # Cogemos una pieza
            pieza = randint(0, len(self.bandejaSushi)-1)
            #Restamos una pieza
            self.bandejaSushi[pieza].cantidad -= 1

            #Si se ha quedado sin quitamos la pieza de la bandeja
            print_ft_mutex(f"**{nombre}: Coge {self.bandejaSushi[pieza].tipo}. Todavia quedan {self.bandejaSushi[pieza].cantidad}")
            if(self.bandejaSushi[pieza].cantidad ==0):
                #La quitamos de la bandeja si ya no hay mas
                print_ft_mutex(f"***** Se han acabado los {self.bandejaSushi[pieza].tipo}")
                self.bandejaSushi.pop(pieza)

            #Dejamos de comer
            self.comiendo = False
            #Avisamos
            self.comer.notify()

#Clase cliente que cogera y comera piezas de Sushi
class Cliente(threading.Thread):
    def __init__(self,n):
        super().__init__()
        self.nombre = n
    
    def run(self):
        global monitor, mutex_print

        print_ft_mutex(f"Hola soy {self.nombre}")
        #Mientras haya piezas
        while monitor.can_eat():
            print_ft_mutex(f"{self.nombre}: Voy a coger")
            monitor.coger()
            monitor.comer_sushi(self.nombre)
            print_ft_mutex(f"{self.nombre}: Ya he comido")
            sleep(randint(MIN_COMER,MAX_COMER))
        print_ft_mutex(f"{self.nombre}: Ya no hay mas. Adios")

def main():
    global monitor

    #Monitor
    monitor = Monitor_bandeja()

    #Declaracion de procesos
    threads = []
    n = 0
    for n in range(CLIENTES):
        threads.append(Cliente(NOMBRES[n]))

    # Start all threads
    for t in threads:
        t.start()
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print("FIN DE LA SIMULACION")


if __name__ == "__main__":
    main()