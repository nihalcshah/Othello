import sys; args = sys.argv[1:]
# args = ['.'*27+"OX......XO"+'.'*27, 'O' ]
# args = ["..................x.o.....ooxx...ooxxx.....ox.......o..........."]
# args = ["..................OOO.....OOO.....OXO......X...................."]
def display(pzl,possiblemoves):
    # print(len(pzl))
    for i in possiblemoves:
        pzl = pzl[:i]+"*"+pzl[i+1:]
    for i in range(0,len(pzl),8):
        print(pzl[i:i+8])

def findmoves(board, tokentofindmovesplay):
    constraints, d = findsets()
    moves = set()
    tokens = {*"XOox"}
    for i in range(len(board)):
        if board[i].lower() == tokentofindmovesplay.lower():
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
    # return sorted(list(moves))
    return moves


def findsets():
    rows = [[j*8+i for i in range(8)] for j in range(8)]
    columns = [[j+i*8 for i in range(8)] for j in range(8)]
    rowdiagonals = [[j for j in range(i, 64, 9)][:8-i] for i in range(8)]
    coldiagonals = [[j for j in range(i, 64, 9)] for i in columns[0][1:]]
    reversedcoldiagonals = [[j for j in range(i,-1, -7)] for i in columns[0][::-1]]
    reversedrowdiagonals = [[j for j in range(i,-1, -7)][:8-(i%8)] for i in rows[-1][1:]]
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
    # print(d[17])
    return constraints, d

# base = '.'*27+"OX......XO"+'.'*27
# moves = findmoves(base, 'O')
# display(base, moves)
# print(moves)
def parseargs(args):
    newargs = args
    board = ""
    possiblemoves = []
    tokens = {*"XOox"}
    digits = {*"0123456789"}
    tokentoplay = ""
    if len(newargs) <=3:
        for arg in newargs:
            if len(arg)==64:
                board = arg.upper()
            if arg in tokens:
                tokentoplay = arg
            k = {*arg}.union(digits)
            if len(k)>0:
                possiblemoves.append(arg)
    if not board:
        board = '.'*27+"OX......XO"+'.'*27
    display(board, [])
    if not tokentoplay:
        xcount = board.count('X')
        ocount = board.count('O')
        if xcount<=ocount:
            tokentoplay = 'X'
        else:
            tokentoplay = 'O'
    if not possiblemoves:
        if tokentoplay.upper() == 'X':
            possiblemoves = findmoves(board, 'O')
        else:
            possiblemoves = findmoves(board, 'X')
    # display(board, possiblemoves)
    # if(possiblemoves):
    #     print("Possible moves for x:", ", ".join([str(val) for val in possiblemoves]))
    # else:
    #     print("No moves possible")
    if possiblemoves:
        print(possiblemoves)
    else:
        print("No moves possible")
    # return board, tokentoplay, possiblemoves
parseargs(args)
#Nihal Shah, Period 6, 2023