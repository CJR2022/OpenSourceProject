# 2022041015 최정륜
# 5명의 학생의 세개의 교과목 (영어, C-언어, 파이썬)에 대하여  키보드로부터 입력받아 총점, 평균, 학점, 등수를 계산하는 프로그램 작성
from operator import itemgetter


def grade(stu, sub):    #학점계산함수
    if sub == "total":
        score = stu[sub] / 3
    else:
        score = stu[sub]
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

def rank(stu_list, Snum):   #등수계산함수
    for i in stu_list:
        rank = 1
        for j in stu_list:
            if i['total'] < j['total']:
                rank += 1
        i['rank'] = rank

def input_info(stu_list, index):   #입력함수
    print("\n===========================")
    s_id = int(input("학번 : "))
    name = input("이름 : ")
    en = int(input("영어 점수 : "))
    c = int(input("c언어 점수 : "))
    p = int(input("파이썬 점수 : "))
    stu_list.insert(index, {'name': name, 'en': en, 'c': c, 'p': p, 'id': s_id})
    stu_list[index]['total'], stu_list[index]['ave'] = calc_total_ave(stu_list[index])
    stu_list[index]['grade'] = grade(stu_list[index],'total')
    print("===========================\n")

def calc_total_ave(stu):    #총점/평균계산함수
    total = stu['en']+stu['c']+stu['p']
    ave = float(total / 3)
    return total, ave

def print_info(stu):    #한 학생 정보 출력
    print(f"\n{'성적관리 프로그램':>20}\n")
    print("========================================================================================\n")
    print(f"{'학번':<12}{'이름':>8}{'영어':>7}{'C-언어':>7}"
          f"{'파이썬':>7}{'총점':>7}{'평균':>7}{'학점':>7}{'등수':>7}\n")
    print("========================================================================================\n")
    print(f"{stu['id']:<13}{stu['name']:>10}{stu['en']:>9}{stu['c']:>9}"
    f"{stu['p']:>9}{stu['total']:>9}{stu['ave']:>9.2f}{stu['grade']:>9}{stu['rank']:>9}\n")

def print_all_info(stu_list):   #출력함수
    print(f"\n{'성적관리 프로그램':>20}\n")
    print("========================================================================================\n")
    print(f"{'학번':<12}{'이름':>8}{'영어':>7}{'C-언어':>7}"
          f"{'파이썬':>7}{'총점':>7}{'평균':>7}{'학점':>7}{'등수':>7}\n")
    print("========================================================================================\n")
    for k in stu_list:
        print(f"{k['id']:<13}{k['name']:>10}{k['en']:>9}{k['c']:>9}"
              f"{k['p']:>9}{k['total']:>9}{k['ave']:>9.2f}{k['grade']:>9}{k['rank']:>9}")
    print(f"[80점 이상 학생 수:    {count_80_up(stu_list)}]\n")

def menu():     #메뉴출력
    print("===========================")
    print("  1 : 전체 학생 정보 출력")
    print("  2 : 정렬된 학생 정보 출력")
    print("  3 : 학생 정보 검색")
    print("  4 : 새로운 학생 정보 입력")
    print("  5 : 학생 정보 삭제")
    print("  6 : 종료")
    print("===========================")

def insert_info(stu_list, Snum):  #삽입함수
    index = int(input(f"\n몇번째 위치에 입력하시겠습니까(현재 총 학생 수 : {Snum}) : "))
    input_info(stu_list, index)

def delete_info(stu_list):  #삭제함수
    stu = search_stu(stu_list)
    if stu != False:
        stu_list.remove(stu)
    else:
        return False

def search_stu(stu_list):  #탐색함수, 학번과 이름이 일치한 학생의 딕셔너리 리턴
    student_id = int(input("\n 검색할 학생의 학번 : "))
    Sname = input(" 검색할 학생의 이름 : ")
    for i in stu_list:
        if i['id'] == student_id and i['name'] == Sname:
            return i
    print("존재하지 않는 학생")
    return False

def sort_info(stu_list):    #정렬함수
    return sorted(stu_list, key = itemgetter('total'), reverse = True)

def count_80_up(stu_list):  #80점 이상 학생 수 카운트 함수
    count = 0
    for i in stu_list:
        if i['ave'] >= 80:
            count += 1
    return count


if __name__ == '__main__':
    students_num = 0
    students = []
    for i in range(5):
        input_info(students, students_num) #5명의 정보 선입력 - 과제 조건
        students_num += 1
    rank(students, students_num)
    while True:
        menu()
        s = int(input("입력 : "))
        if s == 1:
            print_all_info(students)
        elif s == 2:
            print_all_info(sort_info(students))
        elif s == 3:
            print_info(search_stu(students))
        elif s == 4:
            insert_info(students, students_num)
            students_num += 1
            rank(students, students_num)
        elif s == 5:
            if delete_info(students) != False:
                students_num -= 1
                rank(students, students_num)
        elif s == 6:
            break

