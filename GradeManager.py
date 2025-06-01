##################

# 프로그램명: Grade Manager (MySQL DB 연동 버전)

# 작성자: 소프트웨어학부/최정륜(2022041015)

# 작성일: 2025.06.02

# 프로그램 설명: 학생의 세개의 교과목 (영어, C-언어, 파이썬)에 대하여 키보드로부터
# 학번, 이름, 영어점수, C-언어 점수, 파이썬 점수를 입력받아 총점, 평균, 학점, 등수를 계산하는 프로그램
# 학생 정보를 데이터 베이스에 저장 및 불러오기

###################

import mysql.connector
from mysql.connector import Error

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
        # 데이터베이스 연결 정보 (본인의 MySQL 환경에 맞게 수정해주세요!)
        self.db_config = {
            'host': 'localhost',  # MySQL 서버 주소
            'user': 'root',       # MySQL 사용자 이름
            'password': '*****', # MySQL 비밀번호 (과제 제출용이기에 비밀번호는 가렸습니다)
            'database': 'student' # 데이터베이스 이름
        }

        self.conn = None
        self.cursor = None
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            if self.conn.is_connected():
                print("MySQL 데이터베이스에 성공적으로 연결되었습니다.")
                self.cursor = self.conn.cursor()
                self._load_students_from_db() # 프로그램 시작 시 DB에서 학생 정보 불러오기
            else:
                print("MySQL 데이터베이스 연결에 실패했습니다.")
                exit()
        except Error as e:
            print(f"데이터베이스 연결 오류: {e}")
            print("MySQL 서버가 실행 중인지, 계정 정보와 데이터베이스 이름이 올바른지 확인해주세요.")
            exit()


    def _load_students_from_db(self):
        # 데이터베이스에서 모든 학생 정보를 불러와 self.students 리스트에 저장
        self.students = [] # 기존 리스트 초기화
        try:
            self.cursor.execute("SELECT id, name, eng, c, python FROM score")
            rows = self.cursor.fetchall()
            for row in rows:
                student = Student(row[0], row[1], row[2], row[3], row[4])
                self.students.append(student)
            self.update_ranks() # 등수 업데이트
        except Error as e:
            print(f"학생 정보 로드 오류: {e}")

    def add_student(self, student):
        # 학생을 리스트에 추가하고 등수를 업데이트 (DB 저장 포함)
        try:
            # MySQL은 플레이스홀더로 %s 사용
            self.cursor.execute("""
                INSERT INTO score (id, name, eng, c, python)
                VALUES (%s, %s, %s, %s, %s)
            """, (student.id, student.name, student.en, student.c, student.p))
            self.conn.commit() # DB에 저장
            print("학생 정보가 데이터베이스에 성공적으로 추가되었습니다.")
            self._load_students_from_db() # DB 추가 후 메모리 리스트 동기화 및 등수 업데이트
        except mysql.connector.IntegrityError as e:
            # MySQL의 IntegrityError는 학번 중복 등을 포함
            if e.errno == 1062: # Duplicate entry for primary key
                print(f"오류: 학번 {student.id}는 이미 존재합니다. 다른 학번을 입력하세요.")
            else:
                print(f"데이터베이스 추가 중 무결성 오류 발생: {e}")
        except Error as e:
            print(f"데이터베이스 추가 중 오류 발생: {e}")

    def update_ranks(self):
        # 학생 리스트를 총점 기준으로 정렬하고 등수를 설정
        self.students = self.sort_students()
        for idx, student in enumerate(self.students):
            student.rank = idx + 1

    def print_all_students(self):
        # 모든 학생 정보를 출력
        if not self.students:
            print("\n저장된 학생 정보가 없습니다. 새로운 학생을 추가해주세요.")
            return

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
        # 학번과 이름으로 학생을 검색 (메모리 리스트에서 검색)
        for student in self.students:
            if student.id == student_id and student.name == name:
                return student
        print("존재하지 않는 학생입니다.")
        return None

    def delete_student(self, student_id, name):
        # 학번과 이름으로 학생을 삭제 (DB에서 삭제 포함)
        try:
            # 먼저 해당 학생이 DB에 존재하는지 확인
            self.cursor.execute("SELECT id FROM score WHERE id = %s AND name = %s", (student_id, name))
            result = self.cursor.fetchone()

            if result:
                self.cursor.execute("DELETE FROM score WHERE id = %s AND name = %s", (student_id, name))
                self.conn.commit() # DB에서 삭제
                print("학생 정보가 데이터베이스에서 성공적으로 삭제되었습니다.")
                self._load_students_from_db() # DB 삭제 후 메모리 리스트 동기화 및 등수 업데이트
                return True
            else:
                print("존재하지 않는 학생입니다.")
                return False
        except Error as e:
            print(f"데이터베이스 삭제 중 오류 발생: {e}")
            return False

    def sort_students(self):
        # 학생 리스트를 총점 기준으로 정렬하여 반환
        return sorted(self.students, key=lambda x: x.total, reverse=True)

    def menu(self):
        # 메뉴를 출력
        print("\n===========================")
        print("  1 : 전체 학생 정보 출력")
        print("  2 : 학생 정보 검색")
        print("  3 : 새로운 학생 정보 입력")
        print("  4 : 학생 정보 삭제")
        print("  5 : 종료")
        print("===========================")

    def run(self):
        # 프로그램 실행 메서드
        try: # <<--- try 블록을 while 루프 밖으로 이동
            while True:
                self.menu()
                try: # <<--- 이 try 블록은 사용자 입력 및 개별 메뉴 처리용
                    choice = int(input("입력 : "))
                    if choice == 1:
                        self.print_all_students()
                    elif choice == 2:
                        student_id = int(input("\n검색할 학생의 학번 : "))
                        name = input("검색할 학생의 이름 : ")
                        student = self.search_student(student_id, name)
                        if student:
                            # 검색 결과 출력 시 헤더 다시 출력
                            print(f"\n{'성적관리 프로그램':>20}\n")
                            print("========================================================================================\n")
                            print(f"{'학번':<12}{'이름':>8}{'영어':>7}{'C-언어':>7}"
                                f"{'파이썬':>7}{'총점':>7}{'평균':>7}{'학점':>7}{'등수':>7}\n")
                            print("========================================================================================\n")
                            print(student)
                    elif choice == 3:
                        new_student_data = self.input_student()
                        if new_student_data: # 유효한 학생 데이터가 반환된 경우에만 추가
                            self.add_student(new_student_data)
                    elif choice == 4:
                        student_id = int(input("\n삭제할 학생의 학번 : "))
                        name = input("삭제할 학생의 이름 : ")
                        self.delete_student(student_id, name)
                    elif choice == 5:
                        print("프로그램을 종료합니다.")
                        break # <<--- 루프 종료
                    else:
                        print("잘못된 입력입니다. 1에서 5 사이의 숫자를 입력하세요.")
                except ValueError:
                    print("잘못된 입력입니다. 숫자를 입력해주세요.")
                except Exception as e:
                    print(f"예상치 못한 오류 발생: {e}")
        finally: # <<--- finally 블록을 while 루프 밖으로 이동
            if self.conn and self.conn.is_connected():
                self.cursor.close()
                self.conn.close() # 프로그램 종료 시 DB 연결 닫기
                print("MySQL 연결이 닫혔습니다.")

    def input_student(self):
        # 학생 정보를 입력받아 Student 객체를 생성
        print("\n===========================")
        try:
            student_id = int(input("학번 : "))
            name = input("이름 : ")
            en = int(input("영어 점수 : "))
            c = int(input("C언어 점수 : "))
            p = int(input("파이썬 점수 : "))
            if not (0 <= en <= 100 and 0 <= c <= 100 and 0 <= p <= 100):
                print("점수는 0에서 100 사이여야 합니다. 다시 입력해주세요.")
                return None # 유효하지 않은 점수 입력 시 None 반환
            print("===========================\n")
            return Student(student_id, name, en, c, p)
        except ValueError:
            print("잘못된 입력입니다. 학번과 점수는 숫자로 입력해주세요.")
            return None # 유효하지 않은 입력 시 None 반환


if __name__ == '__main__':
    # 프로그램 실행
    manager = GradeManager()
    manager.run()