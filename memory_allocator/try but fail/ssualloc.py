class MemoryBlock:
    def __init__(self, size, is_free=True):
        self.size = size
        self.is_free = is_free
        self.next = None
        self.prev = None

class SSU_Alloc:
    def __init__(self):
        self.chunk_size = 4096
        self.arena = 0
        self.in_use = 0
        self.head = None
        self.tail = None

    def print_stats(self):
        print(f"Arena: {self.arena // (1024 * 1024)} MB")
        print(f"In-use: {self.in_use // (1024 * 1024)} MB")
        print(f"Utilization: {self.in_use / self.arena:.2f}")

    def malloc(self, id, size):
        size = (size + 7) // 8 * 8  # 8의 배수로 반올림
        block = self.head
        while block:
            if block.is_free and block.size >= size:
                if block.size == size:
                    block.is_free = False
                else:
                    new_block = MemoryBlock(block.size - size, True)
                    new_block.next = block.next
                    if block.next:
                        block.next.prev = new_block
                    else:
                        self.tail = new_block
                    block.next = new_block
                    new_block.prev = block
                    block.size = size
                    block.is_free = False
                self.in_use += size
                return
            block = block.next

        # 새로운 청크를 할당받아야 함
        new_chunk_size = max(self.chunk_size, size)
        new_block = MemoryBlock(new_chunk_size, False)
        self.arena += new_chunk_size
        if not self.head:
            self.head = self.tail = new_block
        else:
            self.tail.next = new_block
            new_block.prev = self.tail
            self.tail = new_block
        self.in_use += size

    def free(self, id):
        block = self.head
        while block:
            if not block.is_free:
                block.is_free = True
                self.in_use -= block.size
                # 앞뒤 블록이 모두 free라면 합치기
                if block.prev and block.prev.is_free:
                    block.prev.size += block.size
                    block.prev.next = block.next
                    if block.next:
                        block.next.prev = block.prev
                    else:
                        self.tail = block.prev
                    block = block.prev
                if block.next and block.next.is_free:
                    block.size += block.next.size
                    block.next = block.next.next
                    if block.next:
                        block.next.prev = block
                    else:
                        self.tail = block
                return
            block = block.next

if __name__ == "__main__":
    allocator = SSU_Alloc()
    with open("./input.txt", "r") as file:
        n = 0
        for line in file:
            req = line.split()
            if req[0] == 'a':
                allocator.malloc(int(req[1]), int(req[2]))
            elif req[0] == 'f':
                allocator.free(int(req[1]))
            if n % 100 == 0:
                print(n, "...")
            n += 1
    allocator.print_stats()