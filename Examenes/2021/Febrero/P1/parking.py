#Nombre: Jorge González Pascual
#Idea: Se utilizara un montiror que dejara pasar a las entradas si no esta lleno el parking
# y a las Salidas si hay por lo menos una plaza ocupada, de lo contrario dichos 
# procesos se quedaran bloqueados hasta que las condiciones anteriores se cumplan


import threading            # Generar threads
import random               # Generar valores aleatorios
from random import randint  # Uso del random
from time import sleep
from tkinter.tix import Tree

#Constantes
MAX_PARKING = 5
ENTRADAS = 3
SALIDAS = 2

#Rango de numero de proceso Entrada
MIN_ENTRADAS = 0
MAX_ENTRADAS = 10

#Rango tiempo de espera para cada proceso
MIN_PTIME_ENTRADA = 3
MAX_PTIME_ENTRADA = 3

MIN_PTIME_SALIDA = 1
MAX_PTIME_SALIDA = 1

monitor = object()

#Monitor parking
class Parking(object):
    def __init__(self,totalEntradas):
        super().__init__()
        print(f"+++++++++++ Parking activado, nombre de plazas libres: {MAX_PARKING}")

        self.plazas = 0 #Plazas que se estan ocupando
        self.entradasPendientes = totalEntradas #Numero total de las entras que tienen que hacer las entradas
        self.acabar = False #

        #Mutex
        self.mutex = threading.Lock()
        # Condiciones que afectan al mutex
        self.notFull = threading.Condition(self.mutex)
        # Condiciones que afectan al mutex
        self.canExit = threading.Condition(self.mutex)
    
    #Metodo que returna si se han ocupado todas las entradas
    def isFinished(self):
        with self.mutex:
            for i in range(ENTRADAS):
                if self.entradasPendientes[i] != 0:
                    return False
            return True

    #Metodo que controla las entradas mientras haya disponibles plazas
    def entrar(self,entradaId,nEntradas):
        with self.mutex:
            #Mientras las plazas esten llenas
            while(self.plazas == MAX_PARKING):
                self.notFull.wait()
            
            #Sumamos una plaza
            self.plazas+=1
            #Decrementamos una entrada que queda por hacer
            self.entradasPendientes[entradaId]-=1
            print(f"**********  Barrera: E{entradaId} # Entradas: {nEntradas} / Plazas ocupadas: {self.plazas}")

            self.acabar = True
            for i in range(ENTRADAS):
                if self.entradasPendientes[i] != 0:
                    self.acabar = False
            if self.acabar:
                print(f"+++++++++++ Parking cerrado. Se han quedado: {self.plazas} coches")

            #Avisamos que pueden salir
            self.canExit.notify() #Avisamos de que no esta vacio

    #Metodo que controla las salidas, si no hay ninguna plaza se bloqueran
    def salir(self,salidaId,nSalidas):
        with self.mutex:
            #Mientras haya una plaza ocupada
            while(self.plazas == 0):
                self.canExit.wait()
            
            #Restamos una plaza
            self.plazas-=1
            print(f"----------  Barrera: S{salidaId} # Salidas: {nSalidas} / Plazas ocupadas: {self.plazas}")

            #              >0
            if self.plazas > 0:
                self.canExit.notifyAll() #Si sigue habiendo plazas puedran salir
            self.notFull.notify() #Avisamos que no lleno

#Proceso salida
class Salida(threading.Thread):
    def __init__(self,n):
        super().__init__()
        self.id = n
        self.nSalidas = 0 #Contador de salidas
    def run(self):
        global monitor
        print(f"    Barrera de salida S{self.id} ON")

        #Mintras no se hayan realizado todas las entradas
        while not monitor.isFinished():
            #Esperar un tiempo para salir
            sleep(randint(MIN_PTIME_SALIDA,MAX_PTIME_SALIDA))
            self.nSalidas+=1

            #Salir
            monitor.salir(self.id,self.nSalidas)

        print(f"    Barrera de salida S{self.id} OFF")


#Proceso entrada
class Entrada(threading.Thread):
    def __init__(self,nid,n):
        super().__init__()
        self.id = nid
        self.nEntradas = n #Numero de entradas que realizara
    
    def run(self):
        global monitor
        print(f"Barrera de entrada E{self.id} ON")
        print(f"Barrera de entrada E{self.id} se preveen {self.nEntradas}")

        for i in range(self.nEntradas):
            #Esperar a entrar
            sleep(randint(MIN_PTIME_ENTRADA,MAX_PTIME_ENTRADA))

            #Mirar de entrar
            monitor.entrar(self.id, i+1)

        print(f"Barrera de entrada E{self.id} OFF")

#Main
def main():
    global monitor

    print(f"SIMULACION DEL PAKING GRATUITO")

    entradas = []
    for i in range(ENTRADAS):
        entradas.append(randint(MIN_ENTRADAS,MAX_ENTRADAS))

    #Monitor
    monitor = Parking(entradas)

    #Declaracion de procesos
    threads = []
    for i in range(ENTRADAS):
        threads.append(Entrada(i,entradas[i]))
    for i in range(SALIDAS):
        threads.append(Salida(i))

    # Start todos threads
    for t in threads:
        t.start()
    # Esperar a que los threads hayan acabado
    for t in threads:
        t.join()
    
    print(f"FIN DE LA SIMULACION")


if __name__ == "__main__":
    main()