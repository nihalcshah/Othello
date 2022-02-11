import sys;args = sys.argv[1:]
#Nihal Shah, Period 6, 2023
LIMIT_AB = 11
MG_UPPER_LIMIT_AB = 45
MG_LOWER_LIMIT_AB = 40
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
global movecache
movecache = {}
global hitctr
# print(constraints)
hitctr = {'movescache':0,'findmoves':(0,0), 'findmovestime':0, 'totaltime':0, 'makemovetime':0}

def display(pzl,possiblemoves=[]):
    # print(len(pzl))
    for i in possiblemoves:
        pzl = pzl[:i]+"*"+pzl[i+1:]
    for i in range(0,len(pzl),8):
        print(pzl[i:i+8])
    print()
#NEW MAKEMOVE
def makemove(board, move, tokentoplay, moveindexes = {}):
    global hitctr
    t = time.process_time()
    if move in moveindexes:
        board = board[:move]+tokentoplay+board[move+1:]
        for i in moveindexes[move]:
            board = board[:i]+tokentoplay+board[i+1:]
        hitctr['makemovetime'] += time.process_time()-t
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
        hitctr['makemovetime'] += time.process_time()-t
        return board

def findmoves(board, tokentoplay):
    global hitctr, movecache
    t = time.process_time()
    board = board.upper()
    moveindexes = {}
    moves = set()
    csnames = {}
    key = (board, tokentoplay)
    # if key in movecache:
    #     return movecache[key][0], movecache[key][1]
    eTkn = "X" if tokentoplay == "O" else "O"
    for i in range(len(board)):
        if board[i] == ".":
            for constraintset in d[i]:
                # key = (0, [*constraintset]))
                setstr = "".join([str(val) for val in constraintset])
                if setstr in csnames:
                    continue
                else:
                    csnames[setstr] = 1
                inbetween = set()
                tknindex = 65
                tknmarked = " "
                setstr = ""
                for setindex, boardindex in enumerate(constraintset):
                    # setstr += f"{boardindex}"
                    if boardindex == 54:
                        store =1
                    if (board[boardindex] == tokentoplay or board[boardindex] == "."):
                        if tknindex!=65:
                            if board[boardindex]!=tknmarked and inbetween:
                                if boardindex ==7:
                                    store = 0
                                if tknmarked == ".":
                                    moves.add(tknindex)
                                    if tknindex in moveindexes:
                                        moveindexes[tknindex] = moveindexes[tknindex].union(inbetween)
                                    else:
                                        moveindexes[tknindex] = {*inbetween}
                                else:
                                    moves.add(boardindex)
                                    if boardindex in moveindexes:
                                        moveindexes[boardindex] = moveindexes[boardindex].union(inbetween)
                                    else:
                                        moveindexes[boardindex] = {*inbetween}
                            inbetween.clear()
                        tknindex = boardindex
                        tknmarked = board[boardindex]
                    else:
                        if tknindex!=65:
                            inbetween.add(boardindex)
                # csnames[setstr] = 1
    hitctr['findmovestime'] += time.process_time()-t
    val = (sorted(list({*moves})), moveindexes.copy())
    movecache[key] = val
    return sorted(list({*moves})), moveindexes

def snapshot(board, tokentoplay = 0, possiblemoves=[]):
    if tokentoplay == 0:
        display(board, possiblemoves)
    display(board, possiblemoves)
    print(f'{board} {board.count("X")}/{board.count("O")}')
    if(possiblemoves):
        print(f"Possible moves for {tokentoplay.lower()}:", ", ".join([str(val) for val in possiblemoves]))
    else:
        print("No moves possible")

