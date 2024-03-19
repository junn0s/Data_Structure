def __contains__(self, newItem):
    current = self.head
    prev = None
    while current:
        if current.item == newItem:
            if prev:
                prev.next = current.next
                if current == self.tail:
                    self.tail = prev
                self._size -= 1
            else:
                self.head = current.next
                if current == self.tail:
                    self.tail = None if self.head is None else prev
                self._size -= 1
            return True  
        prev = current
        current = current.next
    return False

def do_sim(self, page):
    if page in self.cache: 
        self.cache.append(page)
        self.cache_hit += 1
    else:
        if len(self.cache) >= self.cache_slots:
            self.cache.remove(self.cache.head.item)
        self.cache.append(page)
    
    self.tot_cnt += 1