import sys; args = sys.argv[1:]
# args = ['44']
# args = "..................x.o.....ooxx..xxxxxx.....ox.......o........... b2".split(" ")
# args = "xxxxxx..xxxoo.o.xxoxooo.xxooooo.xxoooooxx.o.ooox.oo.ooox..o.xxx. x 51".split(" ")
# args = ".x........x.ox.o...ox.o.x.oxox...oxxo.x.ooxooooo.x.x.o..x.ox.o.. o 4".split(" ")
#Othello
#Nihal Shah

def findsets():
    rows = [[j*8+i for i in range(8)] for j in range(8)]
    columns = [[j+i*8 for i in range(8)] for j in range(8)]
    rowdiagonals = [[j for j in range(i, 64, 9)][:8-i] for i in range(8)]
    coldiagonals = [[j for j in range(i, 64, 9)] for i in columns[0][1:]]
    reversedcoldiagonals = [[j for j in range(i,0, -7)] for i in columns[0][::-1]]
    reversedrowdiagonals = [[j for j in range(i,0, -7)][:8-(i%8)] for i in rows[-1][1:]]
    constraints = [rows, columns, rowdiagonals, coldiagonals, reversedcoldiagonals, reversedrowdiagonals]
    d = {}
    for i in range(64):
        for s in constraints:
            for line in s:
                sl = set(line)
                if i in sl:
                    if i not in d:
                        d[i] = [line]
                    else:
                        d[i].append(line)
    # print(d[57])
    return constraints, d

global d, constraints
constraints, d = findsets()

def display(pzl,possiblemoves):
    # print(len(pzl))
    for i in possiblemoves:
        pzl = pzl[:i]+"*"+pzl[i+1:]
    for i in range(0,len(pzl),8):
        print(pzl[i:i+8])
    print()

def makemove(board, move, tokentoplay):
    tokentoplay = tokentoplay.upper()
    tokens = {*"XOox"}
    for s in d[move]:
        ind = s.index(move)
        k = 0
        top = False
        oppositecount = 0
        visitedcount = 0
        while ind+k< len(s) and (board[s[ind+k]] in tokens or k==0):
            if board[s[ind+k]] == tokentoplay:
                if visitedcount>1:
                    oppositecount += 1
                    top = True
                break
            k += 1
            visitedcount += 1
        m = 0
        visitedcount = 0
        while ind-m>=0 and (board[s[ind-m]] in tokens or m == 0):
            if board[s[ind-m]] ==tokentoplay:
                if visitedcount>1:
                    oppositecount += 1
                break
            m += 1
            visitedcount += 1
        if not top and oppositecount==1 and ind-m>=0 and m>1:
            it = ind-1
            while it!=ind-m:
                board = board[:s[it]]+tokentoplay+board[s[it]+1:]
                it -= 1
        elif oppositecount==1 and top and ind+k<len(s):
            it = ind+1
            while it<=ind+k:
                board = board[:s[it]]+tokentoplay+board[s[it]+1:]
                it += 1
    board = board = board[:move]+tokentoplay+board[move+1:]
    return board

def findmoves(board, tokentofindmovesplay):
    
    moves = set()
    tokens = {*"XOox"}
    for i in range(len(board)):
    
        if board[i].upper() == tokentofindmovesplay.upper():
            for s in d[i]:
                ind = s.index(i)
                k = 0
                top = False
                oppositecount = 0
                while ind+k< len(s) and board[s[ind+k]] in tokens:
                    
                    if board[s[ind+k]] != tokentofindmovesplay:
                        oppositecount += 1
                        top = True
                        break
                    k += 1
                m = 0
                while ind-m>=0 and board[s[ind-m]] in tokens:
                    if board[s[ind-m]] != tokentofindmovesplay:
                        oppositecount += 1
                        break
                    m += 1
                if top and oppositecount<2 and ind-m>=0:
                    moves.add(s[ind-m])
                elif oppositecount==1 and not top and ind+k<len(s):
                    moves.add(s[ind+k])
    return sorted(list(moves))

def parseargs(args):    
    newargs = args
    board = ""
    accmoves = []
    possiblemoves = []
    tokens = {*"XOox"}
    digits = {*"0123456789"}
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tokentoplay = ""
    if len(newargs) <=3:
        for arg in newargs:
            if len(arg)==64:
                board = arg.upper()
            if arg in tokens:
                tokentoplay = arg
            k = {*arg}.intersection(digits)
            if len(k)>0:
                if arg[0].upper() in alpha:
                    accmoves.append(alpha.index(arg[0].upper())+((int(arg[1])-1)*8))
                else:
                    accmoves.append(int(arg))

    if not board:
        board = '.'*27+"OX......XO"+'.'*27
    board = board.upper()
    
    
    if not tokentoplay:
        xcount = board.count('X')
        ocount = board.count('O')
        if xcount<=ocount:
            tokentoplay = 'X'
            possiblemoves = findmoves(board, "O")
            if not possiblemoves:
                tokentoplay = 'O'
                possiblemoves = findmoves(board, "X")
        else:
            tokentoplay = 'O'
            possiblemoves = findmoves(board, "X")
            if not possiblemoves:
                tokentoplay = 'X'
                possiblemoves = findmoves(board, "O")
    if not possiblemoves:
        if tokentoplay.upper() == 'X':
            possiblemoves = findmoves(board, 'O')
        else:
            possiblemoves = findmoves(board, 'X')
    display(board, possiblemoves)
    print(f'{board} {board.count("X")}/{board.count("O")}')
    if(possiblemoves):
        print("Possible moves for x:", ", ".join([str(val) for val in possiblemoves]))
    else:
        print("No moves possible")
    if not accmoves:
        accmoves = possiblemoves
    if not accmoves:
        return
    # makemove(board, possiblemoves[0], tokentoplay)
    board = makemove(board, accmoves[0], tokentoplay)
    print(tokentoplay.lower(), "plays to", accmoves[0])
    display(board, [])
    print(f'{board} {board.count("X")}/{board.count("O")}')
    possiblemoves = findmoves(board,tokentoplay.upper())
    if(possiblemoves):
        print("Possible moves for x:", ", ".join([str(val) for val in possiblemoves]))
    else:
        print("No moves possible")
    # jkl = makemove(board, 57, tokentoplay)
    # display(jkl, [])
parseargs(args)
#Nihal Shah, Period 6, 2023