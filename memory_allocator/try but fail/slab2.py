class Slab:
    def __init__(self, size, chunk_size=16 * 1024):
        self.size = size
        self.num_objects_per_page = chunk_size // size
        self.chunk_size = chunk_size
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

    def used_memory(self):
        return len(self.pages) * self.num_objects_per_page * self.size - len(self.free_list) * self.size

    def total_memory(self):
        return len(self.pages) * self.num_objects_per_page * self.size


class Allocator:
    def __init__(self):
        self.chunk_size = 16 * 1024
        self.slabs = [Slab(8 * (2 ** i), self.chunk_size) for i in range(8)]  # 8, 16, 32, ..., 1024 bytes
        self.large_allocations = {}
        self.allocations = {}

    def print_stats(self):
        total_arena_kb = sum(slab.total_memory() for slab in self.slabs) / 1024
        total_arena_kb += sum(size for _, size in self.large_allocations.values()) / 1024
        in_use_kb = sum(slab.used_memory() for slab in self.slabs) / 1024
        in_use_kb += sum(size for _, size in self.large_allocations.values()) / 1024
        utilization = in_use_kb / total_arena_kb if total_arena_kb > 0 else 0
        print(f"Arena: {total_arena_kb:.2f} KB")
        print(f"In-use: {in_use_kb:.2f} KB")
        print(f"Utilization: {utilization:.2f}")

    def malloc(self, id, size):
        size = (size + 7) // 8 * 8  # 8바이트 단위로 정렬
        if size > 1024:
            # Large allocations (greater than 1024 bytes)
            num_chunks = (size + self.chunk_size - 1) // self.chunk_size
            new_page = [None] * num_chunks
            self.large_allocations[id] = (new_page, size)
            self.allocations[id] = ("large", id)
        else:
            slab = self._find_slab(size)
            if slab:
                location = slab.allocate()
                self.allocations[id] = (slab, location)

    def free(self, id):
        if id in self.allocations:
            slab_or_type, location = self.allocations.pop(id)
            if slab_or_type == "large":
                self.large_allocations.pop(location)
            else:
                slab_or_type.free(location)

    def _find_slab(self, size):
        for slab in self.slabs:
            if slab.size >= size:
                return slab
        return None

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