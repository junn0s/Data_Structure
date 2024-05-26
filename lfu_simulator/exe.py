class MinHeap:
    def __init__(self, *args):
        if len(args) != 0:
            self.__A = args[0]
        else:
            self.__A = []

    def insert(self, x):
        self.__A.append(x)
        self.__percolateUp(len(self.__A) - 1)

    def __percolateUp(self, i: int):
        parent = (i - 1) // 2
        if i > 0 and self.__A[i][1] < self.__A[parent][1]:
            self.__A[i], self.__A[parent] = self.__A[parent], self.__A[i]
            self.__percolateUp(parent)

    def deleteMin(self):
        if not self.isEmpty():
            min_val = self.__A[0]
            self.__A[0] = self.__A.pop()
            self.__percolateDown(0)
            return min_val
        else:
            return None
        
    def delete(self, x):
        if x in self.__A:
            index = self.__A.index(x)
            self.__A[index] = self.__A[-1]
            self.__A.pop()

    def __percolateDown(self, i: int):
        child = 2 * i + 1
        right = 2 * i + 2
        if child <= len(self.__A) - 1:
            if right <= len(self.__A) - 1 and self.__A[child][1] > self.__A[right][1]:
                child = right
            if self.__A[i][1] > self.__A[child][1]:
                self.__A[i], self.__A[child] = self.__A[child], self.__A[i]
                self.__percolateDown(child)

    def min(self):
        return self.__A[0]

    def buildHeap(self):
        for i in range((len(self.__A) - 2) // 2, -1, -1):
            self.__percolateDown(i)

    def isEmpty(self) -> bool:
        return len(self.__A) == 0

    def clean(self):
        self.__A = []

    def size(self) -> int:
        return len(self.__A)

    def heapPrint(self):
        depth = 0
        count = 0
        print("===========================")
        while count < len(self.__A):
            for i in range(2 ** depth):
                if count < len(self.__A):
                    print(self.__A[count], end=" ")
                count += 1
            print()
            depth += 1
        print()
    
    
    

def lfu_sim(cache_slots):
    cache_hit = 0
    tot_cnt = 0
    cache = MinHeap()
    
    data_file = open("linkbench.trc")
    
    lpn_freq_dict = {}
    
    for line in data_file.readlines():
        lpn = line.split()[0]
        tot_cnt += 1
        
        if lpn in lpn_freq_dict:
            cache.delete(lpn_freq_dict[lpn])
            lpn_freq_dict[lpn][1] += 1
            cache.insert(lpn_freq_dict[lpn])
            cache_hit += 1
        else:
            if cache.size() > cache_slots:
                evicted = cache.deleteMin()
                if evicted[0] in lpn_freq_dict:
                    del lpn_freq_dict[evicted[0]]

            lpn_freq_dict[lpn] = [lpn, 1]
            cache.insert(lpn_freq_dict[lpn])
            

    
    print("cache_slot =", cache_slots, "cache_hit =", cache_hit, "hit ratio =", cache_hit / tot_cnt)


if __name__ == "__main__":
    for cache_slots in range(100, 1000, 100):
        lfu_sim(cache_slots)