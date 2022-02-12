#Creado por: PlantanosVerdes
import threading            # Generar threads
from random import randint  # Generar valores aleatorios
from time import sleep      # Realizar sleeps
import random               # Generación de números aleatorios

FUMADORES = 6           #Personas no fumadoras
NOFUMADORES = 6         #Personas fumadoras
N_MESAS = 3             #Numero de mesas por salon del
X_SALONES = 3           #Numero de salones

#Tipos de salones
FUMADOR = "FUMADOR"
NOFUMADOR = "NOFUMADOR"
NONE =  ""

#Velocidades
MIN_COMER = 3       #Tipo minimo para comer 
MAX_COMER = 4       #Tipo maximo para comer

#Nombres
NOMBRES = ["Paco", "Ruben", "Pablo", "Alberto", "Kieran", "Maria", "Paula", "Elena", "Irene", "Alicia", "Ramona", "Patricio"]

#Salones que tiene el restante
SALONES = []   

#Semaforos
mutex_salones = threading.Lock()        # Semaforo mutex para proteger la sc de los salones
nofumadores = threading.Semaphore(0)    # Semaforo que bloquea a los no fumadores
fumadores = threading.Semaphore(0)      # Semaforo que bloquea a los fumadores

mutex_print = threading.Lock()          # Semaforo mutex exclusivamente para print_ft_mutexear

#Clase persona Cliente
class Cliente():
    #Constructor
    def __init__ (self,nombre, tipo):
        super().__init__()
        self.nombre = nombre
        self.tipo = tipo

#Clase salon: cada salon tendra "n" mesas
class Salon ():
    #Constructor
    def __init__ (self,n):
        super().__init__()
        self.tipo = NONE
        self.MAX_Mesas = n
        self.mesas = 0

    #Añade una mesa por un cliente
    def anadir_cliente(self):
        self.mesas += 1
    
    #Quita una mesa por un cliente
    def quitar_cliente(self):
        self.mesas -= 1

#Metodo que realiza un buen print_ft_mutex en la terminal
def print_ft_mutex(s):
    global mutex_print
    with mutex_print:
        print(s)


#Metodo que retorna el primer salon vacio segun el tipo pasado por parametro
# -1 error o vacio
def get_salon_tipo(tipo):
    for i in range(X_SALONES):
        #Si el salon esta vacio
        if SALONES[i].tipo == NONE:
            SALONES[i].tipo = tipo
            return i
        else:
            if SALONES[i].tipo == tipo and SALONES[i].mesas < N_MESAS:
                return i 
    return -1

#Clase cliente FUMADOR
class Fumador(threading.Thread):
    def __init__(self, Cliente):
        super().__init__()
        self.Cliente = Cliente

    def run(self):
        global mutex_salones, fumadores, nofumadores, mutex_print

        #print_ft_mutex(f"{self.Cliente.nombre}: {self.Cliente.tipo}")

        #SENTARSE:
        mutex_salones.acquire()
        salon = get_salon_tipo(self.Cliente.tipo)
        #Si no hay ningun salon disponible:
        while salon < 0:
            print_ft_mutex(f"*** Debes de espera {self.Cliente.nombre} - {self.Cliente.tipo} no hay sitio")
            mutex_salones.release()
            fumadores.acquire()
            
            #Cuando se desbloquee hay que coger un salon
            mutex_salones.acquire()
            salon = get_salon_tipo(self.Cliente.tipo)
        
        #Si hay sitio anadimos el cliente
        SALONES[salon].anadir_cliente()
        print_ft_mutex(f"{self.Cliente.nombre} - {self.Cliente.tipo}: Me gusta mucho el salon {salon}")
        mutex_salones.release()

        #COMER:
        sleep(randint(MIN_COMER,MAX_COMER))
        print_ft_mutex(f"{self.Cliente.nombre} - {self.Cliente.tipo}: Ya he comido, la cuenta por favor.")

        #IRSE:
        mutex_salones.acquire()

        SALONES[salon].quitar_cliente()
        
        #Si el salon se queda vacio:
        if SALONES[salon].mesas == 0:
            SALONES[salon].tipo = NONE

            fumadores.release()
            nofumadores.release()
        else:
            fumadores.release()

        mutex_salones.release()
        print_ft_mutex(f"{self.Cliente.nombre} - {self.Cliente.tipo}: Adios! ")


#Clase cliente NO FUMADOR
class NoFumador(threading.Thread):
    def __init__(self, Cliente):
        super().__init__()
        self.Cliente = Cliente

    def run(self):
        global mutex_salones, fumadores, nofumadores, mutex_print

        #print_ft_mutex(f"{self.Cliente.nombre}: {self.Cliente.tipo}")

        #SENTARSE:
        mutex_salones.acquire()
        salon = get_salon_tipo(self.Cliente.tipo)
        #Si no hay ningun salon disponible:
        while salon < 0:
            print_ft_mutex(f"*** Debes de espera {self.Cliente.nombre} - {self.Cliente.tipo} no hay sitio")
            mutex_salones.release()
            nofumadores.acquire()
            
            #Cuando se desbloquee hay que coger un salon
            mutex_salones.acquire()
            salon = get_salon_tipo(self.Cliente.tipo)
        
        #Si hay sitio anadimos el cliente
        SALONES[salon].anadir_cliente()
        print_ft_mutex(f"{self.Cliente.nombre} - {self.Cliente.tipo}: Me gusta mucho el salon {salon}")
        mutex_salones.release()

        #COMER:
        sleep(randint(MIN_COMER,MAX_COMER))
        print_ft_mutex(f"{self.Cliente.nombre} - {self.Cliente.tipo}: Ya he comido, la cuenta por favor.")

        #IRSE:
        mutex_salones.acquire()

        SALONES[salon].quitar_cliente()
        
        #Si el salon se queda vacio:
        if SALONES[salon].mesas == 0:
            SALONES[salon].tipo = NONE

            fumadores.release()
            nofumadores.release()
        else:
            nofumadores.release()

        mutex_salones.release()
        print_ft_mutex(f"{self.Cliente.nombre} - {self.Cliente.tipo}: Adios! ")

#MAIN
def main():
    global mutex_print

    #Añadimos las mesas a los salones: 
    for i in range(X_SALONES):              #{salon,salon,salon}
        SALONES.append(Salon(N_MESAS))      #salon[i] = {mesa,mesa,mesa}

    #Declaracion de procesos
    threads = []
    n = 0
    for n in range(FUMADORES):
        threads.append(Fumador(Cliente(NOMBRES[n],FUMADOR)))

    for i in range(NOFUMADORES):
        threads.append(NoFumador(Cliente(NOMBRES[n+i+1],NOFUMADOR)))

    # Start all threads
    for t in threads:
        t.start()
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print_ft_mutex("FIN DE LA SIMULACION")


if __name__ == "__main__":
    main()