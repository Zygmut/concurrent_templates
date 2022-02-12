#By: Jorge Gonzalalez Pascual
import threading
from turtle import width
import random               # Generar valores aleatorios
from random import randint 
from time import sleep                        # Esperar

FUMADORES = 6       #Numero de fumadores
NO_FUMADORES = 6    #Numero de NoFumadores
SALONES = 3         #Numero de salones
MESAS = 3           #Nuemero de mesas

MIN_COMER = 3 #Tipo minimo para comer 
MAX_COMER = 3 #Tipo maximo para comer

metreMonitor = object()

#Retorna el string adecuado
def getTipo(isFumador):
    if isFumador: return "FUMADOR"
    else: return "NOFUMADOR"


#Clase objeto Salon
class Salon():
    def __init__(self,n):
        self.isFumador = False
        self.Max_Mesas = n
        self.mesa = 0
    
    #Añade una mesa por un cliente
    def anadir_cliente(self):
        self.mesa += 1
    
    #Quita una mesa por un cliente
    def quitar_cliente(self):
        self.mesa -= 1

#Clase Metre (Monitor)
class Metre(object):
    def __init__(self,x,n):
        super().__init__()
        self.MAX_salones = x
        self.MAX_mesas = n

        #Añadimos las mesas a los salones
        self.salones = []   
        for i in range(self.MAX_salones):              #{salon,salon,salon}
            self.salones.append(Salon(self.MAX_mesas)) #salon[i] = {mesa,mesa,mesa}

        self.contadorTotalClientes = 0

        self.mutex = threading.Lock()
        self.tipo = threading.Condition(self.mutex) #Condiciones que afectan al mutex
        self.full = threading.Condition(self.mutex) #Condiciones que afectan al mutex

    #Retorna el numero de mesa disponible segun el tipo
    def salonDisponible(self,tipo):
        numeroSalon = -1
        for i in range(self.MAX_salones):
                #Si no hay nadie se cambia de tipo para adjudicar la mesa
                if (self.salones[i].mesa == 0):
                    self.salones[i].isFumador = tipo

                #Si es del mismo tipo
                if (getTipo(self.salones[i].isFumador) == getTipo(tipo)):
                    #Si hay sitio
                    if (self.salones[i].mesa != self.MAX_mesas):
                        numeroSalon = i
        return numeroSalon
    
    #Metodo para sentar a los clientes
    def sentarse(self,nombre,tipoCliente):
        salonAdjudicado = -1
        tipoSalon = ""
        with self.mutex:
            #Bloqueado mientras no haya salones disponibles
            while (self.contadorTotalClientes == (self.MAX_salones * self.MAX_mesas)):
                self.full.wait()
            
            #Buscar salon segun su tipo, si no hay salones de su tipo, bloqueado
            while (self.salonDisponible(tipoCliente) < 0):
                self.tipo.wait()
            
            salonAdjudicado = self.salonDisponible(tipoCliente) #Recoger el numero del salon adjudicado
            self.contadorTotalClientes += 1

            #Añadimos una mesa a ese cliente
            self.salones[salonAdjudicado].anadir_cliente()
            
            tipoSalon = getTipo(tipoCliente) #Para un correcto print
            print(f"***** {nombre} Tiene mesa en el salon {salonAdjudicado} de tipo {tipoSalon}")
            
            return salonAdjudicado

    #Metodo para pagar un cliente
    def pagar(self,nombre,salon):
        with self.mutex:
            self.salones[salon].quitar_cliente() 

            #Si la mesa se deja vacia
            if (self.salones[salon].mesa == 0):
                self.tipo.notifyAll()

            self.contadorTotalClientes -= 1

            #Si hay sitio disponible
            if (self.contadorTotalClientes != (self.MAX_salones * self.MAX_mesas)):
                self.full.notifyAll()
            
            #FALTARIA MIRAR EN QUE CASO SE LIBERA
            print(f"***** Se libera el salon {salon} de tipo {getTipo(self.salones[salon].isFumador)}")
            print(f"***** Adios {nombre}")

#Clase del cliente der restaurante (Proceso)
class Cliente(threading.Thread):
    def __init__(self,fumador):
        super().__init__()
        self.isFumador = fumador
    
    def run(self):
        global metreMonitor
        threading.currentThread().name = "Cliente"+ "-" + threading.currentThread().name.split("-")[1]
        
        #Pide sentarse
        salon = metreMonitor.sentarse(threading.currentThread().name,self.isFumador) #Espera que haya un salon disponible
        print(f"{threading.currentThread().name}: Me gusta el salon {salon}")

        sleep(randint(MIN_COMER,MAX_COMER)) #Come
        
        #Pide la cuenta para pagar
        print(f"{threading.currentThread().name}: Ya he comido, la cuenta por favor")
        metreMonitor.pagar(threading.currentThread().name,salon) #Se va

def main():
    global metreMonitor

    #Monitor
    metreMonitor = Metre(SALONES,MESAS)

    #Declaracion de procesos
    threads = []
    for i in range(FUMADORES):
        threads.append(Cliente(True))
    for i in range(NO_FUMADORES):
        threads.append(Cliente(False))
    # Start all threads
    for t in threads:
        t.start()
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print("FIN DE LA SIMULACION")


if __name__ == "__main__":
    main()