class GameState():
    colsToFiles = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    filesToCols = {v:k for k, v in colsToFiles.items()}
    rowsToRanks = {0:'8', 1:'7', 2:'6', 3:'5', 4:'4', 5:'3', 6:'2', 7:'1'}
    ranksToRows = {v:k for k, v in rowsToRanks.items()}

    def setZero(self):
        self.valid = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]

    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.setZero()
        self.moveHistory = []
        self.whiteTurn = True
    
    def reset(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        self.setZero()
        self.moveHistory = []
        self.whiteTurn = True

    def __str__(self):
        s = ''
        for row in self.board:
            s += str(row)
            s += '\n'
        s += '\n'
        return s
    
    def getLocationString(self, col, row):
        return self.colsToFiles[col] + self.rowsToRanks[row]
    
    def update(self, row, col, Row, Col):
        self.moveHistory.append(self.getLocationString(col, row) + self.getLocationString(Col, Row) + self.board[Row][Col])
        self.board[Row][Col] = self.board[row][col]
        self.board[row][col] = '--'
        # print(self.moveHistory)
        
    def undoMove(self):
        if self.moveHistory:
            row = int(self.ranksToRows[self.moveHistory[-1][3]])
            col = int(self.filesToCols[self.moveHistory[-1][2]])
            Row = int(self.ranksToRows[self.moveHistory[-1][1]])
            Col = int(self.filesToCols[self.moveHistory[-1][0]])
            self.board[Row][Col] = self.board[row][col]
            self.board[row][col] = self.moveHistory[-1][4] + self.moveHistory[-1][5]
            del self.moveHistory[-1]

    def getPossibleMoves(self, row, col):
        moves = []
        b = self.board
        if(b[row][col][0] == 'w' and self.whiteTurn) or (b[row][col][0] == 'b' and not self.whiteTurn):
            if b[row][col][1] == 'P':
                self.getPawnMoves(row, col, moves)
            if b[row][col][1] == 'R':
                self.getRookMoves(row, col, moves)
            if b[row][col][1] == 'B':
                self.getBishopMoves(row, col, moves)
            if b[row][col][1] == 'Q':
                self.getRookMoves(row, col, moves)
                self.getBishopMoves(row, col, moves)
            if b[row][col][1] == 'K':
                self.getKingMoves(row, col, moves)
        for i in range(len(moves) - 1, -1, -1):
            self.update(self.ranksToRows[moves[i][1]], self.filesToCols[moves[i][0]], self.ranksToRows[moves[i][3]], self.filesToCols[moves[i][2]])
            row, col = self.findKing()
            if self.squareUnderAttack(row, col):
                moves.remove(moves[i])
            self.undoMove()
        return moves

    def getAllPossibleMoves(self):
        moves = []
        b = self.board
        for i in range(8):
            for j in range(8):
                if (b[i][j][0] == 'w' and self.whiteTurn) or (b[i][j][0] == 'b' and not self.whiteTurn):
                    if b[i][j][1] == 'P':
                        self.getPawnMoves(i, j, moves)
                    if b[i][j][1] == 'R':
                        self.getRookMoves(i, j, moves)
                    if b[i][j][1] == 'B':
                        self.getBishopMoves(i, j, moves)
                    if b[i][j][1] == 'Q':
                        self.getRookMoves(i, j, moves)
                        self.getBishopMoves(i, j, moves)
                    if b[i][j][1] == 'K':
                        self.getKingMoves(i, j, moves)
        return moves

    def getKingMoves(self, row, col, moves):
        b = self.board
        startMove = self.getLocationString(col, row)
        color = 'w' if self.whiteTurn else 'b'
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 1), (1, 0)]
        for dir in directions:
            if (0 <= row + dir[0] <= 7) and (0 <= col + dir[1] <= 7):
                if b[row + dir[0]][col + dir[1]][0] != color:
                    move = startMove + self.getLocationString(col + dir[1], row + dir[0])
                    moves.append(move)

    def getPawnMoves(self, row, col, moves):
        b = self.board
        startMove = self.getLocationString(col, row)
        if self.whiteTurn:
            if row == 6 and b[row-2][col] == '--':
                move = startMove + self.getLocationString(col, row-2)
                moves.append(move)
            if row >= 1 and b[row-1][col] == '--':
                move = startMove + self.getLocationString(col, row-1)
                moves.append(move)
            if col >= 1 and row >= 1 and b[row-1][col-1][0] == 'b':
                move = startMove + self.getLocationString(col-1, row-1)
                moves.append(move)
            if col <= 6 and row >= 1 and b[row-1][col+1][0] == 'b':
                move = startMove + self.getLocationString(col+1, row-1)
                moves.append(move)
        else:
            if row == 1 and b[row+2][col] == '--':
                move = startMove + self.getLocationString(col, row+2)
                moves.append(move)
            if row <= 6 and b[row+1][col] == '--':
                move = startMove + self.getLocationString(col, row+1)
                moves.append(move)
            if col <= 6 and row <= 6 and b[row+1][col+1][0] == 'w':
                move = startMove + self.getLocationString(col+1, row+1)
                moves.append(move)
            if col >= 1 and row <= 6 and b[row+1][col-1][0] == 'w':
                move = startMove + self.getLocationString(col-1, row+1)
                moves.append(move)

    def getRookMoves(self, row, col, moves):
        b = self.board
        startMove = self.getLocationString(col, row)
        i = row - 1
        while i >= 0:
            if b[i][col] == '--':
                move = startMove + self.getLocationString(col, i)
                moves.append(move)
                i -= 1
            elif b[row][col][0] == b[i][col][0]:
                break
            else:
                move = startMove + self.getLocationString(col, i)
                moves.append(move)
                break
        i = row + 1
        while i <= 7:
            if b[i][col] == '--':
                move = startMove + self.getLocationString(col, i)
                moves.append(move)
                i += 1
            elif b[row][col][0] == b[i][col][0]:
                break
            else:
                move = startMove + self.getLocationString(col, i)
                moves.append(move)
                break
        i = col - 1
        while i >= 0:
            if b[row][i] == '--':
                move = startMove + self.getLocationString(i, row)
                moves.append(move)
                i -= 1
            elif b[row][col][0] == b[row][i][0]:
                break
            else:
                move = startMove + self.getLocationString(i, row)
                moves.append(move)
                break
        i = col + 1
        while i <= 7:
            if b[row][i] == '--':
                move = startMove + self.getLocationString(i, row)
                moves.append(move)
                i += 1
            elif b[row][col][0] == b[row][i][0]:
                break
            else:
                move = startMove + self.getLocationString(i, row)
                moves.append(move)
                break

    def getBishopMoves(self, row, col, moves):
        b = self.board
        startMove = self.getLocationString(col, row)
        i, j = col + 1, row + 1
        while i <= 7 and j <= 7:
            if b[j][i] == '--':
                move = startMove + self.getLocationString(i, j)
                moves.append(move)
                i += 1
                j += 1
            elif b[row][col][0] == b[j][i][0]:
                break
            else:
                move = startMove + self.getLocationString(i, j)
                moves.append(move)
                break
        i, j = col - 1, row - 1
        while i >= 0 and j >= 0:
            if b[j][i] == '--':
                move = startMove + self.getLocationString(i, j)
                moves.append(move)
                i -= 1
                j -= 1
            elif b[row][col][0] == b[j][i][0]:
                break
            else:
                move = startMove + self.getLocationString(i, j)
                moves.append(move)
                break
        i, j = col + 1, row - 1
        while i <= 7 and j >= 0:
            if b[j][i] == '--':
                move = startMove + self.getLocationString(i, j)
                moves.append(move)
                i += 1
                j -= 1
            elif b[row][col][0] == b[j][i][0]:
                break
            else:
                move = startMove + self.getLocationString(i, j)
                moves.append(move)
                break
        i, j = col - 1, row + 1
        while i >= 0 and j <= 7:
            if b[j][i] == '--':
                move = startMove + self.getLocationString(i, j)
                moves.append(move)
                i -= 1
                j += 1
            elif b[row][col][0] == b[j][i][0]:
                break
            else:
                move = startMove + self.getLocationString(i, j)
                moves.append(move)
                break

    def squareUnderAttack(self, row, col):
        self.whiteTurn = not self.whiteTurn
        moves = self.getAllPossibleMoves()
        for move in moves:
            if self.filesToCols[move[2]] == col and self.ranksToRows[move[3]] == row:
                self.whiteTurn = not self.whiteTurn
                return True
        self.whiteTurn = not self.whiteTurn
        return False

    def findKing(self):
        b = self.board
        ownKing = 'wK' if self.whiteTurn else 'bK'
        for i in range(8):
            for j in range(8):
                if b[i][j] == ownKing:
                    return i, j



            






