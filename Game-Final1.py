board = [['#', '↓', '↓', '↓', '#'],
         ['→', '0', '0', '0', '#'],
         ['→', '0', '0', '0', '#'],
         ['→', '0', '0', '0', '#'],
         ['#', '#', '#', '#', '#']]


def position(board, player, num_pieace):
    if player == '1':
        line = int(num_pieace)
        pos = board[line].index('→')

    if player == '2':
        pos = int(num_pieace)
        line = -1
        for item in board:
            if '↓' == item[pos]:
                line = board.index(item)

    return (line, pos)


def move_count(board, player, pieace):
    if player == '1':
        if (pieace[1] <= 2) and (board[pieace[0]][pieace[1] + 1] == '↓') and (board[pieace[0]][pieace[1] + 2] == '↓'):
            return 0
        elif pieace[1] <= 2 and board[pieace[0]][pieace[1] + 1] == '↓':
            return 2
        elif pieace[1] <= 3:

            return 1
        return 0
    elif player == '2':
        if pieace[0] <= 2 and board[pieace[0] + 1][pieace[1]] == '→' and board[pieace[0] + 2][pieace[1]] == '→':
            return 0
        elif pieace[0] <= 2 and board[pieace[0] + 1][pieace[1]] == '→':
            return 2
        elif pieace[0] <= 3:
            return 1
        return 0


def move(board, player, num_pieace):
    pieace = position(board, player, num_pieace)
    if player == '1':
        if move_count(board, player, pieace) == 0:
            return False
        elif move_count(board, player, pieace) == 1:
            board[pieace[0]][pieace[1]], board[pieace[0]][pieace[1] + 1] = 0, '→'
        elif move_count(board, player, pieace) == 2:
            board[pieace[0]][pieace[1]], board[pieace[0]][pieace[1] + 2] = 0, '→'

    if player == '2':
        if move_count(board, player, pieace) == 0:
            return False
        elif move_count(board, player, pieace) == 1:
            board[pieace[0]][pieace[1]], board[pieace[0] + 1][pieace[1]] = 0, '↓'
        elif move_count(board, player, pieace) == 2:
            board[pieace[0]][pieace[1]], board[pieace[0] + 2][pieace[1]] = 0, '↓'
    return board


def is_lock(board, player):
    for i in range(1, 4):
        if move_count(board, player, position(board, player, i)) != 0:
            return False
    return True


def win(board):
    c2 = 0
    for item in board[-1]:
        if item == '↓':
            c2 += 1
    if c2 == 3:
        return '2'
    c1 = 0
    for item in board:
        if item[-1] == '→':
            c1 += 1
    if c1 == 3:
        return '1'
    return 0


def evaluate(board, player):
    global mover

    if player == '1':
        opposing_player = '2'
    else:
        opposing_player = '1'

    if win(board) == player:
        return True
    elif win(board) == opposing_player:
        return False

    if is_lock(board, player):
        return not evaluate(board, opposing_player)

    for num_pieace in range(1, 4):
        board_copy = [board[0].copy(), board[1].copy(),
                      board[2].copy(), board[3].copy(), board[4].copy()]
        pieace = position(board_copy, player, num_pieace)
        if move_count(board_copy, player, pieace) != 0:
            board_copy = move(board_copy, player, num_pieace)
            if not evaluate(board_copy, opposing_player):
                mover = num_pieace
                return True
    return False

def print_board(board):

    for i in board:
        for j in i:
            print(j,sep=' ',end=' ')
        print()

def run():
    global board
    global mover
    while True:

        player = input("which side do you want to be ? ")

        if int(player) not in range(1,3):
            print('the number of player should be 1 or 2')

        if int(player) in range(1,3):
            break


    if player == '1':
        opposing_player = '2'
    else:
        opposing_player = '1'
    turn = '1'
    while True:
        if turn == player:

            if not is_lock(board,player):
                print_board(board)

                while True:
                     num_pieace = int(input("Chose the pieace you want to move .. "))
                     if int(num_pieace) not in range(1, 4):
                         print('the number of pieace should be 1 or 2 or 3')

                     elif move_count(board, player, position(board, player, num_pieace)) == 0:
                         print('you cant move this pieace ... choose another one .')

                     if int(num_pieace) in range(1, 4) and move_count(board, player, position(board, player, num_pieace)) != 0:
                         break


                move(board, player, num_pieace)
            else:
                print_board(board)
                print('its your turn but you are locked ... so i will move!')

            turn=opposing_player

        elif turn == opposing_player:

            if not is_lock(board,opposing_player):
                evaluate(board, opposing_player)
                if mover != -1:
                    move(board, opposing_player, mover)
                else:
                    for num_pieace in range(1,4):
                        if move_count(board, opposing_player, position(board, opposing_player, num_pieace)) != 0:
                            move(board, opposing_player, num_pieace)
                            break
            else:
                print_board(board)
                print('its my turn but im locked ... so you can move!')

            turn = player

        if win(board) != 0:
            if win(board)==player:
                print('You won the game!')
                print_board(board)
            else:
                print('I won ... you lost!')
                print_board(board)
            break
mover = -1
run()