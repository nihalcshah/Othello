import sys; args = sys.argv[1:]
#Nihal Shah, Period 6, 2023
LIMIT_AB = 11
import random, time

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
hitctr = {'makemove':(0,0),'findmoves':(0,0), 'totaltime':(0,0), 'negamax':(0,0), 'negamax_cachehits':(0,0) , 'moveexists':[0,0]}

def display(pzl,possiblemoves=[]):
    # print(len(pzl))
    for i in possiblemoves:
        pzl = pzl[:i]+"*"+pzl[i+1:]
    for i in range(0,len(pzl),8):
        print(pzl[i:i+8])
    print()

#ORIGINAL MAKEMOVE
def makemove1(board, move, tokentoplay, moveindexes = {}):
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

#ORIGINAL FINDMOVES
def findmoves1(board, eTkn):
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
    return sorted(list(moves)), {}

#NEW MAKEMOVE
def makemove(board, move, tokentoplay, moveindexes = {}):
    global hitctr
    hitctr['moveexists'][1] += 1
    if move in moveindexes:
        hitctr['moveexists'][0] += 1
        board = board[:move]+tokentoplay+board[move+1:]
        for i in moveindexes[move]:
            board = board[:i]+tokentoplay+board[i+1:]
        return board
    else:
        tokentoplay = tokentoplay.upper()
        tokens = {*"XOox"}
        eTkn = "O" if tokentoplay == "X" else "X"
        board = board[:move]+tokentoplay+board[move+1:]
        # print(d[move])
        for constraintset in d[move]:
            inbetween = set()
            characterpos = 65
            for boardindex in constraintset:
                if board[boardindex] == tokentoplay:
                    if characterpos!=65 and inbetween and (characterpos==move or boardindex == move):
                        for i in inbetween:
                            board = board[:i]+tokentoplay+board[i+1:]
                    inbetween.clear()
                    characterpos = boardindex
                if board[boardindex] == ".":
                    inbetween.clear()
                    characterpos = 65
                if characterpos!=65 and board[boardindex] == eTkn:
                    inbetween.add(boardindex)
        return board

#NEW FINDMOVE
def findmoves(board, eTkn):
    board = board.upper()
    moveindexes = {}
    moves = []
    tokentoplay = "X" if eTkn == "O" else "O"
    for i in range(len(board)):
        if board[i] == tokentoplay:
            for constraintset in d[i]:
                leftside = set()
                setindex = constraintset.index(i)
                posindex = 65
                for index in constraintset[:setindex]:
                    if board[index] == ".":
                        posindex=index
                        leftside.clear()
                    if board[index] == tokentoplay:
                        leftside.clear()
                        posindex = 65
                    if board[index] == eTkn and posindex!=65:
                        leftside.add(index)
                if posindex!=65 and leftside:
                    moves.append(posindex)
                    if posindex in moveindexes:
                        moveindexes[posindex] = moveindexes[posindex].union(leftside)
                    else:
                        moveindexes[posindex] = leftside
                rightside = set()
                posindex = 65
                for index in constraintset[setindex+1:][::-1]:
                    if board[index] == ".":
                        posindex=index
                        rightside.clear()
                    if board[index] == tokentoplay:
                        rightside.clear()
                        posindex = 65
                    if board[index] == eTkn and posindex!=65:
                        rightside.add(index)
                if posindex!=65 and rightside:
                    moves.append(posindex)
                    if posindex in moveindexes:
                        moveindexes[posindex] = moveindexes[posindex].union(rightside)
                    else:
                        moveindexes[posindex] = rightside
    
    return sorted(set(moves)), moveindexes

def snapshot(board, tokentoplay = 0, possiblemoves=[]):
    if tokentoplay == 0:
        display(board, possiblemoves)
    display(board, possiblemoves)
    print(f'{board} {board.count("X")}/{board.count("O")}')
    if(possiblemoves):
        print(f"Possible moves for {tokentoplay.lower()}:", ", ".join([str(val) for val in possiblemoves]))
    else:
        print("No moves possible")

