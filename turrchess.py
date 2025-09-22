
import chess
import random

board = chess.Board()

moves = []

def makeMove(move):
    if move == "": return False

    if move in [board.san(m) for m in board.legal_moves]:
        moves.append(move)
        board.push_san(move)
        return True
    else:
        print("Illegal Move, try again.")
        return False

def newBoard():
    global moves
    global board
    board = chess.Board()
    moves = []

def pvp():
    newBoard()
    print("Enter \'quit\' to exit")
    print("Enter \'display\' to display board")
    while not board.is_game_over():
        print("========================")
        try:
            move = input("Move: ")
            if move.lower() == "quit":
                print("Game terminated")
                break
            elif move.lower() == "display":
                print(board)
                continue

            makeMove(move)
        except ValueError:
            print("Invalid move format or illegal move, please try again.")
    print("Game over", board.result(), "\n", moves)

# square to coords
def stc(square):
    file = square % 8     # 0 = a, 7 = h
    rank = square // 8    # 0 = rank 1, 7 = rank 8
    return file, rank

myMove = ""
def evaluate():
    global board
    if board.is_checkmate():
        return -99999 if board.turn else 99999

    material = 0

    i = 0
    while i < 64:
        piece = board.piece_at(i)
        if piece is not None:
            colorMul = 1 if piece.__str__().isupper() else -1
            if piece.__str__() in "Pp": material += colorMul * 10
            if piece.__str__() in "Nn": material += colorMul * 30
            if piece.__str__() in "Bb": material += colorMul * 30
            if piece.__str__() in "Rr": material += colorMul * 50
            if piece.__str__() in "Qq": material += colorMul * 90
            if piece.__str__() in "Kk": material += colorMul * 900
        file, rank = stc(i)

        if piece.__str__() in "Pp":
            if file >= 3 and file <= 4 and rank >= 3 and rank <= 4:
                material += 2 * colorMul
        elif piece.__str__() in "Nn":
            if file >= 2 and file <= 5 and rank >= 2 and rank <= 5:
                material += 2 * colorMul
        i += 1
    return material

movesChecked = 0
def minimax(depth, alpha, beta, isMaxing):
    global board
    global myMove
    global movesChecked
    possible_moves = [board.san(m) for m in board.legal_moves]

    if depth == 0 or len(possible_moves) == 0:
        return evaluate()
    
    
    bestEval = -99999 if isMaxing else 99999
    # ???!!
    bestMove = possible_moves[0]

    for m in possible_moves:
        board.push_san(m)
        evaluation = minimax(depth-1, alpha, beta, not isMaxing)
        movesChecked += 1
        print("Moves checked:", movesChecked, end="\r", flush=True)
        board.pop()
        if (isMaxing and (evaluation > bestEval)) or (not isMaxing and (evaluation < bestEval)):
            bestEval = evaluation
            bestMove = m 
        if isMaxing:
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        else:
            beta = min(beta, evaluation)
            if beta <= alpha:
                break


    myMove = bestMove
    return bestEval

def think(playingAsWhite, depth):
    global board
    global myMove

    minimax(depth, -99999, 99999, playingAsWhite)

    return myMove

def vcomputer():
    global movesChecked
    newBoard()

    # the color the computer is playing as
    playingAsWhite = True

    depth = 4
    while True:
        try:
            depthi = input("Depth(leave blank for default)")
            if not bool(depthi.strip()):
                break
            depth = int(depthi)
            break
        except ValueError:
            print("Please enter a number.")

    color = input("play as white or black? (enter w/b)")
    if color.lower() == "w":
        playingAsWhite = False
        while True:
            move = input("Enter first move:")
            startPlaying = makeMove(move)
            if startPlaying: break

    print("Enter \'quit\' to exit")
    print("Enter \'display\' to display board")
    while not board.is_game_over():
        try:
            if (playingAsWhite and (board.turn == chess.WHITE)) or (not playingAsWhite and (board.turn == chess.BLACK)):
                if playingAsWhite: print("========================")
                AI_move = think(playingAsWhite, depth)
                makeMove(AI_move)
                print(f"-> {AI_move}  Moves checked:{movesChecked}")
                movesChecked = 0
            else:
                if not playingAsWhite: print("========================")
                move = input("Move: ")
                if move.lower() == "quit":
                    print("Game terminated")
                    break
                elif move.lower() == "display":
                    print(board)
                    continue
                makeMove(move)
        except ValueError:
            print("Invalid move format or illegal move, please try again.")
    print("Game over", board.result(), "\n", moves)

def mainloop():
    print("===Welcome to TurrChess!===")
    while True:
        print("1 - player vs player\n2 - player vs computer\n3 - exit")
        option = input()
        if option =="" or option not in "123":
            print("input invalid")
            continue
        elif option == "1":
            pvp()
            print("=======================")
        elif option == "2":
            vcomputer()
            print("=======================")
        elif option == "3":
            break
        else:
            print("input invalid")
            continue

mainloop()
