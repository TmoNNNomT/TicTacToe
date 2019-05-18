import numpy as np
import time
from tkinter import *
K = [0, 1, 2, 3, 4, 5, 6, 7, 8]
count = 0


class CreateTree:

    def __init__(self, possible_moves, win=0, player=1, level=0):
        # print(test, 'Entered init\n')
        self.level = level
        self.player = player
        self.win = win
        self.children = []
        self.value = []
        self.make_children(possible_moves, player, level)

    def make_children(self, possible_moves, player, level):
        # test+=1
        player = -player
        level += 1
        # print(test, 'Entered makechild\n')
        if not possible_moves:
            return
        for i in range(possible_moves):
            # print(test, 'Entered loop', i, '\n')
            self.children.append(CreateTree(possible_moves-1, 0, player, level))


def PrintTree(root):
    print(root.value)
    for child in root.children:
        PrintTree(child)


def initialize(Node):
    # if Node.value == [1, 0, 8, 3, 6, 7, 2, 4, 5]:
    #     print('YAA')
    if not Node.children:
        return
    for child in Node.children:             # overall This loop initializes all the children on the same level
        w = CheckWin(Node.value)
        # if Node.value == [1, 0, 8, 3, 6, 7, 2, 4]:
        #     for kkk in Node.children:
        #         print (kkk.value)
        #     print('w= ', w)
        if w:
            Node.win = w
            return
        child.value = Node.value.copy()
        # if Node.value == [1, 0, 8, 3, 6, 7, 2, 4]:
        #     print('child===', child.value)

        for k in K:                         # decides 'k' from K = [0,1,2] to be appended to child
            flag = 1
            if Node.value:
                for j in Node.value:        # check that k is not present in parent (Node)
                    if k == j:
                        flag = 0
                        break
                    else:
                        flag = 1
            # if Node.value == [1, 0, 8, 3, 6, 7, 2, 4]:
            #     print('k', k, flag)
            if flag == 1:                   # if k is not in parent node, then k is appended to child
                child.value.append(k)
                same = 0

                for baby in Node.children:  # check if any of the child on the same level are same
                    if baby.value == child.value:
                        same += 1

                if same == 1:               # only the child itself matches so this k is okay
                    # if Node.value == [1, 0, 8, 3, 6, 7, 2, 4]:
                    #     print(child.value,'here')
                    break
                else:
                    child.value.pop()       # child matches with someone other than itself, so go for different k

        initialize(child)
        if not child.children:
            w = CheckWin(child.value)
            if w:
                child.win = w


def CheckWin(position):
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    k = 1
    for move in position:
        if k == 1:
            board[move] = 1
            k = -1
        else:
            board[move] = -1
            k = 1
    # if position == [0, 3, 1, 2, 4, 7, 8, 5]:    #[1, 1, -1, -1, 1, -1, 0, -1, 1]
    #     print(board)
    # print(board)
    if [board[0], board[1], board[2]] == [1, 1, 1] or [board[3], board[4], board[5]] == [1, 1, 1] or [board[6], board[7], board[8]] == [1, 1, 1]:
        # if board == [1, 1, -1, -1, 1, -1, 0, -1, 1]:
        #     print('11111111')
        return 1
    elif [board[0], board[3], board[6]] == [1, 1, 1] or [board[1], board[4], board[7]] == [1, 1, 1] or [board[2], board[5], board[8]] == [1, 1, 1]:
        # if board == [1, 1, -1, -1, 1, -1, 0, -1, 1]:
        #     print('2222')
        return 1
    elif [board[0], board[4], board[8]] == [1, 1, 1] or [board[2], board[4], board[6]] == [1, 1, 1]:
        # if board == [1, 1, -1, -1, 1, -1, 0, -1, 1]:
        #     print('33333333333333')
        return 1

    if [board[0], board[1], board[2]] == [-1, -1, -1] or [board[3], board[4], board[5]] == [-1, -1, -1] or [board[6], board[7], board[8]] == [-1, -1, -1]:
        return -1
    elif [board[0], board[3], board[6]] == [-1, -1, -1] or [board[1], board[4], board[7]] == [-1, -1, -1] or [board[2], board[5], board[8]] == [-1, -1, -1]:
        return -1
    elif [board[0], board[4], board[8]] == [-1, -1, -1] or [board[2], board[4], board[6]] == [-1, -1, -1]:
        return -1
    else:
        return 0





