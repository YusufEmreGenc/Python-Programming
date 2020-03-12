import sys

fib_dict = {0: 0, 1: 1}


def elemNumOfBoard(board):
    num = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                num += 1
    return num


def show_board(b):
    for i in range(len(b)):
        for j in range(len(b[i])):
            print(b[i][j], end=" ")
        print()
    print()


def fibo(n):
    if n in fib_dict.keys():
        return fib_dict[n]
    else:
        fib_dict[n] = fibo(n-2) + fibo(n-1)
        return fib_dict[n]


def check_index_in(row, column, board):
    if row <= 0 or column <= 0:
        print('Please enter a correct size')
        return False
    try:
        board[row-1][column-1]
    except IndexError:
        print('Please enter a correct size')
        return False
    return True


def check_above(val, row, column, board):
    if row-2 < 0 or column-1 < 0:
        return False
    try:
        board[row-2][column-1]
    except IndexError:
        return False
    if board[row-2][column-1] == val:
        return True
    else:
        return False


def check_below(val, row, column, board):
    if row < 0 or column-1 < 0:
        return False
    try:
        board[row][column-1]
    except IndexError:
        return False
    if board[row][column-1] == val:
        return True
    else:
        return False


def check_right(val, row, column, board):
    if row-1 < 0 or column < 0:
        return False
    try:
        board[row-1][column]
    except IndexError:
        return False
    if board[row-1][column] == val:
        return True
    else:
        return False


def check_left(val, row, column, board):
    if row-1 < 0 or column-2 < 0:
        return False
    try:
        board[row-1][column-2]
    except IndexError:
        return False
    if board[row-1][column-2] == val:
        return True
    else:
        return False


def del_num (val, row, column, board, num):
    if not(check_above(val, row, column, board) or check_below(val, row, column, board) or check_right(val, row, column, board) or check_left(val, row, column, board)):
        return 0
    else:
        board[row-1][column-1] = ' '
        if check_above(val, row, column, board):
            if not(check_above(val, row-1, column, board) or check_left(val, row-1, column, board) or check_right(val, row-1, column, board)):
                board[row-2][column-1] = ' '
                num+=1

            else:
                if check_above(val, row-1, column, board):
                    num = del_num(val, row - 1, column, board, num+1)
                if check_left(val, row-1, column, board):
                    num = del_num(val, row - 1, column, board, num+1)
                if check_right(val, row-1, column, board):
                    num = del_num(val, row - 1, column, board, num+1)

        if check_below(val, row, column, board):
            if not(check_below(val, row+1, column, board) or check_left(val, row+1, column, board) or check_right(val, row+1, column, board)):
                board[row][column-1] = ' '
                num+=1

            else:
                if check_below(val, row+1, column, board):
                    num = del_num(val, row + 1, column, board, num+1)
                if check_left(val, row+1, column, board):
                    num = del_num(val, row + 1, column, board, num+1)
                if check_right(val, row+1, column, board):
                    num = del_num(val, row + 1, column, board, num+1)

        if check_left(val, row, column, board):
            if not(check_above(val, row, column-1, board) or check_left(val, row, column-1, board) or check_below(val, row, column-1, board)):
                board[row-1][column-2] = ' '
                num+=1

            else:
                if check_above(val, row, column-1, board):
                    num = del_num(val, row, column-1, board, num+1)
                if check_left(val, row, column-1, board):
                    num = del_num(val, row, column-1, board, num+1)
                if check_below(val, row, column-1, board):
                    num = del_num(val, row, column-1, board, num+1)

        if check_right(val, row, column, board):
            if not(check_above(val, row, column+1, board) or check_right(val, row, column+1, board) or check_below(val, row, column+1, board)):
                board[row-1][column] = ' '
                num+=1

            else:
                if check_above(val, row, column+1, board):
                    num = del_num(val, row, column+1, board, num+1)
                if check_right(val, row, column+1, board):
                    num = del_num(val, row, column+1, board, num+1)
                if check_below(val, row, column+1, board):
                    num = del_num(val, row, column+1, board, num+1)
    return num

def check_column(column, board):
    flag = True
    for row in range(len(board)):
        if board[row][column] != ' ':
            flag = False
    return flag

def check_row(row, board):
    flag = True
    for column in range(len(board[-1])):
        if board[row][column] != ' ':
            flag = False
    return flag


def fix_board(board):
    column = 0
    while column < len(board[-1]):
        flag = True
        if check_column(column, board):
            flag = False
            for row in range(len(board)):
                board[row].pop(column)

        for row in range(len(board)-2, -1, -1):
            if board[row][column] != ' ':
                while board[row+1][column] == ' ':
                    board[row + 1][column] = board[row][column]
                    board[row][column] = ' '
                    row += 1
                    if row == len(board)-1:
                        break
        if flag:
            column += 1

    try:
        while check_row(0, board):
            board.pop(0)
    except IndexError:
        pass

score = 0
fhandle = open(sys.argv[1], 'r')

board = list()
for line in fhandle:
    numbers = [int(x) for x in line.split()]
    board.append(numbers)


show_board(board)

print('Your score is:', score)
print()

while True:
    num = 0
    flag = False
    for i in range(1, len(board)+1):
        for j in range(1, len(board[i-1])+1):
            if board[i-1][j-1] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                if check_above(board[i-1][j-1], i, j, board) or check_below(board[i-1][j-1], i, j, board) or check_left(board[i-1][j-1], i, j, board) or check_right(board[i-1][j-1], i, j, board):
                    flag = True

    if not flag:
        print('Game over', end='')
        exit()

    s = input('Please enter a row and column number: ')
    print()
    if len(s.split()) != 2:
        print('Please give exactly 2 arguments\n')
        continue
    try:
        row = int(s.split()[0])
        column = int(s.split()[1])
    except ValueError:
        print('Please enter only positive integers\n')
        continue
    try:
        if not board[row-1][column-1] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            print("Please enter a correct size!\n")
            continue
    except IndexError:
        print("Please enter a correct size!\n")
        continue

    if check_index_in(row, column, board):
        val = board[row - 1][column - 1]
        num = del_num(val, row, column, board, 1)
        fix_board(board)
        show_board(board)
        score += val * fibo(num)
        print('Your score is:', score)
        print()
        try:
            board[0][0]
        except IndexError:
            print('Game over', end='')
            exit()
