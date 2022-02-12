import threading            # Generar threads
import random               # Generar valores aleatorios
from random import randint  # Uso del random
from time import sleep

FUMADORES = 6       #Personas no fumadoras
NOFUMADORES = 6     #Personas fumadoras
MESAS = 3           #Numero de mesas por salon del
SALONES = 3         #Numero de salones

#Tipos de salones
FUMADOR = "FUMADOR"
NOFUMADOR = "NOFUMADOR"
NONE =  ""

#Velocidades
MIN_COMER = 3       #Tipo minimo para comer 
MAX_COMER = 4       #Tipo maximo para comer

NOMBRES = ["Paco", "Ruben", "Pablo", "Alberto", "Kieran", "Maria", "Paula", "Elena", "Irene", "Alicia", "Ramona", "Patricio"]

# Objeto Monitor
monitor = object()

#Clase persona Cliente
class Cliente():
    #Constructor
    def __init__ (self,nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

#Clase salon: cada salon tendra "n" mesas
class Salon ():
    #Constructor
    def __init__ (self,n):
        self.tipo = NONE
        self.MAX_Mesas = n
        self.mesas = 0

    #Añade una mesa por un cliente
    def anadir_cliente(self):
        self.mesas += 1
    
    #Quita una mesa por un cliente
    def quitar_cliente(self):
        self.mesas -= 1

#Clase mayordomo que gestionara a los clientes que
#Esta sera el monitor
class Metre(object):
    def __init__(self,x,n):
        super().__init__()
        self.MAX_salones = x
        self.MAX_mesas = n

        #Mutex
        self.mutex = threading.Lock()
        # Condiciones que afectan al mutex
        self.block_fumadores = threading.Condition(self.mutex)
        # Condiciones que afectan al mutex
        self.block_nofumadores = threading.Condition(self.mutex)

        #Añadimos las mesas a los salones:
        self.salones = []   
        for i in range(self.MAX_salones):              #{salon,salon,salon}
            self.salones.append(Salon(self.MAX_mesas)) #salon[i] = {mesa,mesa,mesa}
    
    #Metodo que retorna el primer salon vacio segun el tipo pasado por parametro
    # -1 error o vacio
    def get_salon_tipo(self,tipo):
        for i in range(self.MAX_salones):
            #Si el salon esta vacio
            if self.salones[i].tipo == NONE:
                self.salones[i].tipo = tipo
                return i
            else:
                if self.salones[i].tipo == tipo and self.salones[i].mesas < self.MAX_mesas:
                    return i 
        return -1

    #Metodo que retorna si hay sitio en un salon
    """ def hay_salon_disponible(self):
        for i in range(self.MAX_salones):
                if self.salones[i].mesas < self.MAX_mesas:
                    return True
        return False """

    #Metodo que retorna el numero de mesas ocupadas
    def get_mesas(self,salon):
        return self.salones[salon].mesas

    #Metodo del monitor que bloqueara a los clientes si no hay sitio disponible 
    #segun el tipo de persona que es
    def sentarse(self,Cliente):
        with self.mutex:
            #Bucle el cual se quedaran calados los clientes si no hay sitio segun un tipo
            while(self.get_salon_tipo(Cliente.tipo) < 0):   
                if Cliente.tipo == FUMADOR:
                    #print(f"***** No hay ninguna mesa disponible para {Cliente.nombre} de {Cliente.tipo}")
                    self.block_fumadores.wait()
                else:
                    #print(f"***** No hay ninguna mesa disponible para {Cliente.nombre} de {Cliente.tipo}")
                    self.block_nofumadores.wait()
        
            #Cogemos el salon adjudicado    
            salon = self.get_salon_tipo(Cliente.tipo)
            #Sumamos un cliente
            self.salones[salon].anadir_cliente()

            print(f"***** {Cliente.nombre} Tiene mesa en el salon {salon} de tipo {Cliente.tipo}")
            #Devolvemos al cliente que salon le ha tocado
            return salon 

    #Metodo que llamara una persona al irse y que notificara a los clientes del mismo tipo que hay una mesa libre
    def abandonar (self,Cliente,salon):
        #Entrada al monitor
        with self.mutex:
            #Quitamos al cliente de la mesa
            self.salones[salon].quitar_cliente()
            print(f"***** Se libera una mesa del salon {salon} {Cliente.tipo}, ahora quedan {self.get_mesas(salon)}/{self.MAX_mesas}")
            #Miramos si se ha quedado vacio
            if (self.get_mesas(salon) == 0):
                self.salones[salon].tipo = NONE #Ponemos el salon a vacio
                print(f"***** El salon {salon} ha quedado vacio.")
                self.block_fumadores.notify()
                self.block_nofumadores.notify()
            else:
                #Notificamos que hay un sitio disponible a los clientes que estan esperando
                if Cliente.tipo == FUMADOR:
                    self.block_fumadores.notify()
                else:
                    self.block_nofumadores.notify()
        
            print(f"***** Adios {Cliente.nombre}!")


#Clase thread de un cliente, el cual tendra un CLiente(nombre y tipo)
class P_Cliente(threading.Thread):
    def __init__(self,Cliente):
        super().__init__()
        self.Cliente = Cliente
    
    def run(self):
        global monitor

        print(f"Hola soy: {self.Cliente.nombre} y soy {self.Cliente.tipo}")

        #Esperar a sentarse
        salon = monitor.sentarse(self.Cliente)
        print(f"{self.Cliente.nombre}: Me gusta mucho el salon {salon}")
        
        #Comer
        sleep(randint(MIN_COMER,MAX_COMER))

        #Se va
        print(f"{self.Cliente.nombre}: Ya he comido, la cuenta por favor.")
        monitor.abandonar(self.Cliente,salon)

def main():
    global monitor

    #Monitor
    monitor = Metre(SALONES,MESAS)

    #Declaracion de procesos
    threads = []
    n = 0
    for n in range(FUMADORES):
        threads.append(P_Cliente(Cliente(NOMBRES[n],FUMADOR)))
    for i in range(NOFUMADORES):
        threads.append(P_Cliente(Cliente(NOMBRES[n+i+1],NOFUMADOR)))

    # Start all threads
    for t in threads:
        t.start()
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print("FIN DE LA SIMULACION")


if __name__ == "__main__":
    main()