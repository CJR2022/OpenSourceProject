# 5명의 학생의 세개의 교과목 (영어, C-언어, 파이썬)에 대하여  키보드로부터 입력받아 총점, 평균, 학점, 등수를 계산하는 프로그램 작성
# 각 학생의 3개 교과목 성적을 입력 받아 해당 교과목들에 대한 학생 개인의 총점, 평균, 학점, 등수를 출력하도록 해봤습니다.
# 학점은 90, 80, 70, 60 단위로 a, b, c, d, f 나눠서 부여했습니다.


def grade(target, sub):
    if sub == "total":
        score = target[sub] / 3
    else:
        score = target[sub]
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


def rank(stu_list, target, sub):
    result = 1
    for i in range(students_num):
        if target['id'] != stu_list[i]['id'] and target[sub] < stu_list[i][sub]:
            result += 1
    return result


students = []
students_num = 5
for i in range(students_num):
    print("===========================")
    name = input("이름 : ")
    en = int(input("영어 점수 : "))
    c = int(input("c언어 점수 : "))
    p = int(input("파이썬 점수 : "))
    students.append({'name': name, 'en': en, 'c': c, 'p': p, 'id': i, 'total': en + c + p})
    print("===========================\n")

for k in students:
    print("\n===========================\n")
    print(f"{k['name']}의 성적\n")
    print(f"영어 : {k['en']}, 학점 : {grade(k, 'en')}, 등수 : {rank(students, k, 'en')}\n")
    print(f"c언어 : {k['c']}, 학점 : {grade(k, 'c')}, 등수 : {rank(students, k, 'c')}\n")
    print(f"파이썬 : {k['p']}, 학점 : {grade(k, 'p')}, 등수 : {rank(students, k, 'p')}\n")
    print(f"총점 : {k['total']}, 평균 : {k['total'] / 3}, 종합등수 : {rank(students, k, 'total')}\n")
print("===========================")
