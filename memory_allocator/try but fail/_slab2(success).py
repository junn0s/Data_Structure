# 13.8초 / Arena: 285.18 MB / In-use: 162.19 MB / Utilization: 0.57

# slab

class Allocator:
    def __init__(self):
        self.chunk_size = 4096
        self.arena = []
        self.free_lists = {2**i: [] for i in range(3, 13)}  # 8, 16, 32, ..., 4096
        self.allocations = {}  # id: (start_address, size)
        self.total_allocated = 0
        self.total_in_use = 0

    def print_stats(self):
        arena_size = len(self.arena) * self.chunk_size / (1024 * 1024)
        in_use_size = self.total_in_use / (1024 * 1024)
        utilization = in_use_size / arena_size if arena_size > 0 else 0
        print(f"Arena: {arena_size:.2f} MB")
        print(f"In-use: {in_use_size:.2f} MB")
        print(f"Utilization: {utilization:.2f}")

    def malloc(self, id, size):
        block_size = self._get_block_size(size)

        if block_size > self.chunk_size:
            raise ValueError("Request size too large")

        if block_size in self.free_lists and self.free_lists[block_size]:
            block = self.free_lists[block_size].pop()
        else:
            block = self._allocate_new_block(block_size)

        self.allocations[id] = (block, size)  # Store the actual requested size
        self.total_in_use += size  # Use the actual requested size for in-use calculation

    def free(self, id):
        if id not in self.allocations:
            raise ValueError("Invalid free request")

        block, size = self.allocations.pop(id)
        block_size = self._get_block_size(size)
        self.free_lists[block_size].append(block)
        self.total_in_use -= size  # Use the actual requested size for in-use calculation

        self._merge_free_blocks()

    def _allocate_new_block(self, size):
        new_chunk = len(self.arena) * self.chunk_size
        self.arena.extend([None] * (self.chunk_size // size))

        for i in range(0, self.chunk_size, size):
            self.free_lists[size].append(new_chunk + i)

        self.total_allocated += self.chunk_size
        return self.free_lists[size].pop()

    def _get_block_size(self, size):
        block_size = 8
        while block_size < size:
            block_size *= 2
        return block_size

    def _merge_free_blocks(self):
        for size in sorted(self.free_lists.keys(), reverse=True):
            free_blocks = sorted(self.free_lists[size])
            merged = []
            while free_blocks:
                block = free_blocks.pop(0)
                while free_blocks and free_blocks[0] == block + size:
                    block = free_blocks.pop(0)
                    size *= 2
                merged.append(block)
            self.free_lists[size] = merged

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

