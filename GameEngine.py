
class GameState():
    colsToFiles = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    filesToCols = {v:k for k, v in colsToFiles.items()}
    rowsToRanks = {0:'8', 1:'7', 2:'6', 3:'5', 4:'4', 5:'3', 6:'2', 7:'1'}
    ranksToRows = {v:k for k, v in rowsToRanks.items()}

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
        print(self.moveHistory)
        
    def undoMove(self):
        if self.moveHistory:
            row = int(self.ranksToRows[self.moveHistory[-1][3]])
            col = int(self.filesToCols[self.moveHistory[-1][2]])
            Row = int(self.ranksToRows[self.moveHistory[-1][1]])
            Col = int(self.filesToCols[self.moveHistory[-1][0]])
            self.board[Row][Col] = self.board[row][col]
            self.board[row][col] = self.moveHistory[-1][4] + self.moveHistory[-1][5]
            del self.moveHistory[-1]
    
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        return moves

    def getAllPossibleMoves(self):
        moves = []
        b = self.board
        for row in range(len(b)):
            for col in range(len(b)):
                if(b[row][col][0] == 'w' and self.whiteTurn) or (b[row][col][0] == 'b' and not self.whiteTurn):
                    if b[row][col][1] == 'P':
                        self.getPawnMoves(row, col, moves)
                    if b[row][col][1] == 'R':
                        self.getRookMoves(row, col, moves)
        return moves
    
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
            






