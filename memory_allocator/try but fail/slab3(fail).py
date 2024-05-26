class Allocator:
    def __init__(self):
        self.chunk_size = 4096
        self.arena = []
        self.free_lists = {}
        self.allocations = {}
        self.total_allocated = 0
        self.total_in_use = 0

    def print_stats(self):
        arena_size = len(self.arena) * self.chunk_size / (1024 * 1024)
        in_use_size = self.total_in_use / (1024 * 1024)
        utilization = in_use_size / arena_size if arena_size > 0 else 0
        print(f"# Arena: {arena_size:.2f} MB / In-use: {in_use_size:.2f} MB / Utilization: {utilization:.2f}")

    def malloc(self, id, size):
        block_size = self._get_block_size(size)
        if block_size in self.free_lists and self.free_lists[block_size]:
            start_address, _ = self.free_lists[block_size].pop(0)
        else:
            start_address = self._allocate_new_block(block_size)
        self.allocations[id] = (start_address, size)
        self.total_in_use += size

    def free(self, id):
        if id not in self.allocations:
            raise ValueError("Invalid free request")
        start_address, size = self.allocations.pop(id)
        block_size = self._get_block_size(size)
        self._merge_free_blocks(start_address, block_size)
        self.total_in_use -= size

    def _allocate_new_block(self, size):
        if not self.arena or self.arena[-1] is None:
            new_chunk_start = len(self.arena) * self.chunk_size
            self.arena.extend([None] * (self.chunk_size // size))
            self.total_allocated += self.chunk_size
        else:
            new_chunk_start = self.arena.pop()

        if size not in self.free_lists:
            self.free_lists[size] = []

        allocated_block = (new_chunk_start, size)
        remaining_block = (new_chunk_start + size, self.chunk_size - size)
        self.free_lists[size].append(allocated_block)
        if remaining_block[1] > 0:
            self._merge_free_blocks(remaining_block[0], remaining_block[1])

        return self.free_lists[size].pop(0)[0]

    def _get_block_size(self, size):
        return 2 ** ((size - 1).bit_length())

    def _merge_free_blocks(self, start_address, block_size):
        if block_size not in self.free_lists:
            self.free_lists[block_size] = []
        self.free_lists[block_size].append((start_address, block_size))
        self.free_lists[block_size].sort()

        merged_blocks = []
        current_start, current_size = self.free_lists[block_size][0]
        for next_start, next_size in self.free_lists[block_size][1:]:
            if next_start == current_start + current_size:
                current_size += next_size
            else:
                merged_blocks.append((current_start, current_size))
                current_start, current_size = next_start, next_size
        merged_blocks.append((current_start, current_size))

        self.free_lists[block_size] = []
        for start, size in merged_blocks:
            self._merge_free_blocks(start, size)

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