#Function to Parse the arguments and run Negamax or Quickmove if arguments are present.
def parseargs(args):
    global key
    board = args[0].upper()
    if not board:
        board = '.'*27+"OX......XO"+'.'*27
    tokentoplay = args[1].upper()

    etkn = ({*"XO"}-{tokentoplay}).pop()

    possiblemoves, movedict = findmoves(board, etkn)
    snapshot(board, tokentoplay, possiblemoves)
    if len(args)>2: #Make the moves
        moves = args[2]
        for move in moves:
            if int(move) == -1:
                tokentoplay = etkn
                etkn = ({*"XO"}-{tokentoplay}).pop()
                continue
            board = makemove(board, int(move), tokentoplay, movedict)
            possiblemoves, movedict = findmoves(board, etkn)
            # snapshot(board, tokentoplay, possiblemoves)
            tokentoplay = etkn
            etkn = ({*"XO"}-{tokentoplay}).pop()
    # print(quickMove(board, tokentoplay))
    snapshot(board, tokentoplay, possiblemoves)
    
    qm = quickMove(board, tokentoplay)
    print("Desired Move:", qm)
    if board.count(".")<LIMIT_AB:
        nmoutput = alphabeta(board, tokentoplay, -64,64)
        print("Min Score:", nmoutput[0], "Move sequence:", nmoutput[1])

def randomruns():
    tokentoplay = "X"
    gamevalues = {}
    t = time.process_time()
    scores = ""
    scorecounter = 0
    totalscore = 0
    totaltokens = 0
    for i in range(100):
        board = "."*27+"OX......XO"+"."*27
        transcript, pcount, ocount = rungame(board, tokentoplay)
        score = pcount-ocount
        totaltokens += pcount+ocount
        #Score Calculations
        scores += str(score)
        scorecounter += 1
        if scorecounter == 10:
            scores += "\n"
            scorecounter = 0
        else:
            scores += " "
        totalscore += score
        #Game Values
        gamevalues[score]= (transcript, i+1, tokentoplay)
        #Alternate Token
        tokentoplay = "O" if tokentoplay == "X" else "X"
        # print("Move", i+1, time.process_time() - t, "seconds")
        # print(board)
    elapsed = time.process_time() - t
    worstgames = sorted(gamevalues)[:2]
    return scores, totalscore, totaltokens, worstgames, gamevalues, elapsed

def rungame(board, token):
    initialtoken = token
    opposingtoken = "O" if token == "X" else "X"
    condensedtranscript = ""
    while board.count(".")>0:
        # print(board)
        eTkn = "O" if token == "X" else "X"
        possiblemoves, movedict = findmoves(board, eTkn)
        
        if not possiblemoves:
            token = eTkn
            eTkn = "O" if token == "X" else "X"
            possiblemoves, movedict = findmoves(board, eTkn)
            # if board.count(".")<LIMIT_NM:
            #     print(possiblemoves)
            if not possiblemoves:
                break
            else:
                condensedtranscript+="-1"
        if token == initialtoken:
            if board.count(".")>=LIMIT_AB:
                move = quickMove(board, token)
                # print("Quick Move:", move)
                if len(str(move))>1:
                    condensedtranscript+=str(move)
                else:
                    condensedtranscript+=f"_{move}"
                board = makemove(board, move, token, movedict)
                token = eTkn
            else:
                nmmove = alphabeta(board, token, -64,64)[1][-1]
                if len(str(move))>1:
                    condensedtranscript+=str(nmmove)
                else:
                    condensedtranscript+=f"_{nmmove}"
                board = makemove(board, nmmove, token, movedict)
                token = eTkn
        else: 
            move = random.choice([*possiblemoves])
            if len(str(move))>1:
                condensedtranscript+=str(move)
            else:
                condensedtranscript+=f"_{move}"
            board = makemove(board, move, token, movedict)
            token = eTkn
    return condensedtranscript, board.count(initialtoken), board.count(opposingtoken)

