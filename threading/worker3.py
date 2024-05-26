from listQueue import ListQueue
import threading
import time

class Producer:
    def __init__(self, platinum, gold, general, queue):
        self.__alive = True
        self.platinum = platinum
        self.gold = gold
        self.general = general
        self.pos = 0
        self.pos2 = 0
        self.pos3 = 0
        self.worker = threading.Thread(target = self.run)
        self.queue = queue

    def get_item(self):
        if self.pos < len(self.platinum):
            item = self.platinum[self.pos]
            self.pos += 1
            return item
        elif self.pos2 < len(self.gold):
            item = self.gold[self.pos2]
            self.pos2 += 1
            return item
        elif self.pos3 < len(self.general):
            item = self.general[self.pos3]
            self.pos3 += 1
            return item
        else:
            return None
             

    def run(self):
        while True:
            time.sleep(0.2)
            if self.__alive:
                item = self.get_item()
                print("Arrived:", item)
                self.queue.enqueue(item)
            else:
                break            
            
        
        print("Producer is dying...")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()



class Consumer:
    def __init__(self, queue):
        self.__alive = True
        self.worker = threading.Thread(target=self.run)
        self.queue = queue

    def run(self):
        while True:
            time.sleep(1)
            if self.__alive:
                if not self.queue.isEmpty():
                    print("Boarding:", self.queue.dequeue())
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
    platinum = []
    gold = []
    general = []
    for c in customers:
        if c[0] == '3':
            platinum.append(c[1])
        elif c[0] == '2':
            gold.append(c[1])
        elif c[0] == '1':
            general.append(c[1])
 
    
    queue = ListQueue()
    #producer = Producer(names)
    #consumer = Consumer()

    # Priority 
    producer = Producer(platinum, gold, general, queue)
    consumer = Consumer(queue)    
    producer.start()
    consumer.start()
    time.sleep(10)
    producer.finish()
    consumer.finish()
