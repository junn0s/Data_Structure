'''A항공사는 고객 등급을 일반, 골드, 플래티넘 회원으로 나누어 관리한다. 
비행기 탑승 시 등급이 높은 순서대로 (일반 < 골드 < 플래티넘) 탑승하고, 
동일 등급 내에서는 도착한 순서대로 탑승한다. 
고객이 도착했을 때 위와 같은 순서로 탑승을 하도록 하는 프로그램을 만드시오.''' 

from listqueue2 import ListQueue

class BoardingQueue:
    def __init__(self):
        self.general = ListQueue()
        self.gold = ListQueue()
        self.platinum = ListQueue()

    def enqueue(self, level, passenger):
        if level == 'general':
            self.general.enqueue(passenger)
        elif level == 'gold':
            self.gold.enqueue(passenger)
        elif level == 'platinum':
            self.platinum.enqueue(passenger)

    def dequeue(self):
        if self.platinum is not None:
            return self.platinum.dequeue()
        elif self.gold is not None:
            return self.gold.dequeue()
        elif self.general is not None:
            return self.general.dequeue()
        else:
            return None

def main():
    boarding_queue = BoardingQueue()

    while True:
        print("\nSelect the passenger's level:")
        print("1. General")
        print("2. Gold")
        print("3. Platinum")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter passenger's name: ")
            boarding_queue.enqueue('general', name)
        elif choice == '2':
            name = input("Enter passenger's name: ")
            boarding_queue.enqueue('gold', name)
        elif choice == '3':
            name = input("Enter passenger's name: ")
            boarding_queue.enqueue('platinum', name)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

    print("\nBoarding Order:")
    while True:
        passenger = boarding_queue.dequeue()
        if passenger:
            print(passenger, "boards the plane.")
        else:
            break

if __name__ == "__main__":
    main()