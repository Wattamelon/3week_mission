"""
실제 흐름 담당
"""
import json
from core import read_matrix, mac, judge , measure_time

def run_mode1():
    print("=== Mode 1: 사용자 입력 (3x3) ===")

    print("[필터 A 입력]")
    filter_a = read_matrix(3)

    print("[필터 B 입력]")
    filter_b = read_matrix(3)

    print("[패턴 입력]")
    pattern = read_matrix(3)

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    result = judge(score_a, score_b)
    
    time_esti = measure_time(pattern , filter_a , filter_b)

    print("\n[결과]")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"판정: {result}")
    print(f"소요시간: {time_esti:.6f} ms")

def run_mode2():
    data = load_json_data()

    filters = data["filters"]
    patterns = data["patterns"]

    total_count = 0
    pass_count = 0
    fail_count = 0
    fail_cases = []

    print("=== Mode 2: data.json 분석 ===")
    print("[1] 필터 로드")

    for filter_key in filters:
        print(f"✓ {filter_key} 필터 로드 완료 (Cross, X)")

    print("\n[2] 패턴 분석")

    for pattern_name, pattern_info in patterns.items():
        total_count += 1 # 총 테스트 갯수 카운트

        print(f"\n--- {pattern_name} ---")

        # 예: size_13_2 -> size_num = 13, filter_key = size_13
        parts = pattern_name.split("_")
        size_num = int(parts[1])
        filter_key = f"size_{size_num}"

        pattern = pattern_info["input"]
        expected = normalize_label(pattern_info["expected"])

        # filter_key 존재 여부 검사
        if filter_key not in filters:
            fail_count += 1
            reason = f"{filter_key} 필터가 존재하지 않음"
            fail_cases.append((pattern_name, reason))
            print(f"FAIL: {reason}")
            continue

        cross_filter = filters[filter_key]["cross"]
        x_filter = filters[filter_key]["x"]

        # 크기 검사
        if not is_valid_matrix_size(pattern, size_num):
            fail_count += 1
            reason = f"패턴 크기 불일치 (기대: {size_num}x{size_num})"
            fail_cases.append((pattern_name, reason))
            print(f"FAIL: {reason}")
            continue

        if not is_valid_matrix_size(cross_filter, size_num):
            fail_count += 1
            reason = f"Cross 필터 크기 불일치 (기대: {size_num}x{size_num})"
            fail_cases.append((pattern_name, reason))
            print(f"FAIL: {reason}")
            continue

        if not is_valid_matrix_size(x_filter, size_num):
            fail_count += 1
            reason = f"X 필터 크기 불일치 (기대: {size_num}x{size_num})"
            fail_cases.append((pattern_name, reason))
            print(f"FAIL: {reason}")
            continue

        # MAC 점수 계산
        cross_score = mac(pattern, cross_filter)
        x_score = mac(pattern, x_filter)

        # 판정
        judge_result = judge(cross_score, x_score)
        predicted = convert_judge_result(judge_result)

        # PASS / FAIL
        if predicted == expected:
            status = "PASS"
            pass_count += 1
        else:
            status = "FAIL"
            fail_count += 1

            if predicted == "UNDECIDED":
                reason = "동점(UNDECIDED) 처리 규칙"
            else:
                reason = f"예상값 불일치 (predicted={predicted}, expected={expected})"

            fail_cases.append((pattern_name, reason))

        print(f"Cross 점수: {cross_score}")
        print(f"X 점수: {x_score}")
        print(f"판정: {predicted} | expected: {expected} | {status}")

    print("\n[3] 성능 분석 (평균/10회)")

    performance_sizes = [5, 13, 25]

    print("크기\t평균 시간(ms)\t연산 횟수")
    print("-" * 40)

    for size_num in performance_sizes:
        filter_key = f"size_{size_num}"
        cross_filter = filters[filter_key]["cross"]
        x_filter = filters[filter_key]["x"]

        # 같은 크기의 첫 번째 패턴 하나를 찾아서 시간 측정
        sample_pattern = None
        for pattern_name, pattern_info in patterns.items():
            if pattern_name.startswith(f"size_{size_num}_"):
                sample_pattern = pattern_info["input"]
                break

        if sample_pattern is not None:
            avg_time = measure_time(sample_pattern, cross_filter, x_filter, repeat=10)
            print(f"{size_num}x{size_num}\t{avg_time:.6f}\t\t{size_num * size_num}")

    print("\n[4] 결과 요약")
    print(f"총 테스트: {total_count}개")
    print(f"통과: {pass_count}개")
    print(f"실패: {fail_count}개")

    if fail_cases:
        print("실패 케이스:")
        for case_name, reason in fail_cases:
            print(f"- {case_name}: {reason}")
    
def load_json_data(path="data.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    

def normalize_label(label):
    """
    표준 라벨로 변환
    expected 값: '+' -> Cross, 'x' -> X
    filter 키: 'cross' -> Cross, 'x' -> X
    """
    if label == "+":
        return "Cross"
    elif label == "x":
        return "X"
    elif label == "cross":
        return "Cross"
    elif label == "X":
        return "X"
    elif label == "Cross":
        return "Cross"
    else:
        return label


def convert_judge_result(result):
    """
    judge() 결과(A/B/UNDECIDED)를 표준 라벨로 변환
    A = Cross
    B = X
    """
    if result == "A":
        return "Cross"
    elif result == "B":
        return "X"
    else:
        return "UNDECIDED"


def is_valid_matrix_size(matrix, expected_size):
    """
    matrix가 expected_size x expected_size인지 검사
    """
    if len(matrix) != expected_size:
        return False

    for row in matrix:
        if len(row) != expected_size:
            return False

    return True