##################

# 프로그램명: Grade Manager

# 작성자: 소프트웨어학부/최정륜(2022041015)

# 작성일: 2025.04.16

# 프로그램 설명: 학생의 세개의 교과목 (영어, C-언어, 파이썬)에 대하여 키보드로부터 
# 학번, 이름, 영어점수, C-언어 점수, 파이썬 점수를 입력받아 총점, 평균, 학점, 등수를 계산하는 프로그램

###################

class Student:
    def __init__(self, student_id, name, en, c, p):
        # 학생의 학번, 이름, 영어, C언어, 파이썬 점수를 초기화
        self.id = student_id
        self.name = name
        self.en = en
        self.c = c
        self.p = p
        self.total = self.en + self.c + self.p  # 총점 계산
        self.ave = self.total / 3  # 평균 계산
        self.grade = self.calculate_grade(self.ave)  # 학점 계산
        self.rank = None  # 등수는 초기화 후 별도로 설정

    def calculate_grade(self, score):
        # 평균 점수를 기준으로 학점을 계산
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

    def __str__(self):
        # 학생 정보를 문자열로 반환
        return (f"{self.id:<13}{self.name:>10}{self.en:>9}{self.c:>9}"
                f"{self.p:>9}{self.total:>9}{self.ave:>9.2f}{self.grade:>9}{self.rank:>9}")


class GradeManager:
    def __init__(self):
        # 학생 리스트를 초기화
        self.students = []

    def add_student(self, student):
        # 학생을 리스트에 추가하고 등수를 업데이트
        self.students.append(student)
        self.update_ranks()

    def update_ranks(self):
        # 학생 리스트를 총점 기준으로 정렬하고 등수를 설정
        self.students = self.sort_students()
        for idx, student in enumerate(self.students):
            student.rank = idx + 1

    def print_all_students(self):
        # 모든 학생 정보를 출력
        print(f"\n{'성적관리 프로그램':>20}\n")
        print("========================================================================================\n")
        print(f"{'학번':<12}{'이름':>8}{'영어':>7}{'C-언어':>7}"
              f"{'파이썬':>7}{'총점':>7}{'평균':>7}{'학점':>7}{'등수':>7}\n")
        print("========================================================================================\n")
        for student in self.students:
            print(student)
        print(f"[80점 이상 학생 수:    {self.count_80_up()}]\n")

    def count_80_up(self):
        # 평균 점수가 80점 이상인 학생 수를 반환
        return sum(1 for student in self.students if student.ave >= 80)

    def search_student(self, student_id, name):
        # 학번과 이름으로 학생을 검색
        for student in self.students:
            if student.id == student_id and student.name == name:
                return student
        print("존재하지 않는 학생")
        return None

    def delete_student(self, student_id, name):
        # 학번과 이름으로 학생을 삭제
        student = self.search_student(student_id, name)
        if student:
            self.students.remove(student)
            self.update_ranks()
            return True
        return False

    def sort_students(self):
        # 학생 리스트를 총점 기준으로 정렬하여 반환
        return sorted(self.students, key=lambda x: x.total, reverse=True)

    def menu(self):
        # 메뉴를 출력
        print("===========================")
        print("  1 : 전체 학생 정보 출력")
        print("  2 : 학생 정보 검색")
        print("  3 : 새로운 학생 정보 입력")
        print("  4 : 학생 정보 삭제")
        print("  5 : 종료")
        print("===========================")

    def run(self):
        # 프로그램 실행 메서드
        for _ in range(5):
            self.add_student(self.input_student())  # 초기 5명의 학생 정보 입력
        while True:
            self.menu()
            choice = int(input("입력 : "))
            if choice == 1:
                self.print_all_students()
            elif choice == 2:
                student_id = int(input("\n검색할 학생의 학번 : "))
                name = input("검색할 학생의 이름 : ")
                student = self.search_student(student_id, name)
                if student:
                    print(f"\n{'성적관리 프로그램':>20}\n")
                    print("========================================================================================\n")
                    print(f"{'학번':<12}{'이름':>8}{'영어':>7}{'C-언어':>7}"
                        f"{'파이썬':>7}{'총점':>7}{'평균':>7}{'학점':>7}{'등수':>7}\n")
                    print("========================================================================================\n")
                    print(student)
            elif choice == 3:
                self.add_student(self.input_student())
            elif choice == 4:
                student_id = int(input("\n삭제할 학생의 학번 : "))
                name = input("삭제할 학생의 이름 : ")
                if self.delete_student(student_id, name):
                    print("학생 정보가 삭제되었습니다.")
            elif choice == 5:
                break

    def input_student(self):
        # 학생 정보를 입력받아 Student 객체를 생성
        print("\n===========================")
        student_id = int(input("학번 : "))
        name = input("이름 : ")
        en = int(input("영어 점수 : "))
        c = int(input("C언어 점수 : "))
        p = int(input("파이썬 점수 : "))
        print("===========================\n")
        return Student(student_id, name, en, c, p)


if __name__ == '__main__':
    # 프로그램 실행
    manager = GradeManager()
    manager.run()

