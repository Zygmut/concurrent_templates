import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                        format='[%(threadName)-2s] %(message)s',
                        )

# Const
PROPORTION= 0.33 
OPERATIONS = 100
NUM_READERS = 3
NUM_WRITERS = 5


# Vars
monitor = object()
counter = 0

class MonitorRW(object):

    def __init__(self):
        self.readers = 0 
        self.writers = False
        self.mutex = threading.Lock()
        self.OK_to_read = threading.Condition(self.mutex)
        self.OK_to_write = threading.Condition(self.mutex)

    def start_read(self):
        with self.mutex:
            while self.writers:
                self.OK_to_read.wait()
            
            self.readers += 1
            self.OK_to_read.notify()

    def end_read(self):
        with self.mutex:
            self.readers -= 1
            if self.readers == 0:
                self.OK_to_write.notify()

    def start_write(self):
        with self.mutex:
            while (not self.writers == 0) and (not self.readers==0):
                self.OK_to_write.wait()
            
            self.writers =True 

    def end_write(self):
        with self.mutex:
            self.writers = False

            self.OK_to_read.notify()
            self.OK_to_write.notify()


class Reader(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global counter, monitor
        threading.currentThread().name = type(self).__name__ + "-" + str(int(threading.currentThread().name.split("-")[1]) - NUM_WRITERS)
        logging.debug("Init")
        for i in range(int(OPERATIONS*PROPORTION)):
            monitor.start_read()
            logging.debug(f"Counter: {counter}")
            monitor.end_read()

class Writer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global counter, monitor
        threading.currentThread().name = type(self).__name__ + "-" + threading.currentThread().name.split("-")[1]
        logging.debug("Init")
        for i in range(int(OPERATIONS*(1-PROPORTION))):
            monitor.start_write()
            counter += 1
            monitor.end_write()
            logging.debug("Incrementa")

def main():
    global monitor
    threads = [] 
    monitor = MonitorRW()

    for i in range(NUM_WRITERS):
        threads.append(Writer())
    
    for i in range(NUM_READERS):
        threads.append(Reader())

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("End")    

if __name__ == "__main__":
    main()