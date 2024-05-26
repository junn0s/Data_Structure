# 1분 4초 / Arena: 235.05 MB / In-use: 148.18 MB / Utilization: 0.63

class MemoryBlock:
    def __init__(self, start, size):
        self.start = start
        self.size = size
        self.is_free = True

class Allocator:
    def __init__(self):
        self.chunk_size = 4096  # 4KB
        self.arena_size = 0
        self.in_use = 0
        self.arena = []  # 전체 메모리 블록 리스트
        self.free_blocks = []  # 빈 블록 리스트 (크기 순으로 정렬)
        self.allocations = {}  # 할당된 메모리 블록 기록

    def print_stats(self):
        total_arena_mb = self.arena_size / (1024 * 1024)
        in_use_mb = self.in_use / (1024 * 1024)
        utilization = self.in_use / self.arena_size if self.arena_size > 0 else 0
        print(f"Arena: {total_arena_mb:.2f} MB")
        print(f"In-use: {in_use_mb:.2f} MB")
        print(f"Utilization: {utilization:.2f}")

    def malloc(self, id, size):
        size = (size + 7) // 8 * 8  # 8바이트 단위로 정렬
        for block in self.free_blocks:
            if block.size >= size:
                if block.size > size:
                    new_block = MemoryBlock(block.start + size, block.size - size)
                    self.arena.append(new_block)
                    self.free_blocks.append(new_block)
                block.size = size
                block.is_free = False
                self.free_blocks.remove(block)
                self.allocations[id] = block
                self.in_use += size
                return
        start = self.arena_size
        new_block = MemoryBlock(start, max(self.chunk_size, size))
        self.arena.append(new_block)
        self.arena_size += new_block.size
        new_block.is_free = False
        self.allocations[id] = new_block
        self.in_use += size

    def free(self, id):
        if id in self.allocations:
            block = self.allocations.pop(id)
            block.is_free = True
            self.in_use -= block.size
            self.free_blocks.append(block)
            self._merge_free_blocks()

    def _merge_free_blocks(self):
        self.free_blocks.sort(key=lambda x: x.start)
        merged_blocks = []
        current = self.free_blocks[0]
        for block in self.free_blocks[1:]:
            if current.start + current.size == block.start:
                current.size += block.size
            else:
                merged_blocks.append(current)
                current = block
        merged_blocks.append(current)
        self.free_blocks = merged_blocks

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
