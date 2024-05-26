# 47초 / Arena: 234.84 MB / In-use: 148.05 MB / Utilization: 0.63

# best fit 사용

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

    def malloc_best_fit(self, id, size):
        size = (size + 7) // 8 * 8  # 8바이트 단위로 정렬
        best_fit = None
        for block in self.free_blocks:
            if block.size >= size and (best_fit is None or block.size < best_fit.size):
                best_fit = block
        if best_fit:
            if best_fit.size > size:
                new_block = MemoryBlock(best_fit.start + size, best_fit.size - size)
                self.arena.append(new_block)
                self.free_blocks.append(new_block)
            best_fit.size = size
            best_fit.is_free = False
            self.free_blocks.remove(best_fit)
            self.allocations[id] = best_fit
            self.in_use += size
            return
        # 새로운 Chunk 할당이 필요한 경우 처리
        self.malloc(id, size)  # 기존 malloc 메서드 호출로 대체

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
                allocator.malloc_best_fit(int(req[1]), int(req[2]))  # malloc 대신 malloc_best_fit 사용
            elif req[0] == 'f':
                allocator.free(int(req[1]))

            if n % 100 == 0:
                print(n, "...")
            n += 1

    allocator.print_stats()


'''
Free Block의 빠른 검색을 위한 자료구조 개선: 
현재 free_blocks 리스트는 매 할당 요청마다 전체를 순회하여 적절한 블록을 찾습니다. 
이를 더 효율적으로 관리하기 위해, 예를 들어 AVL 트리나 레드-블랙 트리와 같은 균형 이진 검색 트리를 사용하면 
검색, 삽입, 삭제가 모두 평균적으로 O(log n) 시간에 이루어질 수 있어 효율을 높일 수 있습니다.

메모리 블록 합치기 최적화:
_merge_free_blocks 메서드는 빈 블록들을 순회하면서 인접한 빈 블록을 합치는 역할을 합니다. 
현재 구현에서는 모든 빈 블록을 매번 정렬하고 순회하는 방식인데, 이를 더 효율적으로 관리하기 위해 합칠 수 있는 블록을 빠르게 찾을 수 있는 자료구조
(예: 연결 리스트와 해시 테이블의 조합)를 사용할 수 있습니다.

메모리 할당 크기 조정: 
malloc 메서드에서 새로운 메모리 블록을 할당할 때, 요청된 크기와 상관없이 고정된 chunk_size (4KB) 또는 요청된 크기 중 더 큰 값으로 할당합니다. 
이는 메모리 낭비를 초래할 수 있습니다. 메모리 할당 시 요청된 크기에 더 적합하게 동적으로 chunk_size를 조정하는 방법을 고려해볼 수 있습니다.

메모리 할당 전략 변경: 
malloc_best_fit 방식은 메모리 파편화를 줄이는 데 도움이 되지만, 시간 복잡도 문제를 야기할 수 있습니다. 
대안으로, malloc에서 사용하는 방식을 유지하되, 메모리 할당이 실패할 경우에만 malloc_best_fit을 시도하는 등의 
하이브리드 접근 방식을 고려해 볼 수 있습니다.
'''