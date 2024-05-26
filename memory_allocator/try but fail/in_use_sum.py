# 162.24 MB 가 나와야 함(allocate, free를 전부 할 시)

if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        sum = 0
        n = 0
        f_count = 0
        a_count = 0
        a_values = {}  # 'a' 명령어의 req[1] 값과 크기를 저장할 딕셔너리

        for line in file:
            req = line.split()
            if req[0] == 'a':
                a_count += 1
                a_values[req[1]] = int(req[2])  # req[1]을 키로, 크기를 값으로 저장
                sum += int(req[2])
            elif req[0] == 'f':
                f_count += 1
                if req[1] in a_values:  # req[1]이 a_values에 있는 경우
                    sum -= a_values[req[1]]  # 저장된 크기 값을 sum에서 뺌
                    del a_values[req[1]]  # 사용한 값은 딕셔너리에서 제거

            if n % 100 == 0:
                print(n, "...")
            n += 1

        print("sum : ", sum)
        print("f_count : ", f_count)
        print("a_count : ", a_count)