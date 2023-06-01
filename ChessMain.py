import GameEngine
import pygame as p 

WIDTH = HEIGHT = 400
SQ_SIZE = WIDTH // 8
IMAGES = {}

def loadImages():
    global IMAGES
    pieceNames = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK',
                  'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieceNames:
        IMAGES[piece] = p.transform.scale(p.image.load('Pieces/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

def drawBoard(screen, gameState):
    for i in range(8):
        for j in range(8):
            if gameState.valid[j][i] == 1:
                p.draw.rect(screen, 'Yellow', (SQ_SIZE * i, SQ_SIZE * j, SQ_SIZE, SQ_SIZE))
            elif (i + j) % 2 == 0:
                p.draw.rect(screen, 'Grey', (SQ_SIZE * i, SQ_SIZE * j, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, 'Grey30', (SQ_SIZE * i, SQ_SIZE * j, SQ_SIZE, SQ_SIZE))
    return
    
def drawImages(screen, board, row, col, moving):
    for i in range(8):
        for j in range(8):
            if board[i][j] != '--' and not (moving == True and i == row and j == col):
                screen.blit(IMAGES[board[i][j]], (SQ_SIZE * j, SQ_SIZE * i))

def getSquareClicked(mouseCoordinates):
    squareRow = mouseCoordinates[1] // SQ_SIZE
    squareCol = mouseCoordinates[0] // SQ_SIZE
    return (squareRow, squareCol)

def markMoves(row, col, gameState):
    validMoves = gameState.getPossibleMoves(row, col)
    for moves in validMoves:
        x = int(gameState.ranksToRows[moves[3]])
        y = int(gameState.filesToCols[moves[2]])
        gameState.valid[x][y] = 1

def validMove(row, col, Row, Col, gameState):
    if Row >= 0 and Row <= 7 and Col >= 0 and Col <= 7:
        move = gameState.getLocationString(col, row) + gameState.getLocationString(Col, Row)
        validMoves = gameState.getPossibleMoves(row, col)
        if move in validMoves:
            return True
    return False

def main():
    p.init()
    loadImages()
    clock = p.time.Clock()
    gameState = GameEngine.GameState()
    p.display.set_caption("The Game of Chess")
    screen = p.display.set_mode((WIDTH, HEIGHT))

    done = False
    moving = False
    row = 0
    col = 0

    while not done:
        for e in p.event.get():
            if e.type == p.QUIT:
                done = True
            if e.type == p.MOUSEBUTTONDOWN:
                moving = True
                row, col = getSquareClicked(p.mouse.get_pos())
                markMoves(row, col, gameState)
            if e.type == p.MOUSEBUTTONUP:
                moving = False
                gameState.setZero()
                Row, Col = getSquareClicked(p.mouse.get_pos())
                if validMove(row, col, Row, Col, gameState):
                    gameState.update(row, col, Row, Col)
                    gameState.whiteTurn = not gameState.whiteTurn
            if e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gameState.undoMove()
                if e.key == p.K_r:
                    gameState.reset()

        drawBoard(screen, gameState)
        drawImages(screen, gameState.board, row, col, moving)
        if moving == True:
            x, y = p.mouse.get_pos()
            if(gameState.board[row][col] != '--'):
                screen.blit(IMAGES[gameState.board[row][col]], (x - SQ_SIZE / 2, y - SQ_SIZE / 2))

        p.display.update()
        clock.tick()

if __name__ == "__main__":
    main()
