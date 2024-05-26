class MemoryBlock:
    def __init__(self, start, size):
        self.start = start
        self.size = size
        self.is_free = True

class Slab:
    def __init__(self, size):
        self.size = size
        self.num_objects_per_page = 4096 // size
        self.pages = []
        self.free_list = []

    def allocate(self):
        if not self.free_list:
            new_page = [None] * self.num_objects_per_page
            self.pages.append(new_page)
            for i in range(self.num_objects_per_page):
                self.free_list.append((len(self.pages) - 1, i))
        page_idx, obj_idx = self.free_list.pop()
        self.pages[page_idx][obj_idx] = True
        return (page_idx, obj_idx)

    def free(self, location):
        page_idx, obj_idx = location
        self.pages[page_idx][obj_idx] = None
        self.free_list.append((page_idx, obj_idx))

class Allocator:
    def __init__(self):
        self.chunk_size = 4096
        self.arena_size = 0
        self.in_use = 0
        self.slabs = [Slab(8 * (2 ** i)) for i in range(8)]  # 8, 16, 32, ..., 2048 bytes
        self.allocations = {}

    def print_stats(self):
        total_arena_mb = self.arena_size / (1024 * 1024)
        in_use_mb = self.in_use / (1024 * 1024)
        utilization = self.in_use / self.arena_size if self.arena_size > 0 else 0
        print(f"Arena: {total_arena_mb:.2f} MB")
        print(f"In-use: {in_use_mb:.2f} MB")
        print(f"Utilization: {utilization:.2f}")

    def malloc(self, id, size):
        size = (size + 7) // 8 * 8  # 8바이트 단위로 정렬
        slab = self._find_slab(size)
        if not slab:
            return
        location = slab.allocate()
        self.allocations[id] = (slab, location)
        self.in_use += slab.size
        self.arena_size += self.chunk_size  # 실제로 메모리 할당 시 증가
        self._update_arena_size()

    def free(self, id):
        if id in self.allocations:
            slab, location = self.allocations.pop(id)
            slab.free(location)
            self.in_use -= slab.size
            self._update_arena_size()

    def _find_slab(self, size):
        for slab in self.slabs:
            if slab.size >= size:
                return slab
        return None

    def _update_arena_size(self):
        self.arena_size = sum(slab.num_objects_per_page * slab.size * len(slab.pages) for slab in self.slabs)

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
