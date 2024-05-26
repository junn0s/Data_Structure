# 3분 15초 / Arena: 163 MB / In-use: 162 MB / Utilization: 0.99

# first fit

class Allocator:
    def __init__(self):
        self.chunk_size = 16 * 1024  # 16KB
        self.max_request_size = 4096  # 4KB
        self.arena = []
        self.allocations = {}
        self.free_list = []
        
        # 여기서 Allocator 클래스는 메모리 할당을 관리합니다. 
        # chunk_size는 각 메모리 청크의 크기를 나타내며
        # max_request_size는 각 요청에 대한 최대 크기를 제한합니다. 
        # arena은 메모리 공간을 나타내고
        # allocations은 할당된 메모리 블록을 추적합니다. 
        # free_list는 사용 가능한 빈 메모리 블록의 목록을 유지합니다.

    def print_stats(self):
        total_arena_size = len(self.arena) * self.chunk_size
        in_use = sum(block[1] for block in self.allocations.values())
        utilization = in_use / total_arena_size
        print(f"Arena: {total_arena_size // (1024 * 1024)} MB")
        print(f"In-use: {in_use // (1024 * 1024)} MB")
        print(f"Utilization: {utilization:.2f}")
        
        # arena 크기 = 길이 * 각 청크 크기
        # in use = 할당된 메모리의 합

    def _allocate_new_chunk(self):
        chunk_base = len(self.arena) * self.chunk_size
        self.arena.append([chunk_base, self.chunk_size])
        self.free_list.append([chunk_base, self.chunk_size])
        
        # chunk base는 arena 청크 개수 * 청크 크기, 즉 새로운 청크 시작 위치 결정
        # arena list에 새 청크 추가(base, 16kb)
        # free list에도 새 청크 추가(base, 16kb)

    def malloc(self, id, size):
        if size > self.max_request_size:
            raise ValueError(f"Requested size {size} exceeds maximum request size {self.max_request_size}")

        for i, (base, free_size) in enumerate(self.free_list):
            if free_size >= size:
                self.allocations[id] = [base, size]
                if free_size > size:
                    self.free_list[i] = [base + size, free_size - size]
                else:
                    self.free_list.pop(i)
                return
            
        # 요청 크기가 최대 크기(4kb)를 초과하면 error 발생
        # free list를 순회하면서 요청 크기 공간을 찾음(first-fit starategy 사용)
        # 빈 메모리 크기가 더 크거나 같다면 allocation에 새로 할당된 메모리 정보 추가
        # 빈 메모리 크기가 더 크면 요청 크기를 뺀 만큼 새로운 base와 size로 free list 수정
        # 빈 메모리 크기와 요청 크기가 같다면 해당 인덱스의 free list 삭제
        # return(종료)
        
        self._allocate_new_chunk()
        self.malloc(id, size)
        
        # 공간이 부족하면 새 청크 할당
        # malloc 함수 다시 실행

    def free(self, id):
        if id not in self.allocations:
            print(f"Warning: Attempt to free non-existent allocation with id {id}")
            return        
        base, size = self.allocations.pop(id)
        self.free_list.append([base, size])
        self.free_list.sort()
        
        # id를 사용해서 free할 메모리의 base와 size를 가져옴
        # free list에 해제된 메모리 추가
        # free list 정렬을 통해 연속적으로 정렬        
        
        merged_free_list = []
        current_base, current_size = self.free_list[0]
        for base, size in self.free_list[1:]:
            if current_base + current_size == base:
                current_size += size
            else:
                merged_free_list.append([current_base, current_size])
                current_base, current_size = base, size
        merged_free_list.append([current_base, current_size])
        self.free_list = merged_free_list
        
        # 병합을 위한 free list 하나 생성
        # 첫 번째 free 블록의 base와 size를 병합 list의 새 base와 size로 지정
        # 다음 free 블록이 완전히 비어있다면(인접하다면) base 유지한 채 size를 합침
        # 인접하지 않다면 현재까지 병합한 블록을 병합list에 추가, 다음 블록이 새 base와 size가 됨
        # 남은 base와 size를 병합 list에 추가, 병합 list가 새 free list가 됨

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