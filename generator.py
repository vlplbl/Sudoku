''' Sudoku Solver '''

import random


def generate_board(difficulty):
    ''' generate board with difficulty of 30 to 90 '''
    board = [[0 for i in range(9)] for j in range(9)]
    solve(board)
    full_board = [[board[col][row] for row in range(
        len(board))] for col in range(len(board[0]))]
    attempts = difficulty
    while attempts > 0:
        removed = (random.randint(0, 8), random.randint(0, 8))
        while board[removed[0]][removed[1]] == 0:
            removed = (random.randint(0, 8), random.randint(0, 8))
        backup = board[removed[0]][removed[1]]
        board[removed[0]][removed[1]] = 0
        # creating a copy of the board
        copy_board = [[board[col][row] for row in range(
            len(board))] for col in range(len(board[0]))]
        # check if there is only one solution
        counter = 1
        for i in range(10):
            solve(copy_board)
            if copy_board != full_board:
                counter += 1
                break
        # return the taken out number back
        if counter != 1:
            board[removed[0]][removed[1]] = backup
        attempts -= 1
    return board


def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find_empty(board)
    lst = list(range(1, 10))
    random.shuffle(lst)
    for i in lst:
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0
    return False


def valid(board, num, pos):
    # horizontal check
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    # vertical check
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    # check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None