def CreateBoard(position):
    boardi = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
    real = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    k = 1
    for move in position:
        if k == 1:
            boardi[move] = 'X'
            k = -1
        else:
            boardi[move] = 'O'
            k = 1
    ind = 0
    for i in range(3):
        for j in range(3):
            real[i][j] = boardi[ind]
            ind += 1
    real = np.matrix(real)

    return real


def Minimax(Node):
    global count
    count+=1
    if not Node.children:
        return
    # print('yes')

    for child in Node.children:
        if child.value == []:
            break
        Minimax(child)
        # print('childlevel=', child.level)
        flag = 0

        for baby in Node.children:

            if Node.player == baby.win:
                Node.win = baby.win
                flag = 1

        if flag == 0:
            for baby in Node.children:
                if baby.win == 0:
                    Node.win = 0
                    flag = 1

        if flag == 0:
            Node.win = -Node.player


def play(node):
    turn = 1
    round = 0
    win = 0
    n = []
    computer = -1
    choice = int(input('Enter 1 to play as X\nEnter 0 to play as O'))
    if choice == 0:
        computer = 1
        turn = 0
    flag = choice
    while win == 0:
        if choice:
            move = int(input('Enter your move: '))
            n.append(move)
            round += 1
            win = CheckWin(n)
            # print('n =', n)

            if win != 0:
                # print('win==', win)
                break
            if round == 9:
                break
        save = bestmove(node, n, computer, choice)
        node = save[0]
        # print(save)
        compmove = save[1][turn]
        n.append(compmove)
        round += 1
        print('Computer moves: ', compmove)
        print(CreateBoard(n))
        if round == 9:
            break
        win = CheckWin(n)
        if win != 0:
            break

        turn = turn + 2
        choice = 1

    if win == -1 and flag == 0:
        print('CONGRATULATIONS YOU WON!!!!')
    elif win == -1 and flag == 1:
        print('LMAO WHAT A LOSER!!')
    elif win == 1 and flag == 1:
        print('CONGRATULATIONS YOU WON!!!!')
    elif win == 1 and flag == 0:
        print('LMAO WHAT A LOSER!!')
    else:
        print('DRAW - pathetic')

    again = int(input('Enter 1 if you want to play again, otherwise enter 0'))
    if again:
        play(A)


def bestmove(node, n, computer, choice):
    global rd
    if computer == -1:
        for child in node.children:
            if child.value == n:
                break
    else:
        child = node
    if rd:
        for child in node.children:
            if child.value == n:
                break

    # print(node.player, ' player moved:', child.value)
    flag = 0
    for baby in child.children:
        # print(baby.win)
        if baby.win == computer:
            # print(baby.value)
            flag = 1
            break

    if flag == 0:
        for baby in child.children:
            if baby.win == 0:
                break

    return [baby, baby.value]


