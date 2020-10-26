import game
import time
import random
import operator
import sys
import chess
import chess.polyglot
import chess.syzygy

pieceValue = dict({'R':50, 
                   'N':30,
                   'B':32.5,
                   'Q':90,
                   'K':900,
                   'P':10,
                   'r':-50,
                   'n':-30,
                   'b':-32.5,
                   'q':-90,
                   'k':-900,
                   'p':-10,})

def syzygyAnalysis(board):
    with chess.syzygy.open_tablebase("data/syzygy/regular") as tablebase:
        if tablebase.get_dtz(board) != None:
            Pvalue = list()
            Ovalue = list()
            Pmove = list()
            Omove = list()
            Tmove = list()
            for move in board.legal_moves:
                auxBoard = board.copy()
                auxBoard.push(move)
                value = tablebase.get_dtz(auxBoard)
                if value == 0:
                    Tmove.append(move)
                elif value > 0:
                    Ovalue.append(value)
                    Omove.append(move)
                elif value < 0:
                    Pvalue.append(value)
                    Pmove.append(move)
            print(Pmove)
            print(Pvalue)
            while True:
                winning = False
                # TERMINAR
                if len(Pvalue) != 0:
                    index = Pvalue.index(max(Pvalue))
                    move = Pmove[index]
                    winning = True
                elif len(Tmove) != 0:
                    move = Tmove[0]
                elif len(Omove) != 0:
                    index = Ovalue.index(max(Ovalue))
                    move = Omove[index]
                # TERMINAR
                if winning:
                    auxBoard = board.copy()
                    auxBoard.push(move)
                    if not auxBoard.is_repetition():
                        break
                    else:
                        Pvalue.pop(index)
                        Pmove.pop(index)
                else:
                    break
        else:
            move = None
    return move


def polyglotAnalysis(board):
    with chess.polyglot.open_reader("data\polyglot\codekiddy.bin") as reader:
        entries = list()
        for entry in reader.find_all(board):
            entries.append([entry.move, entry.weight])
            print(entry.move, entry.weight, entry.learn)
    return entries


finishedScores = dict({'1-0': 10000,
                       '0-1': -1000,
                       '1/2-1/2': 0, })


def evaluatePosition(board, currentPlayer, desiredPlayer):
    score = 0
    stringBoard = board.fen()
    print(board)
    data = stringBoard.split()
    data = data[0]
    for temp in data:
        if temp in pieceValue:
            score = score + pieceValue[temp]
    if board.is_game_over():
        resultString = board.result()
        score = score + finishedScores[resultString]
    print(score)
    if desiredPlayer == chess.WHITE:
        return score
    elif desiredPlayer == chess.BLACK:
        return (-score)


def newTurn(gameState, currentPlayer):
    if currentPlayer == newTurn.userTurn:
        print('User Moves')
        move = userMoves(gameState.board)
    else:
        print('Computer Moves')
        move = cpuMoves(gameState.board)
    return move
newTurn.userTurn = chess.BLACK


def userMoves(board):
    validInput = False
    while not validInput:
        parsed = False
        while not parsed:
            try:
                userInput = input()
                move = chess.Move.from_uci(userInput)
                parsed = True  # we only get here if the previous line didn't throw an exception
            except ValueError:
                print('Invalid move!')
        if move in board.legal_moves:
            validInput = True
        else:
            print('Ilegal Move!')
    return move

def cpuMoves(board):
    to = time.time()
    if cpuMoves.opening == True:
        entries = polyglotAnalysis(board)
        if len(entries) != 0:
            bestMoveScore = 0
            cpuMove = entries[0][0]
            
        else:
            cpuMoves.opening = False
            print('Opening Finished')
    if cpuMoves.opening == False:
        cpuMove = syzygyAnalysis(board)
        if cpuMove != None:
            print('Ending')
            bestMoveScore = 0
        else:
            bestMoveScore, cpuMove = miniMaxAlphaBeta(board, cpuMoves.depth, -float('inf'), float('inf'), board.turn)
    tf = time.time()
    print('MiniMax algorithm lasted %f seconds.' % (tf-to))
    print('Best Move score: %f' % bestMoveScore)
    return cpuMove
cpuMoves.opening = True
cpuMoves.depth = 2

def miniMaxAlphaBeta(board, depth, alpha, beta, currentPlayer):
    bestMove = None
    if board.is_game_over(claim_draw=True) or depth == 0:
        return evaluatePosition(board, currentPlayer, miniMaxAlphaBeta.desiredPlayer), bestMove
    if currentPlayer == miniMaxAlphaBeta.desiredPlayer:
        for move in board.legal_moves:
            board.push(move)
            if depth == cpuMoves.depth:
                auxAlpha = max(alpha, miniMaxAlphaBeta(board, depth-1, alpha, beta, not currentPlayer)[0])
                if auxAlpha > alpha:
                    bestMove = move
                    alpha = auxAlpha
            elif depth != cpuMoves.depth:
                alpha = max(alpha, miniMaxAlphaBeta(board, depth-1, alpha, beta, not currentPlayer)[0])
            board.pop()
            if beta <= alpha:
                break
        return alpha, bestMove
    elif currentPlayer != miniMaxAlphaBeta.desiredPlayer:
        for move in board.legal_moves:
            board.push(move)
            beta = min(beta, miniMaxAlphaBeta(board, depth-1, alpha, beta, not currentPlayer)[0])
            board.pop()
            if beta <= alpha:
                break
        return beta, bestMove
miniMaxAlphaBeta.desiredPlayer = chess.WHITE

runGame = game.Game()
runGame.gameState.render()
while not runGame.gameState.isEndGame:
    nextMove = newTurn(runGame.gameState, runGame.currentPlayer)
    runGame.step(nextMove)
    runGame.gameState.render()
