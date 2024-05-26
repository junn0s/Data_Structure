class MinHeap:
    def __init__(self, *args):
        if len(args) != 0:
            self.__A = args[0]
        else:
            self.__A = []

    def insert(self, x):
        self.__A.append(x)
        self.__percolateUp(len(self.__A) - 1)
    
    def insert_count(self, x):
        for i in range(len(self.__A)):
            if self.__A[i][0] == x[0]:
                self.__A[i][1] += 0              
                break    

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