class ListNode:
    def __init__(self, newItem=None):
        self.item = newItem
        self.next = None

class LinkedListBasic:
    def __init__(self):
        self.head = None
        self.tail = None  
        self._size = 0
    
    def append(self, newItem):
        new_node = ListNode(newItem)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
    
    def remove(self, newItem):
        current = self.head
        prev = None
        while current:
            if current.item == newItem:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                if current == self.tail:  
                    self.tail = prev
                self._size -= 1
                return
            prev = current
            current = current.next
    
    def __contains__(self, newItem):
        current = self.head
        while current:
            if current.item == newItem:
                return True
            current = current.next
        return False
    
    def __len__(self):
        return self._size


class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache = LinkedListBasic()
        self.cache_hit = 0
        self.tot_cnt = 1
    
    def do_sim(self, page):
        if page in self.cache: 
            self.cache.remove(page)
            self.cache.append(page)
            self.cache_hit += 1
        else:
            if len(self.cache) >= self.cache_slots:
                self.cache.remove(self.cache.head.item)
            self.cache.append(page)
        
        self.tot_cnt += 1
        
    def print_stats(self):
        print("cache_slot =", self.cache_slots, "cache_hit =", self.cache_hit, "hit ratio =", self.cache_hit / self.tot_cnt)

if __name__ == "__main__":
    data_file = open("./linkbench.trc")
    lines = data_file.readlines()
    
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)
        cache_sim.print_stats()
