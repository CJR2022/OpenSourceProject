# 2022041015 최정륜
# 5명의 학생의 세개의 교과목 (영어, C-언어, 파이썬)에 대하여  키보드로부터 입력받아 총점, 평균, 학점, 등수를 계산하는 프로그램 작성

def grade(stu, sub):
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

def rank(stu_list, stu, sub):
    result = 1
    for i in range(students_num):
        if stu['id'] != stu_list[i]['id'] and stu[sub] < stu_list[i][sub]:
            result += 1
    return result

def input_info(stu_list):
    for i in range(students_num):
        print("===========================")
        s_id = input("학번 : ")
        name = input("이름 : ")
        en = int(input("영어 점수 : "))
        c = int(input("c언어 점수 : "))
        p = int(input("파이썬 점수 : "))
        stu_list.append({'name': name, 'en': en, 'c': c, 'p': p, 'id': s_id})
        print("===========================\n")

def calc_total_ave(stu):
    total = stu['en']+stu['c']+stu['p']
    ave = float(total / 3)
    return total, ave

def print_info(stu_list):
    print(f"\n{'성적관리 프로그램':>20}\n")
    print("=============================================================================\n")
    print(f"{'학번':<8}{'이름':>4}{'영어':>8}{'C-언어':>8}"
          f"{'파이썬':>8}{'총점':>8}{'평균':>8}{'학점':>8}{'등수':>8}\n")
    print("=============================================================================\n")
    for k in stu_list:
        k['total'], k['ave'] = calc_total_ave(k)
        k['grade'] = grade(k,'total')
        k['rank'] = rank(stu_list,k,'total')
        print(f"{k['id']:<8}{k['name']:>4}{k['en']:>8}{k['c']:>8}"
              f"{k['p']:>8}{k['total']:>8}{k['ave']:>8}{k['grade']:>8}{k['rank']:>8}")


students_num = 5

def main():
    students = []
    input_info(students)
    print_info(students)