def parseargs(args):
    moves = []
    tokentoplay = ""
    board = ""
    condensedmoves = ""
    for arg in args:
        if len(arg) == 1:
            tokentoplay = arg.upper()
        elif len(arg)<=3:
            moves.append(int(arg))
        elif len({*arg})<=3:
            board = arg.upper()
        else: 
            condensedmoves = arg
    if not board:
        board = '.'*27+"OX......XO"+'.'*27
    if not tokentoplay:
        xcount = board.count('X')
        ocount = board.count('O')
        if xcount<=ocount:
            tokentoplay = 'X'
            possiblemoves, movedict = findmoves(board, 'X')
            if not possiblemoves or (xcount+ocount)%2!=0:
                tokentoplay = 'O'
                possiblemoves, movedict = findmoves(board, "O")
        else:
            tokentoplay = 'O'
            possiblemoves, movedict = findmoves(board, "O")
            if not possiblemoves:
                tokentoplay = 'X'
    
    return board, tokentoplay, moves, condensedmoves

def mgalphabeta(board, tokentoplay, lower, upper):
    eTkn = "O" if tokentoplay == "X" else "X"
    possiblemoves, movedict = findmoves(board, tokentoplay)
    if not possiblemoves:
        tokentoplay = eTkn
        eTkn = "O" if tokentoplay == "X" else "X"
        possiblemoves, movedict = findmoves(board, tokentoplay)
        if not possiblemoves:
            score = (0)
            return (board.count(eTkn)-board.count(tokentoplay), [])
        move = mgalphabeta(board, tokentoplay, -upper, -lower)
        move[1].append(-1)
        res = (-1*move[0], [*move[1]])
        return res
    best = (lower-1, [])
    for mv in possiblemoves:
        move = mgalphabeta(makemove(board,mv,tokentoplay, movedict), eTkn, -upper, -lower)
        score = -1*move[0]
        if score < lower: continue
        if score > upper: return (score, [mv])
        best = (score, move[1]+[mv])
        lower = score+1
    return best
#Function to Parse the arguments and run Negamax or Quickmove if arguments are present.
def givenargs(args):
    board, tokentoplay, moves, condensedmoves = parseargs(args)
    etkn = "O" if tokentoplay == "X" else "X"
    possiblemoves, movedict = findmoves(board, tokentoplay)
    snapshot(board, tokentoplay, possiblemoves)
    # if len(args)>2: #Make the moves
    if condensedmoves:
        accmoves = condensedmoves
        moves = [int(accmoves[k:k+2].replace("_", "")) for k in range(0,len(accmoves),2) if int(accmoves[k:k+2].replace("_", ""))>=0]
    for move in moves:
        if int(move) <0:
            tokentoplay = etkn
            etkn = ({*"XO"}-{tokentoplay}).pop()
            continue
        if move == 52:
            st = 1
        board = makemove(board, int(move), tokentoplay, movedict)
        # print()
        print(tokentoplay, "plays to", move)
        tokentoplay = etkn
        etkn = 'O' if tokentoplay == 'X' else 'X'
        possiblemoves, movedict = findmoves(board, tokentoplay)
        # tokentoplay = etkn
        snapshot(board, tokentoplay, possiblemoves)
        print()
    # print(quickMove(board, tokentoplay))
    
    qm = quickMove(board, tokentoplay)
    print("My Preferred Move is", qm)
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
    scoresby10 = ""
    for i in range(100):
        board = "."*27+"OX......XO"+"."*27
        transcript, pcount, ocount = rungame(board, tokentoplay)
        score = pcount-ocount
        totaltokens += pcount+ocount
        #Score Calculations
        if len(str(score))>1:
            scoresby10 += str(score)
        else:
            scoresby10 += " "+str(score)
        scorecounter += 1
        if scorecounter == 10:
            print(scoresby10)
            # scores += scoresby10 +"\n"
            scoresby10 = ""
            scorecounter = 0
        else:
            scoresby10 += " "
        # totalscore += score
        totalscore += pcount
        #Game Values
        gamevalues[score]= (transcript, i+1, tokentoplay)
        #Alternate Token
        tokentoplay = "O" if tokentoplay == "X" else "X"
        # print("Move", i+1, time.process_time() - t, "seconds")
        # print(board)
    elapsed = time.process_time() - t
    worstgames = sorted(gamevalues)[:2]
    return totalscore, totaltokens, worstgames, gamevalues, elapsed

