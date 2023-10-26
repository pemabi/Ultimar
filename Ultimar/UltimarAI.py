import random
from copy import deepcopy

'''
dictionary that holds piece values - can play around with these. King set at 1000 arbitrarily as should always be highest option
'''
pieceScore = {'P': 1, 'I': 8, 'L': 5, 'C': 6, 'H': 6, 'K': 1000, 'W': 5, 'O': 3}
WIN = 10000
STALEMATE = 0
DEPTH = 2

'''
picks and returns a random move
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]  # a and b inclusive - unlike java/c# - index needs to be -1

def findGreedyMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1  # switches the max seeker from positive to negative
    opponentMinMaxScore = WIN
    bestPlayerMove = None
    for index, playerMove in enumerate(validMoves):
        moveHolder = deepcopy(playerMove)  # so that the move that will be passed thru to the engine is not affected by the moves made during AI process / stored board and pieces will not continue to change as it iterates
        gs.makeMove(moveHolder)
        opponentMoves = gs.getValidMoves()
        opponentMaxScore = -WIN
        for oppIndex, opponentMove in enumerate(opponentMoves):
            oppMoveHolder = deepcopy(opponentMove)
            gs.makeMove(oppMoveHolder)
            score = -turnMultiplier * scoreMaterial(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.logCutoff(-2)
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.logCutoff(-2) # undoes the move
    return bestPlayerMove


def findBestMove(gs, validMoves):  # helper method to make first recursive call
    global nextMove, counter
    nextMove = None
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    #counter = 0
    random.shuffle(validMoves)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -WIN, WIN, 1 if gs.whiteToMove else -1)
    #print(counter)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove  
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -WIN
        for move in validMoves:
            #moveHolder = deepcopy(move)
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)  # recursive - goes into next turn with gs, new set of valid moves, one level less depth, and opposite bool as was called in this instance
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:  # ensures move being recorded is only a move that is immediately available to be made
                    nextMove = move
            gs.logCutoff(-2)  # returns gamestate to initial state
        return maxScore
    else:
        minScore = WIN
        for move in validMoves:
            #moveHolder = deepcopy(move)
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:  # same logic as above, but minimizing score
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.logCutoff(-2)
        return minScore
    

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    #counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -WIN
    for move in validMoves:
        moveHolder = deepcopy(move)
        gs.makeMove(moveHolder)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.logCutoff(-2)
    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):  # AB pruning takes branch count of white's first move down from 977 to 94 @depth 2 and 93,379 to 2,360 @depth3 (naive scoring algorithm)
    global nextMove, counter
    #counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    # move ordering - evaluate certain moves first paired with AB pruning to improve efficiency - can implement later
    maxScore = -WIN
    for move in validMoves:
        moveHolder = deepcopy(move)
        gs.makeMove(moveHolder)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.logCutoff(-2)
        if maxScore > alpha:  # pruning
            alpha = maxScore
        if alpha >= beta:  # break case - no need to evaluate rest of tree
            break
    return maxScore

'''
positive score is good for white, negative good for black
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return WIN
        else:
            return -WIN
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square and square[0] == 'w':
                score += pieceScore[square[1]]
                if square[4]:
                    score -= (pieceScore[square[1]] / 2)  # subtracts half of immobilised pieces score
                if square[2]:
                    score -= (pieceScore[square[1]] / 4)
            elif square and square[0] == 'b':
                score -= pieceScore[square[1]]
                if square[4]:
                    score += (pieceScore[square[1]] / 2)
                if square[2]:
                    score += (pieceScore[square[1]] / 4)
    return score

'''
Score board based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square and square[0] == 'w':
                score += pieceScore[square[1]]
                if square[4]:
                    score -= (pieceScore[square[1]] / 2)  # subtracts half of immobilised pieces score
                if square[2]:
                    score -= (pieceScore[square[1]] / 2)
            elif square and square[0] == 'b':
                score -= pieceScore[square[1]]
                if square[4]:
                    score += (pieceScore[square[1]] / 2)
                if square[2]:
                    score += (pieceScore[square[1]] / 2)
    return score