def negamax(board,tokentoplay):
    global cache, hitctr
    key = (board, tokentoplay)
    if key in cache:
        return (cache[key][0], [*cache[key][1]])
    if tokentoplay == "X":
        eTkn = "O"
    else:
        eTkn = "X"
    possiblemoves, movedict = findmoves(board, eTkn)
    if not possiblemoves:
        #Flips the Token
        tokentoplay = eTkn
        if tokentoplay == "X":
            eTkn = "O"
        else:
            eTkn = "X"
        possiblemoves, movedict = findmoves(board, eTkn)
        if not possiblemoves:
            res=  (board.count(eTkn)-board.count(tokentoplay), [])
            cache[key] = (res[0], [*res[1]])
            return res
        else: #If there is a pass
            move = negamax(board, tokentoplay)
            move[1].append(-1)
            res = (-1*move[0], [*move[1]])
            cache[key] = (res[0], [*res[1]])
            return res
    res = []
    for mv in possiblemoves:
        move = negamax(makemove(board,mv,tokentoplay, movedict), eTkn)
        move[1].append(mv)
        res.append((-1*move[0], [*move[1]]))
    res = max(res)
    cache[key] = (res[0], [*res[1]])
    return res

def alphabeta(board, tokentoplay, lower, upper):
    eTkn = "O" if tokentoplay == "X" else "X"
    possiblemoves, movedict = findmoves(board, eTkn)
    if not possiblemoves:
        tokentoplay = eTkn
        eTkn = "O" if tokentoplay == "X" else "X"
        possiblemoves, movedict = findmoves(board, eTkn)
        if not possiblemoves:
            return (board.count(eTkn)-board.count(tokentoplay), [])
        move = alphabeta(board, tokentoplay, -upper, -lower)
        move[1].append(-1)
        res = (-1*move[0], [*move[1]])
        return res
    best = (lower-1, [])
    for mv in possiblemoves:
        move = alphabeta(makemove(board,mv,tokentoplay, movedict), eTkn, -upper, -lower)
        score = -1*move[0]
        if score < lower: continue
        if score > upper: return (score, [mv])
        best = (score, move[1]+[mv])
        lower = score+1
    return best

def quickMove(board, token):    
    if not board:
        board = '.'*27+"OX......XO"+'.'*27
    
    tokens = {*"XO"}
    token2 = (tokens- {token.upper()}).pop()
    board = board.upper()
    possiblemoves, movedict = findmoves(board, token2.upper())
    possiblemoves = set(possiblemoves)
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
        b2 = makemove(board, move, token, movedict)
        posmoves, movedict= findmoves(b2, token)

        # posmoves = set(posmoves)-{1, 6, 8, 9, 14, 15, 48, 49, 57,54 ,55, 62}
        if len(posmoves)<minmoves:
            minmoves = len(posmoves)
            minmove = move
    return minmove

def main():
    if args:
        parseargs(args)
    else:
        scores, totalscore, totaltokens, worstgames, gamevalues, elapsed = randomruns()
        print(scores, "\n")
        print("My tokens:", totalscore,"; Total tokens:" , totaltokens)
        Score = (totalscore/totaltokens) *100
        print("Score:", Score)
        print("AB Limit:" , LIMIT_AB)
        for gamescore in worstgames:
            gamevals = gamevalues[gamescore]
            gamenumber = gamevals[1]
            transcript = gamevals[0]
            token =  gamevals[2]
            print("Game", gamenumber, "as", token, "=>", gamescore, "\n", transcript)
        print("Elapsed time:", elapsed)


if __name__ == "__main__":
    main()

#Nihal Shah, Period 6, 2023