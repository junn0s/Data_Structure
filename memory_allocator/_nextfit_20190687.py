# 1분 10초 / Arena: 174 MB / In-use: 162 MB / Utilization: 0.93

# next fit allocator
import time as t
class Allocator:
    def __init__(self):
        self.chunk_size = 16 * 1024                                      # 16KB
        self.arena = []                                                  # 전체 memory space list [base, size]
        self.free_list = []                                              # free block list [base, size]
        self.allocations = {}                                            # allocate된 memory block 추적 dictionary (key : id, value : [base, size])
        self.last_alloc_index = 0                                        # last allocation index

    def print_stats(self):
        total_arena_size = len(self.arena) * self.chunk_size
        in_use = sum(block[1] for block in self.allocations.values())    # 할당된 메모리의 총합 (block[0]은 base, block[1]은 size)
        utilization = in_use / total_arena_size
        print(f"Arena: {total_arena_size // (1024 * 1024)} MB")
        print(f"In-use: {in_use // (1024 * 1024)} MB")
        print(f"Utilization: {utilization:.2f}")

    def _allocate_new_chunk(self):                                       # new chunk 할당
        chunk_base = len(self.arena) * self.chunk_size                   # chunk base는 arena chunk 개수 * chunk size, 즉 새로운 chunk 시작 위치 결정
        self.arena.append([chunk_base, self.chunk_size])                 # arena list에 새 chunk 추가(base, 16kb)
        self.free_list.append([chunk_base, self.chunk_size])             # free list에도 새 chunk 추가(base, 16kb)
       
    def malloc(self, id, size):
        start_index = self.last_alloc_index                              # 할당 시작 index를 마지막으로 할당된 위치 index로 설정
        free_list_len = len(self.free_list)

        for i in range(free_list_len):                                   # free_list 순회
            index = (start_index + i) % free_list_len                    # modulo 연산을 통해 iteration 보장 (free list 끝까지 가면 다시 처음으로)
            base, free_size = self.free_list[index]
            if free_size >= size:                                        # 할당 가능한 상태면 allocations에 할당된 memory block 추가
                self.allocations[id] = [base, size]                      
                if free_size > size:                                     # 사용된 크기만큼 해당 index의 free_list를 update
                    self.free_list[index] = [base + size, free_size - size]
                else:
                    self.free_list.pop(index)                            # 꽉 찬 free list는 삭제
                self.last_alloc_index = index                            # 마지막 할당 위치 update
                return                                                   # 종료

        self._allocate_new_chunk()                                       # 빈 블록 없으면 새 chunk 할당 및 reculsion
        self.malloc(id, size)
        
    def free(self, id):      
        base, size = self.allocations.pop(id)                            # allocations에서 제거 후 free list에 추가
        self.free_list.append([base, size])

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