def displayboard():
    global movelist
    global rd
    def input(event, N, LabO=0, LabX=0, LabC=0):
        global movelist
        global rd
        global turn
        print('rd=',rd,'movelist=',movelist,'N=',N,'turn=',turn)

        m = -1
        if rd >=0:
            movelist.append(N)
            print('popop',movelist,' ',N)
            rd = rd + 1
            w = CheckWin(movelist)

            if rd < 9:
                temp = return_comp_move(movelist)
                m = temp[1]
                w = temp[0]



        if N == 'X' and rd < 0:
            LabO.config(text='Go')
            LabX.config(text='Go')
            LabC.config(text='Go')
            rd += 1
            turn = 1


        if N == 'O' and rd < 0:
            rd += 1
            turn = 0
            temp = return_comp_move(movelist)
            LabO.config(text='Go')
            LabX.config(text='Go')
            LabC.config(text='Go')

            m = temp[1]
            w = temp[0]

        r = [N, m]

        if turn%2==0:
            X = ['O', 'X']
        else:
            X = ['X', 'O']

        k=0
        for n in r:
            if k == 0:
                choice = X[0]

            else:
                choice = X[1]
            if n == 0:
                Lab0 = Label(frame0, text=choice, height=1, width=2)
                Lab0.config(font=("Courier", 50), fg='green', bg='white')
                Lab0.pack(side=LEFT)
            if n == 1:
                Lab1 = Label(frame1, text=choice, height=1, width=2)
                Lab1.config(font=("Courier", 50), fg='green', bg='black')
                Lab1.pack(side=LEFT)
            if n == 2:
                Lab2 = Label(frame2, text=choice, height=1, width=2)
                Lab2.config(font=("Courier", 50), fg='green', bg='white')
                Lab2.pack(side=LEFT)
            if n == 3:
                Lab3 = Label(frame3, text=choice, height=1, width=2)
                Lab3.config(font=("Courier", 50), fg='green', bg='black')
                Lab3.pack(side=LEFT)
            if n == 4:
                Lab4 = Label(frame4, text=choice, height=1, width=2)
                Lab4.config(font=("Courier", 50), fg='green', bg='white')
                Lab4.pack(side=LEFT)
            if n == 5:
                Lab5 = Label(frame5, text=choice, height=1, width=2)
                Lab5.config(font=("Courier", 50), fg='green', bg='black')
                Lab5.pack(side=LEFT)
            if n == 6:
                Lab6 = Label(frame6, text=choice, height=1, width=2)
                Lab6.config(font=("Courier", 50), fg='green', bg='white')
                Lab6.pack(side=LEFT)
            if n == 7:
                Lab7 = Label(frame7, text=choice, height=1, width=2)
                Lab7.config(font=("Courier", 50), fg='green', bg='black')
                Lab7.pack(side=LEFT)
            if n == 8:
                Lab8 = Label(frame8, text=choice, height=1, width=2)
                Lab8.config(font=("Courier", 50), fg='green', bg='white')
                Lab8.pack(side=LEFT)
            k = 1

    master = Tk()
    master.geometry("250x320")

    frame0 = Frame(master, height=80, width=80, bg='white')
    frame0.bind("<Button-1>", lambda event: input(event, 0))

    frame1 = Frame(master, height=80, width=80, bg='black')
    frame1.bind("<Button-1>", lambda event: input(event, 1))

    frame2 = Frame(master, height=80, width=80, bg='white')
    frame2.bind("<Button-1>", lambda event: input(event, 2))

    frame3 = Frame(master, height=80, width=80, bg='black')
    frame3.bind("<Button-1>", lambda event: input(event, 3))

    frame4 = Frame(master, height=80, width=80, bg='white')
    frame4.bind("<Button-1>", lambda event: input(event, 4))

    frame5 = Frame(master, height=80, width=80, bg='black')
    frame5.bind("<Button-1>", lambda event: input(event, 5))

    frame6 = Frame(master, height=80, width=80, bg='white')
    frame6.bind("<Button-1>", lambda event: input(event, 6))

    frame7 = Frame(master, height=80, width=80, bg='black')
    frame7.bind("<Button-1>", lambda event: input(event, 7))

    frame8 = Frame(master, height=80, width=80, bg='white')
    frame8.bind("<Button-1>", lambda event: input(event, 8))

    frame9 = Frame(master, height=60, width=80, bg='gray')


    frame10 = Frame(master, height=60, width=80, bg='gray')

    frame11 = Frame(master, height=60, width=80, bg='gray')



    frame0.grid(row=0, column=0)
    frame0.grid_propagate(0)
    frame1.grid(row=0, column=1)
    frame1.grid_propagate(0)
    frame2.grid(row=0, column=2)
    frame2.grid_propagate(0)
    frame3.grid(row=1, column=0)
    frame3.grid_propagate(0)
    frame4.grid(row=1, column=1)
    frame4.grid_propagate(0)
    frame5.grid(row=1, column=2)
    frame5.grid_propagate(0)
    frame6.grid(row=2, column=0)
    frame6.grid_propagate(0)
    frame7.grid(row=2, column=1)
    frame7.grid_propagate(0)
    frame8.grid(row=2, column=2)
    frame8.grid_propagate(0)
    frame9.grid(row=3, column=0)
    frame10.grid(row=3, column=1)
    frame11.grid(row=3, column=2)

    if rd == -1:
        o = 'O'
        x = 'X'
        orr = 'OR'
    else:
        o = 'Go'
        x = 'Go'
        orr = 'Go'

    LabO = Label(frame11, text=o, height=1, width=2)
    LabO.config(font=("Courier", 50), fg='green', bg='cyan')
    LabO.grid(row=3, column=0)
    LabO.bind("<Button-1>", lambda event: input(event, 'O', LabO, LabX, LabC))

    LabX = Label(frame9, text=x, height=1, width=2)
    LabX.config( font=("Courier", 50), fg='green', bg='cyan')
    LabX.grid(row=3, column=2)
    LabX.bind("<Button-1>", lambda event: input(event, 'X', LabO, LabX, LabC))

    LabC = Label(frame10, text=orr, height=1, width=2)
    LabC.config( font=("Courier", 50), fg='green', bg='red')
    LabC.grid(row=3, column=1)


    master.mainloop()


