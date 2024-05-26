from listQueue import ListQueue
import threading
import time

class Producer:
    def __init__(self, items):
        self.__alive = True
        self.items = items
        self.pos = 0
        self.worker = threading.Thread(target = self.run)
        self.general = ListQueue()
        self.gold = ListQueue()
        self.platinum = ListQueue()
        self.enqueue()

    def get_item(self):
        if self.pos < len(self.items):
            item = self.items[self.pos]
            self.pos += 1
            return item
        else:
            return None
        
    def enqueue(self):  #3번문제
        for item in self.items:
            level = item[0]
            if level == '1':
                self.general.enqueue(item[1])
            elif level == '2':
                self.gold.enqueue(item[1])
            elif level == '3':
                self.platinum.enqueue(item[1])
                
    def dequeue(self):  #3번문제
        if not self.platinum.isEmpty():
            return self.platinum.dequeue()
        elif not self.gold.isEmpty():
            return self.gold.dequeue()
        elif not self.general.isEmpty():
            return self.general.dequeue()
        else:
            return None

    def run(self):
        while True:
            time.sleep(0.2)
            if self.__alive:
                item = self.get_item()
                # item = self.dequeue()
                print("Arrived:", item)
            else:
                break
        
        print("Producer is dying...")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()

class Consumer:
    def __init__(self, items):
        self.__alive = True
        self.items = items
        self.pos = 0
        self.worker = threading.Thread(target=self.run)
        self.general = ListQueue()
        self.gold = ListQueue()
        self.platinum = ListQueue()
        self.enqueue()
        
    def get_item(self):
        if self.pos < len(self.items):
            item = self.items[self.pos]
            self.pos += 1
            return item
        else:
            return None
        
    def enqueue(self):  #3번문제
        for item in self.items:
            level = item[0]
            if level == '1':
                self.general.enqueue(item[1])
            elif level == '2':
                self.gold.enqueue(item[1])
            elif level == '3':
                self.platinum.enqueue(item[1])
                
    def dequeue(self):  #3번문제
        if not self.platinum.isEmpty():
            return self.platinum.dequeue()
        elif not self.gold.isEmpty():
            return self.gold.dequeue()
        elif not self.general.isEmpty():
            return self.general.dequeue()
        else:
            return None

    def run(self):
        while True:
            time.sleep(1)
            if self.__alive:
                item = self.get_item()
                # item = self.dequeue()
                print("Boarding:", item)
            else:
                break
            
        print("Consumer is dying.")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()





if __name__ == "__main__":
    
    customers = []
    with open("customer.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            customer = line.split()
            customers.append(customer)

    # FIFO
    names = []
    for c in customers:
        names.append(c[1])

    producer = Producer(names)
    consumer = Consumer(names)

    # Priority 
    # producer = Producer(customers)
    # consumer = Consumer(customers)    
    producer.start()
    consumer.start()
    time.sleep(10)
    producer.finish()
    consumer.finish()
