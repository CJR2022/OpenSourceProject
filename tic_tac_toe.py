##################

# 프로그램명: Grade Manager

# 작성자: 소프트웨어학부/최정륜(2022041015)

# 작성일: 2025.04.

# 컴퓨터를 상대로 하는 틱택토 프로그램

###################
import random

def print_board(board): #보드출력
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_win(board, player):   #승리여부
    #열과 행 검사
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True
    #대각선 검사
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw(board):  #무승부여부
    return all(board[i][j] != " " for i in range(3) for j in range(3))

def get_computer_move(board):   #컴퓨터 랜덤 플레이
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                empty_cells.append((i, j))  #모든 빈칸의 행과 열 저장
    return random.choice(empty_cells)   #랜덤하게 빈칸을 선택 후 행과 열 반환

def tic_tac_toe():  #전체진행
    board = [[" " for _ in range(3)] for _ in range(3)]
    player_marker = "X"
    computer_marker = "O"

    while True:
        print_board(board)
        row = int(input(f"플레이어({player_marker}) 차례입니다. 행을 선택하세요 (0, 1, 2): "))
        col = int(input(f"플레이어({player_marker}) 차례입니다. 열을 선택하세요 (0, 1, 2): "))
        if board[row][col] == " ":
            board[row][col] = player_marker
            if check_win(board, player_marker):
                print_board(board)
                print("플레이어 승리")
                break
            elif check_draw(board):
                print_board(board)
                print("무승부")
                break
            
            computer_row, computer_col = get_computer_move(board)
            board[computer_row][computer_col] = computer_marker
            if check_win(board, computer_marker):
                print_board(board)
                print("컴퓨터 승리")
                break
            elif check_draw(board):
                print_board(board)
                print("무승부")
                break
        else:
            print("이미 선택된 칸입니다. 다시 선택하세요.")

if __name__ == "__main__":
    tic_tac_toe()