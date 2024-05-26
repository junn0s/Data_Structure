class Allocator:
    def __init__(self):
        self.chunk_size = 4096
        self.arena = []
        self.free_lists = {2**i: [] for i in range(3, 13)}  # 8, 16, 32, ..., 4096
        self.allocations = {}  # id: (start_address, size)
        self.total_allocated = 0
        self.total_in_use = 0

    def print_stats(self):
        arena_size = self.total_allocated / (1024 * 1024)
        in_use_size = self.total_in_use / (1024 * 1024)
        utilization = self.total_in_use / (self.total_allocated + 1e-9)
        print(f"Arena: {arena_size:.2f} MB")
        print(f"In-use: {in_use_size:.2f} MB")
        print(f"Utilization: {utilization:.2f}")

    def malloc(self, id, size):
        block_size = 8
        while block_size < size:
            block_size *= 2

        if block_size > self.chunk_size:
            raise ValueError("Request size too large")

        block = self._find_free_block(block_size)
        self.allocations[id] = (block, block_size)
        self.total_in_use += block_size

    def free(self, id):
        if id not in self.allocations:
            raise ValueError("Invalid free request")

        block, size = self.allocations.pop(id)
        self._add_to_free_list(block, size)
        self.total_in_use -= size

    def _find_free_block(self, size):
        current_size = size
        while current_size <= self.chunk_size:
            if self.free_lists[current_size]:
                return self.free_lists[current_size].pop()
            current_size *= 2

        new_chunk = len(self.arena) * self.chunk_size
        self.arena.append(new_chunk)
        self.total_allocated += self.chunk_size
        self._add_to_free_list(new_chunk, self.chunk_size)
        return self._find_free_block(size)

    def _add_to_free_list(self, address, size):
        while size <= self.chunk_size:
            buddy_address = self._find_buddy(address, size)
            buddy_list = self.free_lists[size]
            if buddy_address in buddy_list:
                buddy_list.remove(buddy_address)
                address = min(address, buddy_address)
                size *= 2
            else:
                self.free_lists[size].append(address)
                break

    def _find_buddy(self, address, size):
        return address ^ size

if __name__ == "__main__":
    allocator = Allocator()
    
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
