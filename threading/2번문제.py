from listqueue2 import ListQueue

class Stack :
    def __init__(self) :
        self.origin_q = ListQueue()
        self.assis_q = ListQueue()
        self.length = 0
        
    def push(self, x) :
        self.origin_q.enqueue(x)
        self.length += 1
        
    def pop(self) :
        for i in range(self.length-1) :
            temp = self.origin_q.dequeue()
            self.assis_q.enqueue(temp)
        self.origin_q.dequeue()
        self.length -= 1
        for j in range(self.length) :
            temp = self.assis_q.dequeue()
            self.origin_q.enqueue(temp)

    def printStack(self):
        self.origin_q.printQueue()


def main() :
    stack = Stack()
    str = 'ABCDE'
    for i in range(len(str)) :
        stack.push(str[i])
    stack.printStack()
    
    stack.pop()
    stack.printStack()
    

if __name__ == '__main__':
    main()