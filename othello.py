import sys; args = sys.argv[1:]
import time
#Othello
#Nihal Shah, Period 6, 2023

# args = "oxxoooooxxxxooooxxooxoo..xxoxxo.xxxxoxxxxxxoxoxo.xoooxoox..ox.xo o".split(" ")

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
global cache
cache = {}
global hitctr
hitctr = {'makemove':(0,0),'findmoves':(0,0), 'totaltime':(0,0), 'negamax':(0,0), 'negamax_cachehits':(0,0)}


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
        bottom = False
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
                    bottom = True
                    oppositecount += 1
                break
            m += 1
            visitedcount += 1
        if top and bottom:
            it = ind-1
            while it!=ind-m:
                board = board[:s[it]]+tokentoplay+board[s[it]+1:]
                it -= 1
            it = ind+1
            while it<=ind+k:
                board = board[:s[it]]+tokentoplay+board[s[it]+1:]
                it += 1
        else:
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

#
def findmoves(board, eTkn):
    moves = set()
    tokens = {*"XOox"}
    for i in range(len(board)):
        if board[i].upper() == eTkn.upper():
            for s in d[i]:
                ind = s.index(i)
                k = 0
                top = False
                oppositecount = 0
                while ind+k< len(s) and board[s[ind+k]] in tokens:
                    
                    if board[s[ind+k]] != eTkn:
                        oppositecount += 1
                        top = True
                        break
                    k += 1
                m = 0
                while ind-m>=0 and board[s[ind-m]] in tokens:
                    if board[s[ind-m]] != eTkn:
                        oppositecount += 1
                        break
                    m += 1
                if top and oppositecount<2 and ind-m>=0:
                    moves.add(s[ind-m])
                elif oppositecount==1 and not top and ind+k<len(s):
                    moves.add(s[ind+k])
    return sorted(list(moves))

def snapshot(board, tokentoplay = 0, possiblemoves=[]):
    if tokentoplay == 0:
        display(board, possiblemoves)
    display(board, possiblemoves)
    print(f'{board} {board.count("X")}/{board.count("O")}')
    if(possiblemoves):
        print(f"Possible moves for {tokentoplay.lower()}:", ", ".join([str(val) for val in possiblemoves]))
    else:
        print("No moves possible")

#Function to Parse the arguments.
def parseargs(args):
    global hitctr
    board = args[0].upper()
    if not board:
        board = '.'*27+"OX......XO"+'.'*27
    tokentoplay = args[1].upper()

    etkn = ({*"XO"}-{tokentoplay}).pop()

    possiblemoves = findmoves(board, etkn)
    snapshot(board, tokentoplay, possiblemoves)
    if len(args)>2: #Make the moves
        for move in args[2:]:
            if int(move) == -1:
                tokentoplay = etkn
                etkn = ({*"XO"}-{tokentoplay}).pop()
                continue
            board = makemove(board, int(move), tokentoplay)
            possiblemoves = findmoves(board, etkn)
            snapshot(board, tokentoplay, possiblemoves)
            tokentoplay = etkn
            etkn = ({*"XO"}-{tokentoplay}).pop()
    # print(quickMove(board, tokentoplay))
    snapshot(board, tokentoplay, possiblemoves)
    
    qm = quickMove(board, tokentoplay)
    print("Desired Move:", qm)
    t = time.process_time()
    nmoutput = negamax(board, tokentoplay)
    t = time.process_time()-t
    hitctr['negamax'] = (hitctr['negamax'][0]+1, hitctr['negamax'][1]+t)
    # nmoutput = nmoutput[0]
    print("Min Score:", nmoutput[0], "Move sequence:", nmoutput[1])
    # print(quickMove(board, tokentoplay))


#Dated Method meant for Othello 3 and 4
def parseargs2(args):
    board = ""
    if not board:
        board = '.'*27+"OX......XO"+'.'*27
    board = board.upper()
    tokentoplay = "x"
    display(board, [])
    print(f'{board} {board.count("X")}/{board.count("O")}')
    accmoves = args[0]
    accmoves = [int(accmoves[k:k+2].replace("_", "")) for k in range(0,len(accmoves),2) if int(accmoves[k:k+2].replace("_", ""))>=0]
    # accmoves = [accmoves[i:i+2] for i in range(0, len(accmoves), 2) if accmoves[i:i+2]!="-1"]
    for move in accmoves:
        # if "_" in move:
        #     tokentoplay = ({*'XO'}-{tokentoplay.upper()}).pop()
        #     continue
        # move = int(move)
        board = makemove(board, move, tokentoplay)
        print(tokentoplay.lower(), "plays to", move)
        display(board, [])
        print(f'{board} {board.count("X")}/{board.count("O")}')
        possiblemoves = findmoves(board,tokentoplay.upper())

        tokentoplay = ({*'XO'}-{tokentoplay.upper()}).pop()
        if(possiblemoves):
            print(f"Possible moves for {tokentoplay.lower()}:", ", ".join([str(val) for val in possiblemoves]))
        else:
            possiblemoves = findmoves(board,tokentoplay.upper())
            tokentoplay = ({*'XO'}-{tokentoplay.upper()}).pop()
            if(possiblemoves):
                print(f"Possible moves for {tokentoplay.lower()}:", ", ".join([str(val) for val in possiblemoves]))
            else:
                print("No moves possible")
                return

