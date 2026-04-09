"""
프로그램의 시작만 담당하는 파일
"""
from simulator import run_mode1, run_mode2


def main():
    while True:
        print("=== Mini NPU Simulator ===")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("0. 종료")

        choice = input("선택: ")

        if choice == "1":
            run_mode1()
        elif choice == "2":
            run_mode2()
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 메뉴 번호를 입력하세요.")


if __name__ == "__main__":
    main()