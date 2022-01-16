import threading
import collections

TO_PRODUCE = 1000
BUFFER_SIZE = 10
PRODUCERS = 2
CONSUMERS = 2

#Monitor
class ProducerConsumer(object):
    def __init__(self, size):
        self.buffer = collections.deque([], size)
        self.mutex = threading.Lock()
        self.notFull = threading.Condition(self.mutex)
        self.notEmpty = threading.Condition(self.mutex)

    #Servir
    def append(self, data):
        with self.mutex:
            #if si no esta lleno x2
            while len(self.buffer) == self.buffer.maxlen:
                self.notFull.wait()
            #Metemos "data"
            self.buffer.append(data)
            #Notificacion que ya hay "data"
            self.notEmpty.notify() 

    #Coger
    def take(self):
        with self.mutex:
            while not self.buffer:
                self.notEmpty.wait()
            data = self.buffer.popleft() #Sacar el valor mas a la izquierda de la cola
            self.notFull.notify()
            return data

def producer(buffer):
    id = threading.current_thread().name
    print("Producer {}".format(id))

    for i in range(TO_PRODUCE):
        data = "{} i: {}".format(id, i)
        buffer.append(data)
        print("        {} PRODUEIX: {}".format(id, data))

def consumer(buffer):
    id = threading.current_thread().name
    print("Consumer {}".format(id))

    for i in range(TO_PRODUCE):
        data = buffer.take()
        print("{} CONSUMEIX: {}".format(id, data))


def main():
    threads = []

    buffer = ProducerConsumer(BUFFER_SIZE)
    for i in range(CONSUMERS):
        c = threading.Thread(target=consumer, args=(buffer,))
        threads.append(c)

    for i in range(PRODUCERS):
        p = threading.Thread(target=producer, args=(buffer,))
        threads.append(p)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("End")


if __name__ == "__main__":
    main()
