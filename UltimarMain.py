'''
main driver file
'''

import pygame as p
import sys
from copy import deepcopy
from Ultimar import UltimarEngine, UltimarAI, UltimarMenu

WIDTH = HEIGHT = 512  # tweak idea : user inputted / selected board size
DIMENSION = 8  # board dimensions are 8x8
SQ_SIZE = HEIGHT // DIMENSION
IMAGES = {}
MAX_FPS = 15  # for animations

'''
Initialise a global directory of images. This will be called once in main
'''
def loadImages():
    pieces = ['wP', 'wK', 'wO', 'wC', 'wH', 'wW', 'wL', 'wI', 'bP', 'bK', 'bO', 'bC', 'bH', 'bW', 'bL', 'bI']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Ultimar/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    options = UltimarMenu.runMenu(screen)  # runs menu, returns dictionary of options
    print(options)

    playerOne = False
    playerTwo = False
    if options[0]:  # handles the options inputs as fed in by menu
        playerOne = True
        playerTwo = True
    elif options[1]:
        if options[6]:
            playerOne = True
        else:
            playerTwo = True
            UltimarEngine.boardSelect = False

    enableUndo = options[3]
    global immobHighlights 
    immobHighlights = options[4]
    global moveHighlights
    moveHighlights = options[5]

    screen.fill(p.Color("white"))
    gs = UltimarEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  #flag variable for when move is made
    animate = True
    loadImages()
    running = True
    sqSelected = ()  # no square selected initially, tuple to keep track of last click in (row, col) format
    playerClicks = []  # keeps track of player clicks (two tuples) - can be used for log
    gameOver = False  # for Checkmates/stalemates
    navigator = -1  # used to track navigation thru gameLog

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn and navigator == -1:
                    location = p.mouse.get_pos()  #(x,y) of mouse location at click
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if len(playerClicks) == 1 and not gs.board[playerClicks[0][0]][playerClicks[0][1]]:
                        sqSelected = ()
                        playerClicks = []
                    elif sqSelected == (row, col):  # deselects sq if user clicks same square twice
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  #appends first and second clicks
                    if len(playerClicks) == 2:  #after second click

                        move = UltimarEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(move)
                                moveMade = True
                                animate = True
                                sqSelected = ()  #reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handler - want to be able to iterate thru gamestates with arrow keys, then press enter to select returning to a specific gamestate (deleting subsequent gs). mouseclick auto returns to current gs.
            elif e.type == p.KEYDOWN:
                sqSelected = ()
                playerClicks = []
                if e.key == p.K_LEFT:  #travels one move backwards with left arrow key
                        if navigator > -1 * len(gs.gameLog):  # makes sure that you can't go back too far
                            navigator -= 1
                            gs.board = gs.gameLog[navigator]
                elif e.key == p.K_RIGHT:
                        if navigator < -2:
                            navigator += 1
                            gs.board = gs.gameLog[navigator]
                        elif navigator == -2:  # wanted to use shallowcopy for performance benefits, but when I return to the present gameboard, must deepcopy so that board is not saved to reference gs.gamelog[navigator] in log 
                            navigator += 1
                            gs.board = deepcopy(gs.gameLog[navigator])
                elif e.key == p.K_RETURN:  # if enter is hit while looking at past board, removes subsequent log entries and resets navigator (refreshing current gs in the process)
                    if navigator != -1 and enableUndo:
                        gs.logCutoff(navigator)
                        gameOver = False
                        validMoves = gs.getValidMoves()
                        navigator = -1
                    else:  # if enable undo not selected, returns to present board
                        gs.board = gs.gameLog[-1]
                        validMoves = gs.getValidMoves()
                        navigator = -1

        # AI move finder
        if not gameOver and not humanTurn:
            AIMove = UltimarAI.findBestMove(gs, validMoves)
            print(AIMove)
            if AIMove is None:
                AIMove = UltimarAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            print(AIMove.pieceMoved)
            moveMade = True
            animate = True

        if moveMade:
            print(gs.counter)
            gs.counter = 0
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)  # ends game loop if there is checkmate/stalemate, triggers text
        if navigator == -1:  # removes text if navigating thru game Log
            if gs.checkmate:
                gameOver = True
                if playerOne ^ playerTwo:  # exclusive or operator - returns True if human is playing machine
                    if (playerOne and not gs.whiteToMove) or (playerTwo and gs.whiteToMove):
                        drawText(screen, 'CONGRATULATIONS!You are the first human to defeat UltimarAI!')
                    else:

                        drawText(screen, 'You were crushed by UltimarAI...')
                else:
                    if gs.whiteToMove:
                        drawText(screen, 'Black wins!')
                    else:
                        drawText(screen, 'White wins!')
            elif gs.stalemate:
                gameOver = True
                drawText(screen, 'Stalemate!')

        clock.tick(MAX_FPS)
        p.display.flip()
            
'''
Highlight square selected and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c]:
            if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # could have saved lots of lines in engine with this
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)  # transparency value 0 is transparent, 255 is opaque
                s.fill(p.Color('blue'))
                screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
                s.fill(p.Color('yellow'))
                for move in validMoves:
                    if move.startRow == r and move.startCol == c:
                        screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def flagImmobilisedSqs(screen, immobilisedSqs):
    if immobilisedSqs:
        t = p.Surface((SQ_SIZE, SQ_SIZE))  # turns the immobilised squares red
        t.set_alpha(100)
        t.fill(p.Color('red'))
        for i in immobilisedSqs:
            screen.blit(t, (i[1]*SQ_SIZE, i[0]*SQ_SIZE))

def getImmobilisedSqs(gs):
    immobilisedSqs = []
    for r in range(8):
        for c in range(8):
            if gs.board[r][c] and gs.board[r][c][4]:
                immobilisedSqs.append((r, c))
    return immobilisedSqs

'''
Responsible for all graphics within current game state
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) # draws squares on board
    if moveHighlights:
        highlightSquares(screen, gs, validMoves, sqSelected)
    if immobHighlights:
        flagImmobilisedSqs(screen, getImmobilisedSqs(gs))
    drawPieces(screen, gs.board) # draws pieces on top of squares

'''
draws squares on the board
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")] #can change this to take user inputs
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
draw the pieces on the board using current gamestate.board'''
def drawPieces(screen,  board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if board[r][c]:
                piece = board[r][c][0] + board[r][c][1]
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    piece = move.pieceColor + move.pieceType
    for frame in range(frameCount + 1):  # iterates thru path, drawing each frame
        r, c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Red'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 -
                                                    textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()