def rungame(board, token):
    initialtoken = token
    opposingtoken = "O" if token == "X" else "X"
    condensedtranscript = ""
    if initialtoken != "X":
        possiblemoves = [19, 26, 37, 44]
        movedict = {19: {27}, 44: {36}, 26: {27}, 37: {36}}
        move = random.choice([*possiblemoves])
        if len(str(move))>1:
            condensedtranscript+=str(move)
        else:
            condensedtranscript+=f"_{move}"
        board = makemove(board, move, opposingtoken, movedict)
    while board.count(".")>0:
        # print(board)
        eTkn = "O" if token == "X" else "X"
        possiblemoves, movedict = findmoves(board, token)
        # print(possiblemoves)
        if not possiblemoves:
            # print("hi")
            token = eTkn
            eTkn = "O" if token == "X" else "X"
            possiblemoves, movedict = findmoves(board, token)
            if not possiblemoves:
                break
            else:
                condensedtranscript+="-1"
        if token == initialtoken:
            if board.count(".")<MG_UPPER_LIMIT_AB and board.count(".")>MG_LOWER_LIMIT_AB:
                nmmove = mgalphabeta(board, token, -64,64)[1][-1]
                # nmmove = negamax(board, token)[1][-1]
                if len(str(nmmove))>1:
                    condensedtranscript+=str(nmmove)
                else:
                    condensedtranscript+=f"_{nmmove}"
                board = makemove(board, nmmove, token, movedict)
                token = eTkn
            elif board.count(".")>=MG_UPPER_LIMIT_AB or (board.count(".")<=MG_LOWER_LIMIT_AB and board.count(".")>LIMIT_AB):
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
                # nmmove = negamax(board, token)[1][-1]
                if len(str(nmmove))>1:
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
    possiblemoves, movedict = findmoves(board, tokentoplay)
    if not possiblemoves:
        #Flips the Token
        tokentoplay = eTkn
        if tokentoplay == "X":
            eTkn = "O"
        else:
            eTkn = "X"
        possiblemoves, movedict = findmoves(board, tokentoplay)
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
    possiblemoves, movedict = findmoves(board, tokentoplay)
    if not possiblemoves:
        tokentoplay = eTkn
        eTkn = "O" if tokentoplay == "X" else "X"
        possiblemoves, movedict = findmoves(board, tokentoplay)
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
    possiblemoves, movedict = findmoves(board, token.upper())
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
    # for move in possiblemoves:
    #     b2 = makemove(board, move, token, movedict)
    #     posmoves, movedict= findmoves(b2, token)

    #     # posmoves = set(posmoves)-{1, 6, 8, 9, 14, 15, 48, 49, 57,54 ,55, 62}
    #     if len(posmoves)<minmoves:
    #         minmoves = len(posmoves)
    #         minmove = move
    # return minmove
    if possiblemoves:
        return possiblemoves.pop()

def collectstats():
    global LIMIT_AB
    times = ""
    scores = ""
    for i in range(12):
        totalscore, totaltokens, worstgames, gamevalues, elapsed = randomruns()
        print("My tokens:", totalscore,"; Total tokens:" , totaltokens)
        print("AB Limit:" , LIMIT_AB)
        Score = (totalscore/totaltokens) *100
        times += f"{elapsed:.1f} "
        scores += f"{Score:.1f} "
        print(f"{Score:.1f}")
        print(f"{elapsed:.1f}")
        LIMIT_AB +=1
    print(times)
    print(scores)

def main():
    # collectstats()
    if args:
        givenargs(args)
    else:
        totalscore, totaltokens, worstgames, gamevalues, elapsed = randomruns()
        print("My tokens:", totalscore,"; Total tokens:" , totaltokens)
        Score = (totalscore/totaltokens) *100
        print("Score:", f"{Score:.1f}%")
        print("NM/AB Limit:" , LIMIT_AB)
        for gamescore in worstgames:
            gamevals = gamevalues[gamescore]
            gamenumber = gamevals[1]
            transcript = gamevals[0]
            token =  gamevals[2]
            print("Game", gamenumber, "as", token, "=>", gamescore, "\n", transcript)
        print("Elapsed time:", f"{elapsed:.1f}s")
    print(hitctr["movescache"])
if __name__ == "__main__":
    main()

#Nihal Shah, Period 6, 2023