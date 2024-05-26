from listqueue2 import ListQueue

def isPalindrome(A) -> bool:
    queue = ListQueue()
    if '$' in A:
        for i in range(len(A)):
            if (A[i] == '$'): break
            else: queue.enqueue(A[i])
                
        for j in range(len(A)-1, i, -1):
            if queue.isEmpty() : return False
            if (queue.dequeue() != A[j]): return False
        if (queue.isEmpty()) : return True
        else : return False
    else : return False

if __name__ == "__main__":
        str = 'abds$sdba'
        t = isPalindrome(str)
        print(str, " is Palindrome? : ", t)