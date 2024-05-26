from listqueue2 import ListQueue

def isPalindrome(A) -> bool:
    queue = ListQueue()
    if '$' in A:
        for i in range(len(A)):
            queue.enqueue(A[i])
        reverse_queue = queue.reverse()
        while (not queue.isEmpty()) and queue.dequeue() == reverse_queue.dequeue():
            {}
        if queue.isEmpty():
            return True
        else:
            return False
    else :
        return False

if __name__ == "__main__":
        str = 'abcdeee$eeedcba'
        t = isPalindrome(str)
        print(str, " is Palindrome? : ", t)