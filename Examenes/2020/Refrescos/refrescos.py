#By PlatanosVerdes
import threading
from turtle import width
import random               # Generar valores aleatorios
from random import randint 
from time import sleep                        # Esperar

MIN_COMPRAS = 0
MAX_COMPRAS = 5

MIN_CLIENTES = 1
MAX_CLIENTES = 7

MIN_REPONEDORES = 1
MAX_REPONEDORES = 7

MAX_PRODUCTOS = 10

#Monitor
maquinaMonitor= object()

class MaquinaMonitor(object):
    def __init__(self,size):
        self.clientes = 0 #Numero de clientes que habra durante la ejecucion

        self.actual_consumiciones = 0 #Productos en la maquina
        self.max_consumiciones = size #Maximo de productos en la maquina
        
        self.mutex = threading.Lock()
        self.notFull = threading.Condition(self.mutex) #Condiciones que afectan al mutex
        self.notEmpty = threading.Condition(self.mutex) #Condiciones que afectan al mutex

    #Añadir consumidores
    def add_consumidor(self):
        with self.mutex:
            self.clientes += 1

    #Quitar consumidores
    def delete_consumidor(self):
        with self.mutex:
            self.clientes -= 1
            #Desbloquear a los reponedores
            if self.clientes == 0:
                self.notFull.notifyAll()
    
    #Consumidores
    def get_consumidores(self):
        with self.mutex:
            return self.clientes

    #Coger un producto
    def take(self):
        with self.mutex:
            #Condicion para saber si la maquina esta vacia
            while (self.actual_consumiciones == 0):
                self.notEmpty.wait() #Esperar a que no este vacio
            #Consumir
            self.actual_consumiciones = self.actual_consumiciones - 1
            #Maquina no esta llena
            self.notFull.notify()

    #Reponer
    def replenish(self):
        with self.mutex:
            while (self.actual_consumiciones == self.max_consumiciones) and (self.clientes > 0): #+1 porque si no, da errores
                self.notFull.wait()
                
            #Reponer
            self.actual_consumiciones = self.max_consumiciones
            self.notEmpty.notify() #Notificar de que no esta Vacia

class Cliente(threading.Thread):
    def __init__(self):
        super().__init__()
        self.nCompras = random.randint(MIN_COMPRAS,MAX_COMPRAS)
        maquinaMonitor.add_consumidor()
    
    def run(self):
        threading.currentThread().name = "Cliente"+ "-" + threading.currentThread().name.split("-")[1]
        print(f"*{threading.currentThread().name}: hare {self.nCompras} compras en la maquina.")
        
        #Si hay reponedores, no bloqueamos, nos vamos
        if reponedores > 0:
            for i in range(self.nCompras):
                maquinaMonitor.take()
                print(f"*{threading.currentThread().name}: compro un refresco. Consumicion: {i+1}/{self.nCompras} ")
                sleep(randint(1,2))
                
            maquinaMonitor.delete_consumidor()
            print(f"*{threading.currentThread().name} Adios. Numero de clientes: {maquinaMonitor.get_consumidores()}")
        else:
            print(f"*{threading.currentThread().name} No hay nadie en la maquina. Chao!!")


class Reponedor(threading.Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        threading.currentThread().name = "Reponedor"+ "-" + threading.currentThread().name.split("-")[1]
        print(f"{threading.currentThread().name}: hola")
        
        while (maquinaMonitor.get_consumidores() > 0):
            maquinaMonitor.replenish()
            print(f"{threading.currentThread().name}: lleno la maquina")
            sleep(randint(7,10))
        
        print(f"{threading.currentThread().name} ya no hay mas clientes. Adios")


def main():
    global maquinaMonitor, clientes, reponedores

    #Monitores
    maquinaMonitor = MaquinaMonitor(MAX_PRODUCTOS)

    #Clientes y reponedores aleatorios
    clientes = randint(MIN_CLIENTES,MAX_CLIENTES)
    reponedores = randint(MIN_REPONEDORES,MAX_REPONEDORES)

    #Array de todos los threads
    threads = []

    print(f"En la maquina hay: {clientes} clientes y {reponedores} reponedores")
    for i in range(clientes):
        threads.append(Cliente())

    for i in range(reponedores):
        threads.append(Reponedor())

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("End")


if __name__ == "__main__":
    main()