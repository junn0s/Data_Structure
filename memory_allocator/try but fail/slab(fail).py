# 2초 / Arena: 327.82 MB / In-use: 216.33 MB / Utilization: 0.66

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
        utilization = in_use_size / arena_size
        print(f"Arena: {arena_size:.2f} MB")
        print(f"In-use: {in_use_size:.2f} MB")
        print(f"Utilization: {utilization:.2f}")

    def malloc(self, id, size):
        # Find the smallest power of two greater than or equal to size
        block_size = 8
        while block_size < size:
            block_size *= 2

        if block_size > self.chunk_size:
            raise ValueError("Request size too large")

        # Find a free block or split a larger block
        if block_size in self.free_lists and self.free_lists[block_size]:
            block = self.free_lists[block_size].pop()
        else:
            block = self._allocate_new_block(block_size)

        self.allocations[id] = (block, block_size)
        self.total_in_use += block_size

    def free(self, id):
        if id not in self.allocations:
            raise ValueError("Invalid free request")

        block, size = self.allocations.pop(id)
        self.free_lists[size].append(block)
        self.total_in_use -= size

    def _allocate_new_block(self, size):
        new_chunk = len(self.arena) * self.chunk_size
        self.arena.extend([None] * (self.chunk_size // size))

        # Initialize new chunk as free blocks
        for i in range(0, self.chunk_size, size):
            self.free_lists[size].append(new_chunk + i)

        self.total_allocated += self.chunk_size
        return self.free_lists[size].pop()

if __name__ == "__main__":
    allocator = Allocator()
    
    with open ("./input.txt", "r") as file:
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


'''
초기화 (__init__)
chunk_size를 4096 바이트로 설정.
arena는 전체 메모리 공간을 저장하는 리스트.
free_lists는 8, 16, 32, ..., 4096 바이트 크기의 블록을 관리하는 자유 목록 딕셔너리.
allocations는 각 할당된 메모리의 ID와 (시작 주소, 크기)를 저장.
total_allocated는 할당된 총 메모리 크기.
total_in_use는 현재 사용 중인 메모리 크기.

malloc 함수
요청된 크기 이상의 가장 작은 2의 거듭제곱 크기의 블록을 찾음.
해당 크기의 자유 목록에서 블록을 찾고 없으면 새로운 블록을 할당.
블록을 할당하고 allocations에 저장.

free 함수
지정된 ID의 메모리를 해제하고 자유 목록에 추가.

_allocate_new_block 함수
새로운 4KB 청크를 할당하고 이를 지정된 크기의 블록으로 나누어 자유 목록에 추가.
새로운 블록을 반환.

print_stats 함수
전체 메모리 크기, 사용 중인 메모리 크기, 메모리 사용률을 출력.
'''