def return_comp_move(n):
    global movelist
    global CurrentNode
    global turn, rd

    if turn % 2 == 0:
        player = 1
        choice = 0

    else:
        player = -1
        choice = 1

    save = bestmove(CurrentNode, n, player, choice)
    CurrentNode = save[0]
    print(save[1],'=save[1]', n)
    m = save[1][turn]
    movelist.append(m)
    rd += 1
    turn = turn + 2

    w = CheckWin(movelist)
    return [w, m]


A = CreateTree(9)
initialize(A)
Minimax(A)
print('1')

y = 1
while y:
    CurrentNode = A
    turn = 1
    movelist = []
    rd = -1
    displayboard()
    y = int(input('Again?'))





# start = time.time()

# end = time.time()

# end2 = time.time()


# FOR DEBUGGING-
# -----------------
# for child in A.children:
#     if child.value == [8]:
#         break
# print('value= ', child.value, 'level= ', child.level, 'player=', child.player, 'win= ', child.win, '\n')
#
# for baby in child.children:
#     if baby.value == [8, 0]:
#         break
# print('value= ', baby.value, 'level= ', baby.level, 'player=', baby.player, 'win= ', baby.win, '\n')
# #
# for baby2 in baby.children:
#     if baby.value == [8, 0, 7]:
#         break
# print('value= ', baby2.value, 'level= ', baby2.level, 'player=', baby2.player, 'win= ', baby2.win, '\n')
# #
# for child in baby2.children:
#     if child.value == [8, 0, 7, 1]:
#         break
# print('value= ', child.value, 'level= ', child.level, 'player=', child.player, 'win= ', child.win, '\n')
# #
# for baby in child.children:
#     # if baby.value == [8, 0, 7, 1]:
#     #     break
#     print('value= ', baby.value, 'level= ', baby.level, 'player=', baby.player, 'win= ', baby.win, '\n')
#
# for child in baby.children:
#     if child.value == [1, 0, 8, 3, 6, 7]:
#         break
# print('value= ', child.value, 'level= ', child.level, 'player=', child.player, 'win= ', child.win)
# #
# for baby in child.children:
#     if baby.value == [1, 0, 8, 3, 6, 7, 2]:
#         break
# print('value= ', baby.value, 'level= ', baby.level, 'player=', baby.player, 'win= ', baby.win, '\n')
#
# for child in baby.children:
#     if child.value == [1, 0, 8, 3, 6, 7, 2, 4]:
#         break
# print('value= ', child.value, 'level= ', child.level, 'player=', child.player, 'win= ', child.win)
#
# for baby in child.children:
#     # if baby.value == [1, 0, 8, 3, 6, 7, 2]:
#     #     break
#     print('value= ', baby.value, 'level= ', baby.level, 'player=', baby.player, 'win= ', baby.win, '\n')


#PrintTree(A)
# end3 = time.time()
#
# print(count)
# print('\nCreateTree =', end - start)
# print('\nInitialize =', end2 - end)
# print('\nMinimax =', end3 - end2)

# CreateTree = 5.128087043762207 sec
#
# Initialize = 5.214020729064941 sec
#
# PrintTree = 15.634144306182861 sec


















