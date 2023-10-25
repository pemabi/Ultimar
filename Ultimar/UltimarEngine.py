#Class is responsible for storing infor about current gamestate, determining valid moves, finding attacking moves, and keeping game log
'''Idea here is that this focuses on simply mechanics,  and creates a very accurate snapshot of the board includiong conditions. The AI will work
by moving 'forward' one move and examining the difference in snapshots to determine best move
Question of 'attacking potential is interesting as that takes it away from 'greedy' level. possible to do this later? I think this can be modular enough to 
do entirely from the AI level - that's the poiht of remvoing all the arrays etc and using this 'snapshot' board approach - modular and easily analysed in a vacuum
'''


from copy import deepcopy

vectors = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
borders = ((-1, 0), (0, 1), (1, 0), (0, -1))
pieces = ['P', 'O', 'L', 'C', 'W', 'K', 'H', 'I']
boardSelect = True

class GameState():
    def __init__(self):

        '''
        ['b', 'C', False, ['iC', 'iC', 'iC', 'iC'], ['i', 'i']]
        new : [0: color][1: piecetype][2: withdrawn log][3: acitng as Immob][4: immobilisedLog]
        '''
        if boardSelect:
            self.board = [
            [["b", "O", False, False, []], ["b", "L", False, False, []], ["b", "C", False, [], []], ["b", "W", False, False, []], 
                ["b", "K", False, False, []], ["b", "H", False, [], []], ["b", "L", False, False, []], ["b", "I", False, [('I')], []]],
            [["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], 
                ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []]],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], 
                ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []]],
            [["w", "I", False, [('i')], []], ["w", "L", False, False, []], ["w", "C", False, [], []], ["w", "W", False, False, []], 
                ["w", "K", False, False, []], ["w", "H", False, [], []], ["w", "L", False, False, []], ["w", "O", False, False, []]]]
        else:
            self.board = flippedBoard

        self.moveFunctions = {'P': self.getPawnMoves, 'I': self.getImmobiliserMoves, 'L': self.getLeaperMoves,
                              'C': self.getChameleonMoves, 'H': self.getChameleonMoves, 'K': self.getKingMoves,
                              'W': self.getWithdrawerMoves, 'O': self.getCoordinatorMoves}
   
        self.attackFunctions = {'P': self.getPawnAttacks, 'W': self.getWithdrawerAttacks,
                            'I': self.getImmobiliserAttacks, 'K': self.getKingAttacks, 'L': self.getLeaperAttacks,
                            'C': self.getChameleonAttacks, 'H': self.getChameleonAttacks,
                            'O': self.getCoordinatorAttacks}
        
        self.immobilisingPieces = {'wI': 'i', 'wC': 'c', 'wH': 'h', 'bI': 'I', 'bC': 'C', 'bH': 'H'}

        self.whiteToMove = True
        self.moveLog = []
        self.gameLog = [deepcopy(self.board)]

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.checkmate = False
        self.stalemate = False

        self.counter = 0
        
    def logCutoff(self, desiredIndex):
        self.gameLog = self.gameLog[:(desiredIndex+1)]
        self.moveLog = self.moveLog[:(desiredIndex+1)]
        if len(self.gameLog) % 2 == 0:
            self.whiteToMove = False
        else:
            self.whiteToMove = True
        self.board = deepcopy(self.gameLog[-1])
        self.checkmate = False
        self.stalemate = False
        self.counter = self.counter + 1

    def makeMove(self, move):
        self.resetWithdrawer(move.startRow, move.startCol, move.pieceColor + move.pieceType)
        self.immobiliserCaller(move.startRow, move.startCol, move.pieceMoved)
        self.board[move.startRow][move.startCol] = []  # sets the start sq blank
        self.getAttacks(move)  # looks for any attacks made during move
        self.board[move.endRow][move.endCol] = move.pieceMoved  # sets the end square equal to the moved piece
        self.withdrawnMovedPiece(move.endRow, move.endCol)  # resets withdrawn flag for piecemoved
        self.moveLog.append(move)
        self.gameLog.append(deepcopy(self.board))  # adds a deep copy of board to the gamelog
        self.whiteToMove = not self.whiteToMove  # switch turn Bool

    def getKingLocations(self, r, c):
        if self.board[r][c] and self.board[r][c][1] == 'K':
            if self.board[r][c][0] == 'w':
                self.whiteKingLocation = (r, c)  # can put something in here ensure king is on board, pass this back to trigger checkmate
            else:
                self.blackKingLocation = (r, c)

    def getValidMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):  # while iterating through the board, update King locations. putting this first means coordinator attacks will still work after moving through gamelog
                self.getKingLocations(r, c)
                if self.board[r][c] and self.isAlly(r, c) and not self.board[r][c][4]:
                        piece = self.board[r][c][1]
                        self.moveFunctions[piece](r, c, moves)  # calls move type based on piece type
        if not moves:
            self.stalemate = True
        return moves

    def getAttacks(self, move):
        attacks = []
        r = move.endRow
        c = move.endCol
        self.attackFunctions[move.pieceType](r, c, move, attacks)
        for i in range(len(attacks)):  # replaces attacked squares with blanks
            r1 = attacks[i][0]
            c1 = attacks[i][1]
            self.immobiliserCaller(r1, c1, self.board[r1][c1])  # handles captured Immobilising pieces
            if self.board[r1][c1][1] == 'K':
                #print(move.pieceMoved, (move.startRow, move.startCol), (move.endRow, move.endCol))
                self.checkmate = True
            self.board[r1][c1] = []

    def resetWithdrawer(self, startRow, startCol, piece):  # resets enemy withdrawn pieces if Withdrawer is not moved subsequently
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.isEnemyPiece(startRow, startCol, r, c) and not self.board[r][c][2] == piece[1]:
                    self.board[r][c][2] = False

    def withdrawnMovedPiece(self, endRow, endCol):  # if the moved Piece is withdrawn, checks if it is still next to withdrawing piece, removes pieces it has moved away from 
        if self.board[endRow][endCol] and self.board[endRow][endCol][2]:
            neighbours = self.getNeighbourSquares(endRow, endCol)
            for neighbour in neighbours:
                if self.isEnemy(neighbour[0], neighbour[1]) and self.board[neighbour[0]][neighbour[1]][1] == self.board[endRow][endCol][2]:
                    return
            self.board[endRow][endCol][2] = False


    def immobiliserCaller(self, r, c, piece):  # clears immobilisations
        if self.board[r][c][3]:  # if piece moved is acting as an immobiliser
                self.clearImmobilisedSqs(r, c, piece)
                self.clearImmobilisingChains(r, c, piece)

    def clearImmobilisedSqs(self, r, c, piece):  # clears neighbouring immobilised pieces from start square
        immobPieceKey = piece[0] + piece[1]
        neighbours = self.getNeighbourSquares(r, c)
        for neighbour in neighbours:
            if self.isEnemyPiece(r, c, neighbour[0], neighbour[1]) and self.board[neighbour[0]][neighbour[1]][4]:  # checks that the start sq neighbour is immobilised enemy
                immobilisedBy = [entry for entry in self.board[neighbour[0]][neighbour[1]][4] if not self.immobilisingPieces[immobPieceKey] in entry]
                self.board[neighbour[0]][neighbour[1]][4] = deepcopy(immobilisedBy)

    def clearImmobilisingChains(self, r1, c1, piece):
        immobPieceKey = piece[0] + piece[1]
        if not immobPieceKey[1] == 'I':
            piece[3] = []  # clears chain of moved chameleon
        for neighbour in self.getNeighbourSquares(r1, c1):
            if self.isEnemyPiece(r1, c1, neighbour[0], neighbour[1]) and self.board[neighbour[0]][neighbour[1]][1] in ['C', 'H']:  # checks if start sq borders any enemy chameleon
                chain_copy = []
                flag = False
                for chain in self.board[neighbour[0]][neighbour[1]][3]:  # for strings in list
                    if self.immobilisingPieces[immobPieceKey] in chain:  # if letter in string
                        flag = True # raise flag - indicates a chain has been removed
                    else:
                        chain_copy.append(chain)  # otherwise, add it to chain copy
                    self.board[neighbour[0]][neighbour[1]][3] = deepcopy(chain_copy)  # rewrites piece chain array with copy
                    if flag:  # if chain has been removed
                        if not self.board[neighbour[0]][neighbour[1]][3]:  # if no more chains, clears immobilised sqs
                            self.clearImmobilisedSqs(neighbour[0], neighbour[1], self.board[neighbour[0]][neighbour[1]])
                        # calls function again recursively - clears the chains and sqs until no relevant neighbours have any relevant neighbours left
                        self.clearImmobilisingChains(neighbour[0], neighbour[1], self.board[neighbour[0]][neighbour[1]])

    def getPawnMoves(self, r, c, moves):
        for b in borders:
            for i in range(1, 8):
                endRow = r + b[0] * i
                endCol = c + b[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if not endPiece:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:  # runs into occupied square
                        break
                else:  # off board
                    break
    
    def getPawnAttacks(self, r, c, move, attacks):
        # checks bordering squares for opposing piece
        # using this vector, checks one square over, first excluding squares that are off the board
        # if there is an attacked square, appends coords to list
        for b in range(len(borders)):
            targetRow = r + borders[b][0]
            targetCol = c + borders[b][1]
            if 0 <= targetRow < 8 and 0 <= targetCol < 8:
                if self.isEnemy(targetRow, targetCol):
                    allyRow = targetRow + borders[b][0]
                    allyCol = targetCol + borders[b][1]
                    if 0 <= allyRow < 8 and 0 <= allyCol < 8:
                        if self.isAlly(allyRow, allyCol):
                            attacks.append((targetRow, targetCol))

    def getImmobiliserMoves(self, r, c, moves):
        self.getCoordinatorMoves(r, c, moves)
    
    def getImmobiliserAttacks(self, r, c, move, attacks):  # checks neighbours for enemies, adds immobilisation signature
        neighbours = self.getNeighbourSquares(r, c)
        for neighbour in neighbours:
            if self.isEnemy(neighbour[0], neighbour[1]):
                self.board[neighbour[0]][neighbour[1]][4].append(self.immobilisingPieces[move.pieceMoved[0]+move.pieceMoved[1]])
    
    def getLeaperMoves(self, r, c, moves):
        self.leaps(r, c, moves, pieces)
    
    def getLeaperAttacks(self, r, c, move, attacks):  # checks along the path travelled and appends all pieces to attack list. Can afford to be dumb due the move logic
        sqs = []
        for x in range(1, max((abs(move.moveVector[0]), abs(move.moveVector[1])))):
            sqs.append((int(move.startRow + move.moveDirection[0] * x), int(move.startCol + move.moveDirection[1] * x)))
        for sq in sqs:        
            if self.board[sq[0]][sq[1]]:
                attacks.append((sq[0], sq[1]))
           
    def getChameleonMoves(self, r, c, moves):
        self.leaps(r, c, moves, ['L'])  # same moving logic as LLs, but has can only jump over 'L' pcs
        neighbours = self.getNeighbourSquares(r, c)
        for neighbour in neighbours:
            if self.isEnemy(neighbour[0], neighbour[1]) and self.board[neighbour[0]][neighbour[1]][1] == 'K':
                moves.append(Move((r, c), (neighbour[0], neighbour[1]), self.board))

    def getChameleonAttacks(self, r, c, move, attacks):
        self.withdraws(r, c, move, attacks, move.pieceType, ['W'])
        self.getLeaperAttacks(r, c, move, attacks)
        self.coordinators(r, c, attacks, ['O'])
            
        if self.isEnemy(r, c) and self.board[r][c][1] == 'K':
            attacks.append((r, c))

        if move.moveDirection in [(1, 0), (0, 1), (0, -1), (-1, 0)]:  # appends attacks on pawns
            for border in borders:  # if cham moves along rank/file, for bordering pieces
                if 0 <= (r + border[0]) < 8 and 0 <= (c + border[1]) < 8:  # if bordering piece on board
                    if self.isEnemy((r + border[0]), (c + border[1])):  # if bordering piece is enemy
                        if self.board[(r + border[0])][(c + border[1])][1] == 'P':  # if it is enemy pawn
                            if 0 <= (r + 2 * border[0]) < 8 and 0 <= (c + 2 * border[1]) < 8:  # if piece on opposite side of enemy pawn from cham is on board
                                if self.isAlly((r + 2 * border[0]), (c + 2 * border[1])):  # if piece is an ally
                                    attacks.append(((r + border[0]), (c + border[1]))) # append attack

        neighbours = self.getNeighbourSquares(r, c)
        for neighbour in neighbours:
            if self.isEnemy(neighbour[0], neighbour[1]) and self.board[neighbour[0]][neighbour[1]][3]:
                for chain in self.board[neighbour[0]][neighbour[1]][3]:
                    move.pieceMoved[3].append((chain + self.immobilisingPieces[move.pieceColor + move.pieceType]))  # adds to immobiling ability chain

        if move.pieceMoved[3]:
            self.getImmobiliserAttacks(r, c, move, attacks)  # if able to immobilise, calls immobiliser function
    
    def getKingMoves(self, r, c, moves):
        for i in range(8):
            endRow = r + vectors[i][0]
            endCol = c + vectors[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not self.isAlly(endRow, endCol):
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    
    def getKingAttacks(self, r, c, move, attacks):  # necessary to access some of the things that happen after capture (such as immob tracking)
        if self.isEnemy(r, c):
            attacks.append((r, c))
    
    def getWithdrawerMoves(self, r, c, moves):
        self.getCoordinatorMoves(r, c, moves)

    def getWithdrawerAttacks(self, r, c, move, attacks):
        self.withdraws(r, c, move, attacks, 'W', pieces)

    def getCoordinatorMoves(self, r, c, moves):
        for v in vectors:
            for i in range(1, 8):
                endRow = r + v[0] * i
                endCol = c + v[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if not endPiece:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:  # runs into occupied square
                        break
                else:  # off board
                    break
    
    def getCoordinatorAttacks(self, r, c, move, attacks):
        self.coordinators(r, c, attacks, pieces)
    
    def withdraws(self, r, c, move, attacks, piece, targetPcs):  # lesson here - don't try to do too much at once and break down functions/methods into smaller pieces. No point in making everything more complicated to keep it in one block of code
        targetDir = (int(move.moveDirection[0] * -1), int(move.moveDirection[1] * -1))  # first section takes care of attacks
        targetSq = (move.startRow + targetDir[0], move.startCol + targetDir[1])
        if 0 <= targetSq[0] < 8 and 0 <= targetSq[1] < 8:
            if self.isEnemy(targetSq[0], targetSq[1]) and self.board[targetSq[0]][targetSq[1]][2] == piece:  # checks to see if piecetype is in the log of withdrawing pcs
                while 0 <= targetSq[0] < 8 and 0 <= targetSq[1] < 8:
                    if self.isEnemy(targetSq[0], targetSq[1]):
                        attacks.append(targetSq)
                        targetSq = (targetSq[0] + targetDir[0], targetSq[1] + targetDir[1])
                    else:
                        break
        
        neighbours = self.getNeighbourSquares(move.startRow, move.startCol)  # first clears the withdrawn markers from neighbouring squares. This combined with initial withdrawer flag clearing should clear all flags
        for neighbour in neighbours:
            if self.isEnemy(neighbour[0], neighbour[1]) and self.board[neighbour[0]][neighbour[1]][2]:
                self.board[neighbour[0]][neighbour[1]][2] == False

        neighbours = self.getNeighbourSquares(r, c)
        for neighbour in neighbours:  # flags pieces that are newly attacked by withdrawer/cham
            if self.isEnemy(neighbour[0], neighbour[1]) and self.board[neighbour[0]][neighbour[1]][1] in targetPcs:  # if neighbour is enemy and is a valid target (withdrawer in case of chameleon)
                self.board[neighbour[0]][neighbour[1]][2] = piece

    def coordinators(self, r, c, attacks, validCoordPcs):  # for relevant king coords, checks the intersection of rank & file, file & rank
        kingCoords = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        if self.isEnemy(kingCoords[0], c) and self.board[kingCoords[0]][c][1] in validCoordPcs:  # unsure of this, adding extra work for coords in order to reuse code for the CHams
            attacks.append((kingCoords[0], c))
        if self.isEnemy(r, kingCoords[1]) and self.board[r][kingCoords[1]][1] in validCoordPcs:
            attacks.append((r, kingCoords[1]))

    def leaps(self, r, c, moves, validLeapedPcs):
        for v in vectors:  # moves along vector directions up to max length of board
            for i in range(1, 8):
                endRow = r + v[0] * i
                endCol = c + v[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # first, checks target sq is on board
                    if not self.board[endRow][endCol]:  # if target sq is empty, appends move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif self.isEnemy(endRow, endCol) and self.board[endRow][endCol][1] in validLeapedPcs:  # if sq is enemy, and is a valid piece to leap (important for CHams) checks one sq further along vector (the 'jump')
                        endRow = r + v[0] * (i + 1)
                        endCol = c + v[1] * (i + 1)
                        if 0 <= endRow < 8 and 0 <= endCol < 8 and self.board[endRow][endCol]:
                            break # if this square is occupied, breaks square loop and begins new vector. Othwise, square loop continues by examining and adding the empty sq
                    else:
                        break  # breaks sq loop if target sq is ally
                else:
                    break  # breaks sq loop if target sq is off board

    def getNeighbourSquares(self, r, c):  # returns list of all neighbouring squares
        neighbourSquares = []
        for vector in vectors:
            endRow = r + vector[0]
            endCol = c + vector[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                neighbourSquares.append((endRow, endCol))
        return neighbourSquares
    
    def isAlly(self, r, c):  # checks to see if piece at sq (r, c) is an ally
        if self.board[r][c] and self.whiteToMove and self.board[r][c][0] == 'w':
            return True
        elif self.board[r][c] and not self.whiteToMove and self.board[r][c][0] == 'b':
            return True  # important to ask if list has elements first to avoid index errors on empty sqs
        else:
            return False

    def isEnemy(self, r, c):  # checks to see if piece at certain sq is an enemy. Returns false if blank sq. Could also do this referenced off piecemoved
        if self.board[r][c] and self.whiteToMove and self.board[r][c][0] == 'b':
            return True
        elif self.board[r][c] and not self.whiteToMove and self.board[r][c][0] == 'w':
            return True
        else:
            return False
        
    def isEnemyPiece(self, selfrow, selfcol, enemyrow, enemycol):  # unfortunate, but have used the above logic for everything previous. Doesn't fit needs of immobilisers
        if self.board[selfrow][selfcol] and self.board[enemyrow][enemycol]:
            if self.board[selfrow][selfcol][0] != self.board[enemyrow][enemycol][0]:
                return True
        else:
            return False

class Move():

    # maps keys to values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}  # reverses keys and values
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4,
                   "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        if not board[self.startRow][self.startCol]:  # immediately returns to Main if sq is empty
            return
        
        self.pieceColor = deepcopy(board[self.startRow][self.startCol][0])  # otherwise, continues identifying piece/move characteristics
        self.pieceType = deepcopy(board[self.startRow][self.startCol][1])
        self.pieceMoved = deepcopy(board[self.startRow][self.startCol])
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

        self.moveVector = (self.endRow - self.startRow, self.endCol - self.startCol)
        self.moveDirection = self.getMoveDirection(self.moveVector)


    def getMoveDirection(self, vector):
        r = 0 if vector[0] == 0 else vector[0]/abs(vector[0])
        c = 0 if vector[1] == 0 else vector[1]/abs(vector[1])
        return(r, c)
    
    def getSqsTravelled(self):  # gets sqs traversed (excluses start and end sqs)
        sqs = []
        for sq in range(max(self.moveVector) - 1):
            sqs.append(int(self.startRow + self.moveDirection[0]), int(self.startCol + self.moveDirection[1]))
        return sqs

    '''
    overriding equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
defaultBoard = [
            [["b", "O", False, False, []], ["b", "L", False, False, []], ["b", "C", False, [], []], ["b", "W", False, False, []], 
                ["b", "K", False, False, []], ["b", "H", False, [], []], ["b", "L", False, False, []], ["b", "I", False, [('I')], []]],
            [["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], 
                ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []]],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], 
                ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []]],
            [["w", "I", False, [('i')], []], ["w", "L", False, False, []], ["w", "C", False, [], []], ["w", "W", False, False, []], 
                ["w", "K", False, False, []], ["w", "H", False, [], []], ["w", "L", False, False, []], ["w", "O", False, False, []]]]

flippedBoard = [
            [["w", "O", False, False, []], ["w", "L", False, False, []], ["w", "C", False, [], []], ["w", "W", False, False, []], 
                ["w", "K", False, False, []], ["w", "H", False, [], []], ["w", "L", False, False, []], ["w", "I", False, [('I')], []]],
            [["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], 
                ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []]],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], 
                ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []]],
            [["b", "I", False, [('i')], []], ["b", "L", False, False, []], ["b", "C", False, [], []], ["b", "W", False, False, []], 
                ["b", "K", False, False, []], ["b", "H", False, [], []], ["b", "L", False, False, []], ["b", "O", False, False, []]]]




