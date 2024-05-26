class ListNode:
    def __init__(self, newItem, nextNode:'ListNode'):
        self.item = newItem
        self.next = nextNode

class LinkedListBasic:
    def __init__(self):
        self.__head = ListNode('dummy', None)
        self.__numItems = 0
        
    def append(self, newItem):
        prev = self.__getNode(self.__numItems - 1)
        newNode = ListNode(newItem, prev.next)
        prev.next = newNode
        self.__numItems += 1
    
    def pop(self, i:int):
        if (i >= 0 and i <= self.__numItems - 1):
            prev = self.__getNode(i - 1)
            curr = prev.next
            prev.next = curr.next
            retItem = curr.item
            self.__numItems -= 1
            return retItem
        else :
            return None
        
    def remove(self, x):
        (prev, curr) = self.__findNode(x)
        if curr != None:
            prev.next = curr.next
            self.__numItems -= 1
            return x
        else :
            return None
        
    def __findNode(self, x) -> (ListNode, ListNode): # type: ignore
        prev = self.__head
        curr = prev.next
        while curr != None:
            if curr.item == x:
                return(prev, curr)
            else:
                prev = curr
                curr = curr.next
        return (None, None)
    
    def __getNode(self, i:int) -> ListNode:
        curr = self.__head
        for index in range(i+1):
            curr = curr.next
        return curr
