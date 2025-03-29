# 2022041015 최정륜
# 5명의 학생의 세개의 교과목 (영어, C-언어, 파이썬)에 대하여  키보드로부터 입력받아 총점, 평균, 학점, 등수를 계산하는 프로그램 작성

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

def rank(stu_list, stu, sub, StudentNum):   #등수계산함수
    result = 1
    for i in range(StudentNum):
        if stu[sub] < stu_list[i][sub]:
            result += 1
    return result

def input_info(stu_list, StudentNum):   #입력함수
    for i in range(StudentNum):
        print("===========================")
        s_id = input("학번 : ")
        name = input("이름 : ")
        en = int(input("영어 점수 : "))
        c = int(input("c언어 점수 : "))
        p = int(input("파이썬 점수 : "))
        stu_list.append({'name': name, 'en': en, 'c': c, 'p': p, 'id': s_id})
        stu_list[i]['total'], stu_list[i]['ave'] = calc_total_ave(stu_list[i])
        print("===========================\n")

def calc_total_ave(stu):    #총점/평균계산함수
    total = stu['en']+stu['c']+stu['p']
    ave = float(total / 3)
    return total, ave

def print_info(stu_list, StudentNum):   #출력함수
    print(f"\n{'성적관리 프로그램':>20}\n")
    print("========================================================================================\n")
    print(f"{'학번':<12}{'이름':>8}{'영어':>7}{'C-언어':>7}"
          f"{'파이썬':>7}{'총점':>7}{'평균':>7}{'학점':>7}{'등수':>7}\n")
    print("========================================================================================\n")
    for k in stu_list:
        k['grade'] = grade(k,'total')
        k['rank'] = rank(stu_list, k, 'total', StudentNum)
        print(f"{k['id']:<13}{k['name']:>10}{k['en']:>9}{k['c']:>9}"
              f"{k['p']:>9}{k['total']:>9}{k['ave']:>9.2f}{k['grade']:>9}{k['rank']:>9}")

if __name__ == '__main__':
    students_num = 2
    students = []
    input_info(students, students_num)
    print_info(students, students_num)
