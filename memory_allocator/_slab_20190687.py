# 0.82초 / Arena: 216.35 MB / In-use: 162 MB / Utilization: 0.75

# slab allocator
import time as t
class Allocator:
    def __init__(self):
        self.chunk_size = 4096                                            # 4KB
        self.arena = []                                                   # 전체 memory space list (arena의 길이가 chunk 할당 횟수를 나타냄)
        self.free_lists = {2**i: [] for i in range(3, 13)}                # free block dictionary   8, 16, 32, ..., 4096
        self.allocations = {}                                             # id: (start_address, size)                                    
        self.total_in_use = 0                                             # 실제 사용중 메모리 크기 추적

    def print_stats(self):
        arena_size = len(self.arena) * self.chunk_size / (1024 * 1024)
        in_use_size = self.total_in_use / (1024 * 1024)
        utilization = in_use_size / arena_size
        print(f"Arena: {arena_size:.2f} MB")
        print(f"In-use: {in_use_size:.2f} MB")
        print(f"Utilization: {utilization:.2f}")
        
    def _allocate_new_block(self, size):
        self.arena.append('0')                                            # arena에 새 청크 추가(할당 횟수 추가)
        new_chunk = len(self.arena) * self.chunk_size                     # 새 청크 시작 주소 계산
                                                      
        for i in range(0, self.chunk_size, size):                         # 해당 size의 free list에 추가(ex size=1024면 4개 추가)
            self.free_lists[size].append(new_chunk + i)                   # 추가 내용은 주소값임
        return self.free_lists[size].pop()                                # 해당 free list 맨앞 블록 반환

    def malloc(self, id, size):
        block_size = self._get_block_size(size)                           # 요청된 크기보다 크거나 같은 가장 작은 2의 제곱수를 찾음

        if self.free_lists[block_size]:                                   # free_lists에서 블록을 찾아 꺼냄
            block = self.free_lists[block_size].pop()
        else:
            block = self._allocate_new_block(block_size)                  # 없다면 새 블록 할당

        self.allocations[id] = (block, size)                              # allocations에 할당된 memory block 추가
        self.total_in_use += size                                         # total use에 size 추가
        
    def free(self, id):
        block, size = self.allocations.pop(id)                            # allocations에서 해당 블록 정보 제거 및 return
        self.free_lists[self._get_block_size(size)].append(block)         # 해당 블록을 해당 free_lists에 추가 (블록의 internal fragmentation은 무시)
        self.total_in_use -= size                                         # tatal use에서 해당 size 제거
        
    def _get_block_size(self, size):                                      # 요청된 크기보다 크거나 같은 가장 작은 2의 제곱수 반환
        block_size = 8   
        while block_size < size:
            block_size *= 2
        return block_size

if __name__ == "__main__":
    allocator = Allocator()
    start = t.time()
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
    end = t.time()
    allocator.print_stats()
    print("time = %.2f second" % (end - start))