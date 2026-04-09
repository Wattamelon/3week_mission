"""
함수 모음 파일
"""
import time

def parse_row(input_value, n):
    input_value = input_value.split()

    if len(input_value) != n:
        print(f"{n}개의 숫자만 입력 가능합니다.")
        return None

    tmp = []
    for num in input_value:
        if (num == "1" or num == "0"):
            tmp.append(int(num))
        else:
            print("0 또는 1만 입력 가능합니다.")
            return None

    return tmp

def read_matrix(n):
    matrix = []

    for i in range(n):
        while True:
            print(f"{i+1}번째 줄: {n}개의 숫자를 입력해주세요.")
            row = input()

            parsed = parse_row(row, n)

            if parsed is not None:
                matrix.append(parsed)
                break

    return matrix

def mac(pattern, filt) : 
    score = 0
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filt[i][j]
    return score
    

def judge(score_a, score_b, epsilon=1e-9):
    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"

def measure_time(pattern, filter_a, filter_b, repeat=10):
    total_time = 0
    for i in range(repeat):
        start = time.time()
        mac(pattern , filter_a)
        mac(pattern , filter_b)
        end = time.time()
        total_time += (end-start)
        
    return (total_time/repeat) * 1000