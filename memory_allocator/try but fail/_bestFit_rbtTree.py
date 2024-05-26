# 35초 / Arena: 234.84 MB / In-use: 148.05 MB / Utilization: 0.63

# best fit 사용 / red black tree 사용

from sortedcontainers import SortedDict

class MemoryBlock:
    def __init__(self, start, size):
        self.start = start
        self.size = size
        self.is_free = True

class Allocator:
    def __init__(self):
        self.chunk_size = 4096  # 4KB
        self.min_block_size = 32  # 최소 블록 크기 32바이트
        self.arena_size = 0
        self.in_use = 0
        self.arena = []  # 전체 메모리 블록 리스트
        self.free_blocks = SortedDict()  # 빈 블록 리스트 (크기 순으로 정렬)
        self.allocations = {}  # 할당된 메모리 블록 기록

    def print_stats(self):
        total_arena_mb = self.arena_size / (1024 * 1024)
        in_use_mb = self.in_use / (1024 * 1024)
        utilization = self.in_use / self.arena_size if self.arena_size > 0 else 0
        print(f"Arena: {total_arena_mb:.2f} MB")
        print(f"In-use: {in_use_mb:.2f} MB")
        print(f"Utilization: {utilization:.2f}")

    def _remove_free_block(self, block):
        size = block.size
        if size in self.free_blocks:
            blocks = self.free_blocks[size]
            blocks.remove(block)
            if not blocks:
                del self.free_blocks[size]

    def _add_free_block(self, block):
        size = block.size
        if size not in self.free_blocks:
            self.free_blocks[size] = []
        self.free_blocks[size].append(block)

    def malloc(self, id, size):
        size = max((size + 7) // 8 * 8, self.min_block_size)  # 8바이트 단위로 정렬 및 최소 블록 크기 적용
        for free_size in self.free_blocks:
            if free_size >= size:
                block = self.free_blocks[free_size][0]
                self._remove_free_block(block)
                if block.size >= size + self.min_block_size:  # 남은 블록이 최소 블록 크기 이상이어야 분할
                    new_block = MemoryBlock(block.start + size, block.size - size)
                    self.arena.append(new_block)
                    self._add_free_block(new_block)
                block.size = size
                block.is_free = False
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

    def malloc_best_fit(self, id, size):
        size = max((size + 7) // 8 * 8, self.min_block_size)  # 8바이트 단위로 정렬 및 최소 블록 크기 적용
        best_fit_key = None
        for free_size in self.free_blocks:
            if free_size >= size:
                best_fit_key = free_size
                break
        if best_fit_key is not None:
            block = self.free_blocks[best_fit_key][0]
            self._remove_free_block(block)
            if block.size >= size + self.min_block_size:  # 남은 블록이 최소 블록 크기 이상이어야 분할
                new_block = MemoryBlock(block.start + size, block.size - size)
                self.arena.append(new_block)
                self._add_free_block(new_block)
            block.size = size
            block.is_free = False
            self.allocations[id] = block
            self.in_use += size
            return
        self.malloc(id, size)  # 기존 malloc 메서드 호출로 대체

    def free(self, id):
        if id in self.allocations:
            block = self.allocations.pop(id)
            block.is_free = True
            self.in_use -= block.size
            self._add_free_block(block)
            self._merge_free_blocks()

    def _merge_free_blocks(self):
        if not self.free_blocks:
            return
        sorted_blocks = sorted((block for blocks in self.free_blocks.values() for block in blocks), key=lambda x: x.start)
        merged_blocks = []
        current = sorted_blocks[0]
        for block in sorted_blocks[1:]:
            if current.start + current.size == block.start:
                current.size += block.size
            else:
                merged_blocks.append(current)
                current = block
        merged_blocks.append(current)
        self.free_blocks.clear()
        for block in merged_blocks:
            self._add_free_block(block)

if __name__ == "__main__":
    allocator = Allocator()

    with open("./input.txt", "r") as file:
        n = 0
        for line in file:
            req = line.split()
            if req[0] == 'a':
                allocator.malloc_best_fit(int(req[1]), int(req[2]))  # malloc 대신 malloc_best_fit 사용
            elif req[0] == 'f':
                allocator.free(int(req[1]))

            if n % 100 == 0:
                print(n, "...")
            n += 1

    allocator.print_stats()