def negamax(board,tokentoplay):
    global cache, hitctr
    key = (board, tokentoplay)
    if key in cache:
        return (cache[key][0], [*cache[key][1]])
    # eTkn = ({*"XO"}-{tokentoplay}).pop()
    if tokentoplay == "X":
        eTkn = "O"
    else:
        eTkn = "X"
    t = time.process_time() 
    possiblemoves = findmoves(board, eTkn)
    t = time.process_time() - t
    hitctr["findmoves"] = (hitctr["findmoves"][0]+1, hitctr["findmoves"][1]+t)
    if not possiblemoves:
        #Flips the Token
        tokentoplay = eTkn
        # eTkn = ({*"XO"}-{tokentoplay}).pop()
        if tokentoplay == "X":
            eTkn = "O"
        else:
            eTkn = "X"
        possiblemoves = findmoves(board, eTkn)
        if not possiblemoves:
            res=  (board.count(eTkn)-board.count(tokentoplay), [])
            cache[key] = (res[0], [*res[1]])
            return res
        else: #If there is a pass
            # res = []
            move = negamax(board, tokentoplay)
            # for move in nm:
            move[1].append(-1)
            # res.append((-1*move[0], move[1]))
            res = (-1*move[0], [*move[1]])
            cache[key] = (res[0], [*res[1]])
            # res=[max(res)
            return res
    res = []
    for mv in possiblemoves:
        move = negamax(makemove(board,mv,tokentoplay), eTkn)
        
        move[1].append(mv)
        res.append((-1*move[0], [*move[1]]))
    res = max(res)
    cache[key] = (res[0], [*res[1]])
    return res

def quickMove(board, token):    
    if not board:
        board = '.'*27+"OX......XO"+'.'*27
    
    tokens = {*"XO"}
    token2 = (tokens- {token.upper()}).pop()
    board = board.upper()
    possiblemoves = set(findmoves(board, token2.upper()))
    # print("move:",possiblemoves)
    for move in possiblemoves:
        if move in {0, 7, 56, 63}:
            return move
    for move in possiblemoves:
        # if move in {1, 6, 8, 9, 14, 15, 48, 49, 57,54 ,55, 62}:
        if move == 1 or move == 8 or move ==9:
            if board[0].upper() == token.upper():
                return move
        if move == 6 or move == 15 or move== 14:
            if board[7].upper() == token.upper():
                return move
        if move == 48 or move == 57 or move == 49:
            if board[56].upper() == token.upper():
                return move
        if move == 54 or move == 62 or move == 55:
            if board[63].upper() == token.upper():
                return move
    cxpieces = {1, 6, 8, 9, 14, 15, 48, 49, 57,54 ,55, 62}
    minmoves = 1000
    minmove = 0
    rowsstart = set(constraints[0][0])
    rowsend = set(constraints[0][-1])
    colsstart = set(constraints[1][0])
    colsend = set(constraints[1][-1])
    if (possiblemoves - cxpieces):
        possiblemoves -= cxpieces
    for move in possiblemoves:
        if move in rowsstart or move in rowsend or move in colsstart or move in colsend:
            return move
    for move in possiblemoves:
        b2 = makemove(board, move, token)
        posmoves = findmoves(b2, token)

        # posmoves = set(posmoves)-{1, 6, 8, 9, 14, 15, 48, 49, 57,54 ,55, 62}
        if len(posmoves)<minmoves:
            minmoves = len(posmoves)
            minmove = move
    return minmove
def main():
    parseargs(args)
    print(hitctr["findmoves"])
    print(hitctr["negamax"])
    # print(hitctr["negamax"])
    # print(hitctr["negamax_cachehits"])
    # pass
if __name__ == "__main__":
    main()
    # drawargs(sys.argv[1:])
    # parseargs(args)

#Nihal Shah, Period 6, 2023
