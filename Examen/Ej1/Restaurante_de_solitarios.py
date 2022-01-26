# Rubén Palmer Pérez: 2022GenerP1

import threading            # Generar threads
import random               # Generar valores aleatorios
from random import randint  
from time import sleep      # Sleep/Delay

# Numero de procesos de cada tipo 
NUM_FUMADOR = 6
NUM_NO_FUMADOR = 6

# Rango de velocidad de los clientes 
MIN_CLIENT_TIME = 1
MAX_CLIENT_TIME = 5

# Diferentes tipos de salones
NON_SMOKER = 0   
SMOKER = 1
NONE = 2

# Control del salon
NUM_SALONES = 3 
NUM_MESAS = 3

NAMES = ["Kevin", "Luis", "Aitor", "Noah", "Marc", "Aimar", "Neus", "Elena", "Uxia", "Nora", "Manuela", "Soraya"]

camarero = object

# Estructura de datos para gestionar los salones 
class Salon():
    def __init__(self, name, num_mesas):
        self.name = name                # Nombre del salon
        self.num_mesas = num_mesas      # Numero de mesas totales que tiene el salon
        self.num_mesas_ocupadas = 0
        self.type = NONE                # Tipo de salon (NONE, SMOKERS, NONSMOKERS)
        self.comensales = []            # Array de comensales dentro del salon

# Monitor
class Camarero(object):
    def __init__(self, restaurante):
        self.restaurante = restaurante
        self.mutex = threading.Lock()

        # Condiciones para fumadores 
        self.notfull_smokers = threading.Condition(self.mutex) 

        # Condiciones para no fumadores 
        self.notfull_non_smokers = threading.Condition(self.mutex) 

    # Devuelve el primer salon de su tipo que tenga sitio.
    def check_first(self, type):
        for salon in self.restaurante:
            if (salon.type == type or salon.type == NONE) and salon.num_mesas_ocupadas != salon.num_mesas: 
               return salon

        return None

    # Devuelve el salon donde se encuentra una persona
    def find_salon(self, client_name, client_type):
        for salon in self.restaurante:
            if salon.type == client_type:
                for comensal in salon.comensales:
                    if comensal == client_name:
                        return salon

        return None

    # Devuelve la capacidad máxima que puede tomar el restaurante con respecto al tipo de cliente (fumador/no fumador) 
    def get_max_capacity(self, type):
        capacity = 0
        for salon in self.restaurante:
            if salon.type == type or salon.type == NONE:
                capacity += salon.num_mesas - salon.num_mesas_ocupadas

        return capacity

    # Entrar
    def entrar(self, client_name, client_type):
        with self.mutex:
            # Mientras no haya sitio en los salones de mi tipo

            while(self.get_max_capacity(client_type) == 0): # Mientras no haya capacidad para mi tipo
                print(f"[Camarero] Lo siento {client_name}, no tenemos mesas disponibles para usted ya que es " + ("fumador/a" if client_type == SMOKER else "no fumador/a"))
                if client_type: 
                    self.notfull_smokers.wait()
                else:
                    self.notfull_non_smokers.wait()
            
            salon = self.check_first(client_type)    # Cogemos el primer salon que acceda al tipo del cliente
            if salon.type == NONE:                          # Cambiamos el tipo del salon con respecto al tipo de persona que haya entrado
                salon.type = client_type

            print(f"[Camarero] El Sr./Sra. {client_name} tiene mesa en el salon {salon.name} de " + ("fumadores" if salon.type == SMOKER else "no fumadores") )
            salon.comensales.append(client_name)            # Añadimos el comensal a la lista de comensales del salon
            salon.num_mesas_ocupadas += 1                   # Añadimos una mesa ocupada

    # Salir
    def salir(self, client_name, client_type):
        with self.mutex:
            # Podemos salir siempre que queramos porque implicitamente sabemos que estamos dentro
            salon = self.find_salon(client_name, client_type)
            salon.num_mesas_ocupadas -= 1
            salon.comensales.remove(client_name)
            print(f"[Camarero] Se alibera un sitio en el salon {salon.name} de " + ("fumadores" if salon.type == SMOKER else "no fumadores") + f". Quedan {salon.num_mesas_ocupadas} comensales")
            
            if salon.type == SMOKER:
                self.notfull_smokers.notify()
            else:                               # Necesariamente tiene que ser de no fumadores porque estabamos antes 
                self.notfull_non_smokers.notify()

            if salon.num_mesas_ocupadas == 0 :  # Miramos si en ese salon quedan comensales
                salon.type = NONE
                print(f"[Camarero] El salon {salon.name} queda vacio")
            
            print(f"[Camarero] Espero que haya disfrutado {client_name}")

class Cliente(threading.Thread):

    def __init__(self, name, is_fumador):
        super().__init__()
        self.name = NAMES[name] + "-" + ("F" if is_fumador else "NF")
        self.tipo = is_fumador                            # Definir si es fumador o no
        self.vel = randint(MIN_CLIENT_TIME, MAX_CLIENT_TIME) # Definimos la velocidad de los sleep

    # Pediremos entrar al camarero 
    def pedir_entrar(self):
        global camarero
        print(f"[{self.name}] Pide al camarero una mesa")
        camarero.entrar(self.name.split("-")[0], self.tipo)

    # Comeremos. Esencialmente es un sleep 
    def comer(self):
        print(f"[{self.name}] Empieza a comer")
        sleep(self.vel)
    
    # Perdiremos salir al camarero
    def pedir_salir(self):
        global camarero
        print(f"[{self.name}] He acabado de comer y pido la cuenta")
        camarero.salir(self.name.split("-")[0], self.tipo)

    def run(self):
        global camarero
        print(f"[{self.name}] Quiero comer y mi velocidad es {self.vel}")

        self.pedir_entrar()
        self.comer()
        self.pedir_salir()



def main():
    global camarero

    threads = []

    # Creamos el restaurante
    restaurante = [Salon(i, NUM_MESAS) for i in range(NUM_SALONES)]
    
    # Inicializamos el camarero con su restaurante asignado
    camarero = Camarero(restaurante)

    # Cargamos todos los threads en un array
    for i in range(NUM_FUMADOR):
        threads.append(Cliente(i,SMOKER))

    for i in range(NUM_NO_FUMADOR):
        threads.append(Cliente(i+NUM_FUMADOR,NON_SMOKER))
   

    # Ejecutamos todos los threads
    for thread in threads:
        thread.start()

    # Esperamos que acaben todos los threads
    for threads in threads:
        thread.join()

    print("End")


if __name__ == "__main__":
    main()